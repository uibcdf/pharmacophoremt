# Audit the observed receptor before detecting interactions

The [observed EST hydrogen recipe](observed_est_hydrogens.md) prepares an isolated
ligand. Its receptor needs a separate chemical assessment before building a
complex-based hypothesis. This recipe audits the deposited 1QKU asymmetric unit
through public MolSysMT tools; receptor preparation remains a subsequent step.

Run from this source checkout in the compatible development environment. The
retained mmCIF is checksum-qualified by the fixture manifest. It contains three
protein copies, three EST molecules and water. The chosen receptor is **label
chain A**, and its observed ligand is **label chain D**. Both have author chain A
in the deposition: label and author identifiers are different domains. Other
protein copies and water are excluded from this receptor scope. No symmetry mate
or bioassembly is constructed.

## Separate heavy-atom coverage from chemical readiness

```python
import molsysmt as msm
from devtools.prepare_eralpha_ligand import SOURCES, load_manifest

manifest = load_manifest()
source = msm.convert(str(SOURCES / '1qku.cif'), to_form='molsysmt.MolSys')
receptor_selection = 'molecule_type == "protein" and chain_id == "A"'
ligand_selection = manifest['source_selection']
receptor = msm.build.get_residue_chemical_coverage(
    source, selection=receptor_selection, structure_indices=0,
)
shell_selection = (
    f'({receptor_selection}) within 0.5 nm without pbc of ({ligand_selection})'
)
groups = msm.select(source, selection=shell_selection, element='group')
# Numeric selections in this tool are GROUP indices, not atom indices.
shell = msm.build.get_residue_chemical_coverage(
    source, selection=groups, structure_indices=0,
)
assert receptor['summary'] == {'assessed': 247, 'incomplete': 3, 'unassessed': 0}
assert shell['summary'] == {'assessed': 19, 'incomplete': 0, 'unassessed': 0}
chemistry = shell['chemical_readiness']
assert chemistry['fields']['formal_charge']['status'] == 'missing'
assert chemistry['fields']['atom_is_aromatic']['status'] == 'missing'
assert len(chemistry['explicit_hydrogen_atom_indices']) == 0
assert chemistry['connectivity']['declared_completeness'] == 'partial'
```

`assessed` means the bounded residue comparison ran; it does not certify chemical
validity. The three heavy-atom gaps are SER301 OG and LYS302/LYS303 CG, CD, CE and
NZ. All are outside the tested ligand shells. At 0.4/0.5/0.6 nm the shell contains
12/19/23 whole residues, each without a reported heavy-atom gap. These radii define
inspection scopes, not interaction criteria or a validated binding-site boundary.

The current standard-residue reference database lacks bond orders, so its order
comparison remains unassessed. Protonation, hydrogen expectations, valence,
conformer quality and complete reference-sequence coverage remain separate
questions. Missing OXT is not automatically a gap without terminal context.
Restricting the spatial scope does not complete chemistry.

## Preserve the actual calculation gate

```python
from pharmacophoremt.modeler import get_features

calculations = {
    'receptor_features': lambda: get_features(
        msm.extract(source, selection=receptor_selection)
    ),
    'hydrophobic': lambda: msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source, selection=receptor_selection, selection_2=ligand_selection,
        selection_mode='between', structure_indices=[0], pbc=False,
        method='atom_pair_distance', profile='smarts_hydrophobic_atoms',
        distance_threshold='0.45 nm',
    ),
    'hbonds': lambda: msm.interactions.hbonds.get_hbonds(
        source, selection=receptor_selection, selection_2=ligand_selection,
        selection_mode='between', structure_indices=[0], pbc=False,
        method='prolif', distance_threshold='0.35 nm', angle_threshold='130 degrees',
    ),
}
gates = {}
for name, calculate in calculations.items():
    try:
        calculate()
    except msm.StructuralInconsistencyError as error:
        gates[name] = {'status': 'blocked', 'code': error.code, 'n_observations': None}
assert len(gates) == 3
assert all(g['code'] == 'MSM-ERR-STRUCT-003' for g in gates.values())
```

These are requested profiles and cutoffs; the chemical gate prevents successful
evaluation. A blocked calculation cannot become zero interactions, an empty
pharmacophore or a negative pose score. An attempted call does not establish a
successful method citation.

Full-source detectors recognize chemistry before filtering participants. This
source still contains the raw ligand and other unprepared copies; the separately
prepared EST has not been inserted into it. The receptor-only feature call
establishes a receptor gate too. Ligand readiness alone cannot qualify the complex.

## Retain evidence and credit the data actually used

```python
import json
import ackredit
import pharmacophoremt as phmt
from devtools.audit_eralpha_receptor import audit
from devtools.prepare_eralpha_ligand import credit_inputs
from devtools.validate_eralpha_template import portable

with ackredit.session('1QKU receptor coverage'), phmt.attribution(True):
    with ackredit.capture('coverage audit with blocked detectors') as capture:
        report = portable(audit(source))
        credit_inputs(roles=('observed',))
    evidence = {'audit': report, 'attribution': capture.attribution.to_dict()}
assert report['source_unchanged']
assert len(evidence['attribution']['items']) == 1
assert evidence['attribution']['items'][0]['type'] == 'dataset'
serialized = json.dumps(evidence, allow_nan=False)
bibliography = ackredit.Attribution.from_dict(
    evidence['attribution']
).report(format='bibtex')
assert '1QKU' in bibliography
```

The application credits the observed entry. No chemical template or H-generation
method runs here. Portable attribution stays beside the original provider reports;
loading or rendering it does not execute another calculation.

The case driver retains the receptor and three shell reports, source mappings,
actual diagnostics, source preservation checks, dependency/source/extension
identities and off/on tracking comparison:

```bash
python -m devtools.audit_eralpha_receptor --output /tmp/receptor-audit.json
```

[Retained evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/README.md)
and the [acceptance record](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/eralpha_validation.md)
belong to
[PharmacophoreMT #22](https://github.com/uibcdf/pharmacophoremt/issues/22).
The provider preparation contract is discussed in
[MolSysMT #298](https://github.com/uibcdf/molsysmt/issues/298): residue/terminal
chemical templates, explicit protonation choices, inter-residue connectivity,
conflict/coverage reports and source correspondence. Preparation and complex
assembly remain molecular provider operations. Successful detectors must retain
criteria, evaluated coverage, measurements and actual citations before their
observations can feed `from_interactions()`.
