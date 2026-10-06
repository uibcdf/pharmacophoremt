# Native reference-ligand workflow

The next classical slice, tracked in `uibcdf/pharmacophoremt#14`, builds a query
from a prepared reference ligand and evaluates existing poses in its frame.
It complements the [observed-complex route](placed_pose_workflow.md). Both
consume public MolSysMT chemistry; neither is a free conformational search.

## Public tools and chemical definition

`modeler.get_features()` is independently usable. It returns local participant
and geometry atom indices, explicit-unit centers, donor directions, aromatic
normals, formal charges, and detached provider evidence. `modeler.from_ligand()`
turns that inventory into an editable query. `model(method='reference-ligand')`
exposes the same construction, using `ligand_selection` when needed.
`screening.PoseEvaluator` calls the same extraction tool.

The explicit definition is `classical_atomic_formal@1`:

| Family | MolSysMT provider | Query geometry |
| --- | --- | --- |
| Hydrophobicity | `get_hydrophobic_sites(method='smarts_hydrophobic_atoms')` | Atomic sphere |
| H-bond donor | `get_hbond_sites(method='smarts_donor_acceptor')` | Donor-centered sphere and indexed donor-H direction |
| H-bond acceptor | Same hydrogen-bond provider | Atomic sphere, no inferred lone-pair direction |
| Aromatic ring | `get_aromatic_rings()` and `get_least_squares_plane()` | Disk centered on the fitted plane with its normal |
| Positive/negative charge | `get_charge_centers()` and `get_center()` | Sphere at the uniform centroid of geometry members |

Names refer to `molsysmt.physchem` for chemical tools and `molsysmt.structure`
for geometry tools. Aromatic membership uses the provider's stored-aromatic-bond
minimum cycle basis, not a universal ring definition. Formal charges are declared
chemical-state charges, not inferred ionization at a chosen pH. For carboxylates,
the provider identifies the whole charged group and uses its two oxygens for
geometry. Split rings/charge groups raise provider diagnostics. Ring planarity
residuals and source chemical-state evidence remain in recognition metadata.

All generated sites start essential and equally weighted. These defaults are
a reference hypothesis for curation, not an assertion that every feature binds.
No participant found for the requested families raises an argument diagnostic.

## Matching contract

Points and spheres bound participant-center distance. Donor directed spheres
also bound the donor-H angle. Aromatic disks bound center distance by their
radius and the *unoriented* normal angle by `direction_tolerance`: reversing a
normal leaves the physical plane unchanged. This profile compares ring centers
and axes; it does not calculate point-in-disk intersections or disk thickness.
Aromatic spheres/points intentionally omit the orientation constraint.

The existing `essential_then_weighted_one_to_one@1` assignment strategy and
exclusion veto still apply. A charge participant matches only its sign. Results
record the chemical definition, geometric criteria, assignment method and actual
NumPy/SciPy CPU versions/precision. This is a specific classical strategy; future
logical constraints or scoring methods must declare their own contracts.

## Executable analytical example

The following example creates a public synthetic fixture through MolSysMT.
Real workflows should supply prepared experimental structures instead.

```python
import molsysmt as msm
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import PoseEvaluator
from pharmacophoremt.validation.retrospective import RetrospectiveValidator

source = msm.convert(
    msm.convert('smiles:CCC', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity(
    [[[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]]], 'nm',
))
query = from_ligand(source, features=['hydrophobicity'])
evaluator = PoseEvaluator(query)
positive = evaluator.evaluate(source)
displaced = msm.structure.translate(
    source, translation=puw.quantity([[[2, 0, 0]]], 'nm'), in_place=False,
)
report = RetrospectiveValidator(query, evaluator=evaluator).run(
    [source], [displaced],
)
assert positive['status'] == 'matched'
assert report['scores'].tolist() == [1, 0]
assert report['AUC'] == report['BEDROC'] == 1
```

This demonstrates geometric controls and failure accounting, not biological
enrichment. The durable guard `tests/test_reference_ligand.py` additionally covers
all six families together, sign-sensitive charge matching, provider-derived group
centroids, orthogonal aromatic negatives, normal sign invariance, shared rigid
transforms, nm/angstrom and degree policies, source-coordinate preservation,
degenerate geometry, split selections and native JSON persistence.

## Remaining classical work

Prepared coordinates, chemically declared bond orders/aromaticity/charges and
explicit donor hydrogens remain inputs. The [bounded rigid-search route](rigid_search_workflow.md) now supplies separate
correspondence/alignment tools. The [prepared-conformer route](conformer_screening_workflow.md)
now composes those tools over requested MolSysMT frames. Conformer preparation,
multi-ligand consensus and the native pocket-based route remain separate steps.
Their molecular transformations and preparation
belong in MolSysMT; provider gaps must be resolved there. Legacy modelers retain
local molecular operations and remain migration work.

Verification uses the pinned provider source snapshots described in
[placed_pose_workflow.md](placed_pose_workflow.md#verification-and-release-limits),
with the existing scientific environment supplying other dependencies. Local
tests do not establish published-wheel, hosted-matrix or biological-pilot success.

On 2026-10-02, the complete suite passed **87 tests** on Python 3.13.14 using
those pinned MolSysMT/PyUnitWizard source snapshots on PYTHONPATH and
`python -m pytest --receptor=llm -p no:cacheprovider -p no:rerunfailures tests`.
All seven reference-ligand controls passed, and the example above was executed
separately with its assertions intact. Ruff, the generated-report index check,
the three offline reporting tests and `git diff --check` also passed.
