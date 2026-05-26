import numpy as np
from collections import defaultdict
from argdigest import arg_digest
from smonitor import signal
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.data.smarts import LIGAND_SMARTS
from pharmacophoremt.utils.conformers import ConformerGenerator
import molsysmt as msm
from rdkit import Chem


class VirtualScreening:
    """Engine to screen molecular libraries against a pharmacophore model.

    Matching uses the native LIGAND_SMARTS feature definitions for consistency
    with the modeling pipeline. A Fit Value (0–1) is assigned to each hit:

        FitValue = Σ(weight_i for matched sites) / Σ(weight_i for all sites)

    Directional sites (SphereAndVector) additionally check that the ligand
    feature vector falls within ``direction_tolerance`` degrees of the site
    direction. ExcludedVolume sites veto any conformer whose heavy atoms
    clash with the defined exclusion spheres.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        The query pharmacophore.
    min_match_ratio : float, optional
        Minimum fraction of essential-site weight that must be matched for a
        molecule to be considered a hit (default 1.0 = all essential sites).
    n_conformers : int, optional
        Maximum conformers to generate when a molecule has none (default 50).
    point_tolerance : float, optional
        Matching tolerance in nm for Point-shaped sites (default 0.10 nm).
    direction_tolerance : float, optional
        Maximum angular deviation in degrees for directional sites
        (SphereAndVector). Default 30°.
    """

    def __init__(self, pharmacophore, min_match_ratio=1.0, n_conformers=50,
                 point_tolerance=0.10, direction_tolerance=30.0):
        self.pharmacophore = pharmacophore
        self.min_match_ratio = float(min_match_ratio)
        self.point_tolerance = float(point_tolerance)
        self.direction_tolerance = float(direction_tolerance)
        self._conformer_generator = ConformerGenerator(n_conformers=n_conformers)
        self.matches = []

        # Pre-compute excluded volume data for speed
        self._ev_centers = []   # list of ndarray (3,) in nm
        self._ev_radii = []     # list of float in nm
        self._non_ev_sites = []
        for site in pharmacophore.interaction_sites:
            if 'excluded volume' in site.features:
                c = site.center
                r = site.radius
                if c is not None and r is not None:
                    self._ev_centers.append(puw.get_value(c, to_unit='nm'))
                    self._ev_radii.append(float(puw.get_value(r, to_unit='nm')))
            else:
                self._non_ev_sites.append(site)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _detect_features(self, mol, conf_id):
        """Detect LIGAND_SMARTS features in one conformer.

        Returns
        -------
        dict[str, list[ndarray]]
            Feature name → list of centroids in nm.
        """
        found = defaultdict(list)
        conf = mol.GetConformer(conf_id)
        for feat_name, patterns in LIGAND_SMARTS.items():
            for pattern in patterns:
                p = Chem.MolFromSmarts(pattern)
                if p is None:
                    continue
                for match in mol.GetSubstructMatches(p):
                    pts = [conf.GetAtomPosition(idx) for idx in match]
                    center_ang = np.mean([[pt.x, pt.y, pt.z] for pt in pts], axis=0)
                    found[feat_name].append(center_ang / 10.0)  # Å → nm
        return found

    def _site_center_and_radius(self, site):
        """Return (center_nm, radius_nm) for a site, or (None, None)."""
        center_q = site.center
        if center_q is not None:
            center_nm = puw.get_value(center_q, to_unit='nm')
        else:
            position_q = getattr(site.shape, 'position', None)
            if position_q is None:
                return None, None
            center_nm = puw.get_value(position_q, to_unit='nm')

        radius_q = site.radius
        radius_nm = (float(puw.get_value(radius_q, to_unit='nm'))
                     if radius_q is not None else self.point_tolerance)
        return center_nm, radius_nm

    def _direction_ok(self, site, feat_center_nm, center_nm):
        """Check angular tolerance for SphereAndVector sites.

        For directional sites the ligand feature centroid must lie roughly in
        the direction indicated by site.shape.direction relative to the site
        center. Returns True for non-directional sites unconditionally.
        """
        if site.shape_name != 'sphere and vector':
            return True
        direction = getattr(site.shape, 'direction', None)
        if direction is None:
            return True
        direction = np.asarray(direction, dtype=float)
        norm = np.linalg.norm(direction)
        if norm < 1e-6:
            return True
        direction = direction / norm

        # Vector from site center toward ligand feature
        ligand_vec = feat_center_nm - center_nm
        ligand_norm = np.linalg.norm(ligand_vec)
        if ligand_norm < 1e-6:
            return True  # coincident — accept
        ligand_vec = ligand_vec / ligand_norm

        cos_angle = np.clip(np.dot(direction, ligand_vec), -1.0, 1.0)
        angle_deg = np.degrees(np.arccos(cos_angle))
        return angle_deg <= self.direction_tolerance

    def _has_ev_clash(self, mol, conf_id):
        """Return True if any heavy atom clashes with an ExcludedVolumeSphere."""
        if not self._ev_centers:
            return False
        conf = mol.GetConformer(conf_id)
        for atom in mol.GetAtoms():
            if atom.GetAtomicNum() == 1:
                continue  # skip H
            pos = conf.GetAtomPosition(atom.GetIdx())
            atom_nm = np.array([pos.x, pos.y, pos.z]) / 10.0
            for ev_center, ev_radius in zip(self._ev_centers, self._ev_radii):
                if np.linalg.norm(atom_nm - ev_center) < ev_radius:
                    return True
        return False

    def _match_conformer(self, mol, conf_id):
        """Evaluate one conformer against the pharmacophore.

        Returns the Fit Value (float) if the molecule passes all criteria,
        otherwise None.
        """
        # Fast-reject: excluded volume clash
        if self._has_ev_clash(mol, conf_id):
            return None

        features = self._detect_features(mol, conf_id)

        total_weight = sum(s.weight for s in self._non_ev_sites)
        if total_weight == 0.0:
            return None

        essential_weight = sum(s.weight for s in self._non_ev_sites if s.essential)

        matched_weight = 0.0
        essential_matched = 0.0

        for site in self._non_ev_sites:
            center_nm, radius_nm = self._site_center_and_radius(site)
            if center_nm is None:
                continue

            matched = False
            for feat_name in site.features:
                for feat_center in features.get(feat_name, []):
                    dist = np.linalg.norm(feat_center - center_nm)
                    if dist <= radius_nm and self._direction_ok(site, feat_center, center_nm):
                        matched = True
                        break
                if matched:
                    break

            if matched:
                matched_weight += site.weight
                if site.essential:
                    essential_matched += site.weight

        # Reject if too few essential sites are matched
        if essential_weight > 0.0:
            if (essential_matched / essential_weight) < self.min_match_ratio:
                return None

        return matched_weight / total_weight

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @signal(tags=["screening", "run"])
    @arg_digest(type_check=True)
    def run(self, molecular_database, skip_digestion=False):
        """Screen a library of molecules against the pharmacophore.

        Parameters
        ----------
        molecular_database : iterable
            Molecular systems accepted by molsysmt (SMILES strings, RDKit Mol
            objects, molsysmt.MolSys, file paths, etc.).

        Returns
        -------
        list of dict
            Sorted by Fit Value (descending). Each entry contains:
            ``'mol'``, ``'fit_value'``, ``'conf_id'``, ``'rd_mol'``.
        """
        self.matches = []

        for mol_system in molecular_database:
            try:
                if isinstance(mol_system, Chem.Mol):
                    rd_mol = mol_system
                else:
                    rd_mol = msm.convert(mol_system, to_form='rdkit.Mol')
            except Exception:
                continue

            if rd_mol is None:
                continue

            if rd_mol.GetNumConformers() == 0:
                rd_mol = self._conformer_generator.generate(rd_mol)

            if rd_mol.GetNumConformers() == 0:
                continue

            best_fit = None
            best_conf = 0
            for conf_id in range(rd_mol.GetNumConformers()):
                fit = self._match_conformer(rd_mol, conf_id)
                if fit is not None and (best_fit is None or fit > best_fit):
                    best_fit = fit
                    best_conf = conf_id

            if best_fit is not None:
                self.matches.append({
                    'mol': mol_system,
                    'fit_value': best_fit,
                    'conf_id': best_conf,
                    'rd_mol': rd_mol,
                })

        self.matches.sort(key=lambda x: x['fit_value'], reverse=True)
        return self.matches

    def to_dataframe(self):
        """Return screening results as a pandas DataFrame.

        Columns: rank, fit_value, conf_id, smiles.
        """
        import pandas as pd
        rows = []
        for rank, entry in enumerate(self.matches, start=1):
            rd_mol = entry.get('rd_mol')
            smiles = (Chem.MolToSmiles(Chem.RemoveHs(rd_mol))
                      if rd_mol is not None else '')
            rows.append({
                'rank': rank,
                'fit_value': entry['fit_value'],
                'conf_id': entry['conf_id'],
                'smiles': smiles,
            })
        return pd.DataFrame(rows)

    def to_csv(self, file_name):
        """Write screening results to a CSV file.

        Parameters
        ----------
        file_name : str
            Output path.
        """
        self.to_dataframe().to_csv(file_name, index=False)

    def to_sdf(self, file_name):
        """Write the best-matching conformer of each hit to an SDF file.

        The ``FitValue`` property is embedded in each record.

        Parameters
        ----------
        file_name : str
            Output path.
        """
        from rdkit.Chem import SDWriter
        writer = SDWriter(file_name)
        for entry in self.matches:
            rd_mol = entry.get('rd_mol')
            if rd_mol is None:
                continue
            conf_id = entry['conf_id']
            mol_out = Chem.RWMol(rd_mol)
            mol_out = Chem.RemoveHs(mol_out)
            mol_out.SetDoubleProp('FitValue', entry['fit_value'])
            writer.write(mol_out, confId=conf_id)
        writer.close()
