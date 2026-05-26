from argdigest import arg_digest
from smonitor import signal
import molsysmt as msm
import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor import InvalidInteractionSiteError

class Pharmacophore():

    """ Native object for pharmacophores.

    A pharmacophore is a set of interaction sites defining the necessary 3D 
    interaction requirements for a molecular system.

    Parameters
    ----------
    pharmacophore : :obj: (optional)
        File or object with pharmacophoric model. (Default: None)
    form : str (optional)
        Form of input pharmacophore: 'pharmer', 'ligandscout', 'rdkit', 'sdf', 'json', 'yaml'.
    name : str, optional
        Name of the pharmacophoric model.
    description : str, optional
        Short description of the model.
    molecular_system : :obj:`molsysmt.MolSys`, optional
        Molecular system linked to this pharmacophore.
    score : float, optional
        Score of the pharmacophore model.
    ref_mol : int, optional
        Index of the reference molecule.
    ref_struct : int, optional
        Index of the reference structure/frame.

    Attributes
    ----------
    name : str
        Name of the pharmacophoric model.
    description : str
        Short description of the model.
    interaction_sites : list of :obj:`pharmacophoremt.interaction_site.InteractionSite`
        List of interaction sites.
    n_interaction_sites : int
        Number of interaction sites.
    molecular_system : :obj:`molsysmt.MolSys`
        Molecular system linked to this pharmacophore.
    score : float
        Score of the pharmacophore model.
    ref_mol : int
        Index of the reference molecule.
    ref_struct : int
        Index of the reference structure/frame.
    """

    @signal(tags=["core", "pharmacophore", "init"])
    @arg_digest(type_check=True)
    def __init__(self, pharmacophore=None, form=None, name=None, description=None, 
                 molecular_system=None, score=None, ref_mol=None, ref_struct=None, 
                 skip_digestion=False):

        self.name = name
        self.description = description
        self.interaction_sites = []
        self.n_interaction_sites = 0
        self.molecular_system = molecular_system
        self.score = score
        self.ref_mol = ref_mol
        self.ref_struct = ref_struct
        self.metadata = {}

        if pharmacophore is not None:
            if form == 'pharmer':
                self.__from_pharmer(pharmacophore)
            elif form == 'ligandscout':
                self.__from_ligandscout(pharmacophore)
            elif form == 'rdkit':
                from pharmacophoremt.io import load_rdkit
                tmp = load_rdkit(pharmacophore)
                self._copy_from(tmp)
            elif form in ['json', 'yaml']:
                from pharmacophoremt.io import load_json, load_yaml
                tmp = load_json(pharmacophore) if form == 'json' else load_yaml(pharmacophore)
                self._copy_from(tmp)
            elif form == 'sdf':
                from pharmacophoremt.io import load_sdf
                tmp = load_sdf(pharmacophore)
                self._copy_from(tmp)
            else:
                raise NotImplementedError(f"Form {form} not supported in constructor.")

    def _copy_from(self, other):
        """Internal helper to copy attributes from another pharmacophore."""
        self.interaction_sites = other.interaction_sites
        self.n_interaction_sites = other.n_interaction_sites
        self.molecular_system = other.molecular_system
        self.name = other.name if other.name else self.name
        self.description = other.description if other.description else self.description

    def __reset(self):
        self.interaction_sites = []
        self.n_interaction_sites = 0

    @signal(tags=["core", "pharmacophore", "edit"])
    @arg_digest(type_check=True)
    def add_interaction_site(self, interaction_site, skip_digestion=False):
        """Add a new interaction site to the pharmacophore."""
        from pharmacophoremt.interaction_site.interaction_site import InteractionSite
        if not isinstance(interaction_site, InteractionSite):
            raise InvalidInteractionSiteError(reason="Object is not an InteractionSite instance")
        
        self.interaction_sites.append(interaction_site)
        self.n_interaction_sites += 1

    @signal(tags=["core", "pharmacophore", "edit"])
    @arg_digest(type_check=True)
    def remove_interaction_site(self, index, skip_digestion=False):
        """Remove an interaction site by its index."""
        self.interaction_sites.pop(index)
        self.n_interaction_sites -= 1

    @signal(tags=["core", "pharmacophore", "query"])
    @arg_digest(type_check=True)
    def get(self, selection='all', feature_name=None, shape_name=None, 
            get_center=False, get_radius=False, get_direction=False, 
            get_features=False, skip_digestion=False):
        """Flexible query method to extract information from interaction sites."""
        indices = range(self.n_interaction_sites) if selection == 'all' else selection
        subset = [self.interaction_sites[i] for i in indices]

        if feature_name is not None:
            subset = [s for s in subset if feature_name in s.features]
        if shape_name is not None:
            subset = [s for s in subset if s.shape_name == shape_name]

        output = []
        if get_center:
            centers = [puw.get_value(s.center, to_unit='nm') for s in subset]
            output.append(puw.quantity(np.array(centers), 'nm'))
        if get_radius:
            radii = [puw.get_value(s.radius, to_unit='nm') for s in subset]
            output.append(puw.quantity(np.array(radii), 'nm'))
        if get_direction:
            # Only some shapes have direction
            dirs = [puw.get_value(getattr(s.shape, 'direction', [0.0, 0.0, 0.0])) for s in subset]
            output.append(np.array(dirs))
        if get_features:
            output.append([s.features for s in subset])

        if len(output) == 0: return subset
        if len(output) == 1: return output[0]
        return tuple(output)

    @signal(tags=["core", "pharmacophore", "view"])
    @arg_digest(type_check=True)
    def add_to_molsysviewer(self, view, tag=None, skip_digestion=False):
        """Add the pharmacophore to a MolSysViewer instance using high-performance vectorization."""
        if self.n_interaction_sites == 0:
            return

        # 1. Extract data in bulk
        centers, radii, directions, features = self.get(
            get_center=True, get_radius=True, get_direction=True, get_features=True, 
            skip_digestion=True
        )
        
        # 2. Map features to MolSysViewer kinds (taking the primary feature)
        kinds = [f[0] for f in features]
        
        # 3. Send to Mol* engine via vectorized call
        # Using the new official RFC-001 API
        view.shapes.add_interaction_sites(
            centers=puw.get_value(centers, to_unit='angstroms'), 
            kinds=kinds,
            radii=puw.get_value(radii, to_unit='angstroms'),
            directions=directions,
            tag=tag,
            name=self.name
        )

    @signal(tags=["core", "pharmacophore", "query"])
    def get_distance_matrix(self):
        """Calculate the N x N distance matrix between interaction site centers."""
        if self.n_interaction_sites < 2:
            return puw.quantity(np.zeros((self.n_interaction_sites, self.n_interaction_sites)), 'nm')
        centers = self.get(get_center=True, skip_digestion=True)
        coords = puw.get_value(centers)
        diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
        dist = np.sqrt(np.sum(diff**2, axis=-1))
        return puw.quantity(dist, 'nm')

    @signal(tags=["core", "pharmacophore", "inspect"])
    def to_dataframe(self):
        """Convert the set of interaction sites to a Pandas DataFrame."""
        import pandas as pd
        data = []
        for i, site in enumerate(self.interaction_sites):
            data.append({
                'index': i,
                'features': site.features,
                'shape': site.shape_name,
                'center': site.center,
                'radius': site.radius,
            })
        return pd.DataFrame(data)

    # ------------------------------------------------------------------
    # Refinement API
    # ------------------------------------------------------------------

    @signal(tags=["core", "pharmacophore", "edit"])
    @arg_digest(type_check=True)
    def set_radius(self, index, radius, skip_digestion=False):
        """Set the radius of one interaction site.

        Parameters
        ----------
        index : int
            Index of the site to modify.
        radius : quantity
            New radius as a puw quantity (e.g. ``puw.quantity(0.2, 'nm')``).
        """
        from pharmacophoremt.interaction_site.shape import Sphere, SphereAndVector, GaussianKernel, Disk, Cylinder
        site = self.interaction_sites[index]
        shape = site.shape
        sname = shape.shape_name

        if sname == 'sphere':
            site.shape = Sphere(shape.center, radius, skip_digestion=True)
        elif sname == 'sphere and vector':
            site.shape = SphereAndVector(shape.center, radius, shape.direction, skip_digestion=True)
        elif sname == 'gaussian kernel':
            site.shape = GaussianKernel(shape.center, radius, skip_digestion=True)
        elif sname == 'disk':
            site.shape = Disk(shape.center, shape.normal, radius, skip_digestion=True)
        elif sname == 'cylinder':
            site.shape = Cylinder(shape.start, shape.end, radius, skip_digestion=True)
        else:
            raise NotImplementedError(f"set_radius not supported for shape '{sname}'")

    @signal(tags=["core", "pharmacophore", "edit"])
    @arg_digest(type_check=True)
    def set_essential(self, index, essential, skip_digestion=False):
        """Toggle the essential flag of one or all interaction sites.

        Parameters
        ----------
        index : int or 'all'
            Index of the site, or ``'all'`` to set all sites at once.
        essential : bool
            New essential value.
        """
        if index == 'all':
            for site in self.interaction_sites:
                site.essential = bool(essential)
        else:
            self.interaction_sites[int(index)].essential = bool(essential)

    def merge(self, other):
        """Return a new Pharmacophore combining sites from self and other.

        The merged pharmacophore takes the name and metadata of self. No
        deduplication is applied; call the modeler's merge helper if needed.

        Parameters
        ----------
        other : Pharmacophore

        Returns
        -------
        Pharmacophore
        """
        from pharmacophoremt.pharmacophore import Pharmacophore
        merged = Pharmacophore(name=self.name, description=self.description,
                               molecular_system=self.molecular_system)
        for site in self.interaction_sites + other.interaction_sites:
            merged.add_interaction_site(site, skip_digestion=True)
        return merged

    def similarity(self, other, tolerance_nm=0.15):
        """Compute Dice similarity between two pharmacophores.

        For each site in self, the best-matching site in other (same feature,
        minimum distance) is found. A pair is counted as matched when the
        centroid distance ≤ ``tolerance_nm``. The result is the Dice coefficient:

            similarity = 2 * |matched_pairs| / (N_self + N_other)

        Parameters
        ----------
        other : Pharmacophore
        tolerance_nm : float
            Maximum centroid distance for a site-match (default 0.15 nm = 1.5 Å).

        Returns
        -------
        float
            Dice similarity in [0, 1].
        """
        matched = 0
        used_other = set()

        for site in self.interaction_sites:
            if site.center is None:
                continue
            c_self = puw.get_value(site.center, to_unit='nm')
            best_dist = float('inf')
            best_j = None
            for j, o_site in enumerate(other.interaction_sites):
                if j in used_other:
                    continue
                if o_site.center is None:
                    continue
                if not set(site.features) & set(o_site.features):
                    continue
                dist = float(np.linalg.norm(c_self - puw.get_value(o_site.center, to_unit='nm')))
                if dist < best_dist:
                    best_dist = dist
                    best_j = j
            if best_j is not None and best_dist <= tolerance_nm:
                matched += 1
                used_other.add(best_j)

        n_self = self.n_interaction_sites
        n_other = other.n_interaction_sites
        if n_self + n_other == 0:
            return 0.0
        return 2.0 * matched / (n_self + n_other)

    def __repr__(self):
        name = getattr(self, 'name', 'unnamed')
        n_sites = getattr(self, 'n_interaction_sites', 0)
        return f"<Pharmacophore '{name}' with {n_sites} interaction sites>"

    def __from_pharmer(self, pharmacophore):
        from pharmacophoremt.io import from_pharmer as _from_pharmer
        tmp = _from_pharmer(pharmacophore)
        self._copy_from(tmp)

    def __from_ligandscout(self, pharmacophore):
        from pharmacophoremt.io import from_ligandscout as _from_ligandscout
        tmp = _from_ligandscout(pharmacophore)
        self._copy_from(tmp)
        
    @signal(tags=["core", "pharmacophore", "view"])
    @arg_digest(type_check=True)
    def add_to_NGLView(self, view, color_palette='pharmacophoremt', skip_digestion=False):
        for interaction_site in self.interaction_sites:
            interaction_site.add_to_NGLView(view, color_palette=color_palette)

    @signal(tags=["core", "pharmacophore", "view"])
    @arg_digest(type_check=True)
    def show(self, color_palette='pharmacophoremt', skip_digestion=False):
        if self.molecular_system is not None:
            view = msm.view(self.molecular_system, standardize=False)
            self.add_to_NGLView(view, color_palette=color_palette)
        else:
            from molsysviewer import MolSysView
            view = MolSysView()
            self.add_to_molsysviewer(view, skip_digestion=True)
        return view
