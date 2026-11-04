# Prepared-ligand rigid search

**#63 molecular ranking:** choose `search_method='seeded_hit'` for the new
seed-only binary criterion, described in [its contract](seeded_ranking_workflow.md).
The `rigid_triplet_fit@1` sections below describe the direct compatibility default
`placed_and_triplets`; ranking its pose coverage now requires explicit
`score_method='checked_pose_coverage'` in the facade/retrospective consumers.

The native classical slice tracked in `uibcdf/pharmacophoremt#15` adds rigid
correspondence search to the [reference-ligand workflow](reference_ligand_workflow.md).
It composes independently usable tools: chemical extraction, correspondence
proposals, molecular alignment and placed-pose evaluation. Feature + Shape
remains the query representation; the search method adds its own explicit
requirements instead of imposing them on every future pharmacophoric method.

## Public tools and contracts

| Tool | Responsibility |
| --- | --- |
| `modeler.get_features()` | Participant recognition and geometry through MolSysMT |
| `screening.get_correspondences()` | Chemically compatible triplet proposals and bounded enumeration |
| `screening.align_to_pharmacophore()` | Compose public MolSysMT fitting/copy/get/set operations for a proposed mapping |
| `screening.PoseEvaluator` | Check placed geometry, essential sites, optional coverage and exclusion veto |
| `screening.RigidPoseSearch` | Search prepared rigid ligands and report checked results/failures |

`rigid_triplet_fit@1` requires three or more essential sites with non-collinear
centers. Triplets use distinct candidate records compatible with the query
feature vocabulary. Pair-distance differences must not exceed the sum of the
site matching tolerances. Point sites use `point_tolerance`. Zero-weight essential
sites still participate. Collinear center triplets are omitted. A different
method is needed for one/two-center queries or orientation-defined anchors;
those queries remain usable with the placed-pose evaluator.

Feature indices refer to the supplied `get_features()` inventory. Site indices
refer to the query interaction-site list. Reused inventories must come from the
same unchanged source, frame, chemical state and selection. Axis/metadata checks
cannot authenticate source identity or coordinate history.

The alignment tool uses native `molsysmt.native.Structures` point clouds of
selected molecular coordinates and pharmacophoric center anchors. MolSysMT's
`least_rmsd_fit()` computes and applies a proper rigid rotation/translation;
the resulting selected coordinates are installed with public `copy/get/set`
operations. No artificial molecular topology or local Kabsch implementation is
introduced. Unselected atoms and other frames retain their original data in the
copy. The input system is never modified. Prepared coordinates are interpreted
without periodic image reconstruction or cell fitting.

Alignment evidence records the source/target centers, paired site/feature/atom
indices, RMSD, fitted atom coordinates, provider/version and selected CPU/double
options. Physical arrays use PyUnitWizard QuantityRecords. MolSysMT owns its
internal kernel choice; these results do not claim an executed Rust or GPU kernel.

## Bounds, termination and scoring

`max_trials` bounds raw candidate triplet products, including rejected products.
`get_correspondences()` returns a bounded list and an explicit `complete` flag;
standalone callers may inspect incomplete proposals. The search tests the original
placement and evaluates each fitted seed with `PoseEvaluator`. A valid hit takes
priority over an inadmissible pose; weighted coverage ranks within each status,
and exact ties keep the earliest candidate deterministically.

A valid hit with fit one establishes the maximum possible coverage and stops
fitting further seeds. It remains valid even if proposal enumeration was truncated;
the result retains both the incomplete-enumeration flag and `optimal_fit_found`.
This termination does not optimize RMSD among equal-fit poses.

Without that demonstrated maximum, truncated enumeration raises
`PoseEvaluationError` at `search_budget`, caused by catalog diagnostic
`PHMT-E105`. Explicit `on_error='record'` retains a failed entry with no fit value.
Retrospective validation excludes it and reports the original class/input counts;
it never becomes a zero-valued decoy. Complete valid negatives report checked
coverage and `not_matched`. Provider failures retain their own cause and stage.
Angular checks declare an eight-float64-epsilon cosine comparison allowance
for normalization roundoff, preserving zero-angle source/rigid-transform
invariance. The independently tracked correction is `#16`.

Completion means enumeration of this discrete triplet-fit method. It does not
prove absence of every pose satisfying continuous unequal tolerances. No conformer
generation or torsional search occurs. The method's assumptions are separate from
the extensible scientific model and from future compute/execution choices.
The [prepared-conformer workflow](conformer_screening_workflow.md) composes this
search across explicit source frames and states, retaining per-frame evidence and
resolving a molecule score only when its failures permit that conclusion.

## Executable analytical example

This synthetic fixture exercises reference construction, displacement recovery and
retrospective ranking through public MolSysMT operations. Its disconnected chemical
fragments isolate known feature positions; it is not a biological benchmark.

```python
import molsysmt as msm
import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import RigidPoseSearch
from pharmacophoremt.validation.retrospective import RetrospectiveValidator

coordinates = np.array([
    [0, 0, 0], [0.15, 0, 0], [0.3, 0, 0],
    [0.1, 0.5, 0], [0, 0.5, 0], [0.3, 0.6, 0], [0.3, 0.5, 0],
    [0.05, 0.2, 0.7],
])
source = msm.convert(
    msm.convert('smiles:CCC.[2H]O.C=O.[NH4+]', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity([coordinates], 'nm'))
query = from_ligand(source, features=[
    'hydrophobicity', 'hb donor', 'hb acceptor', 'positive charge',
], radius='0.02 nm')
displaced = msm.structure.translate(
    source, translation=puw.quantity([[[2, 1, 3]]], 'nm'), in_place=False,
)
search = RigidPoseSearch(query, max_trials=10000)
result = search.evaluate(displaced)
assert result['status'] == 'matched' and result['fit_value'] == 1

reflected = msm.copy(source)
msm.set(reflected, coordinates=puw.quantity([coordinates * [1, 1, -1]], 'nm'))
report = RetrospectiveValidator(query, evaluator=search,
                               score_method='checked_pose_coverage').run(
    [displaced], [reflected],
)
assert report['AUC'] == report['BEDROC'] == 1
assert report['n_actives_found'] == 1
```

For an inspectable fitted molecular system, reuse the recorded correspondence:

```python
from pharmacophoremt.screening import align_to_pharmacophore

aligned = align_to_pharmacophore(
    displaced, query, result['alignment']['correspondence'],
)
placed_ligand = aligned['molecular_system']
```

Alternatively, read `aligned_atom_coordinates` through the public
`puw.QuantityRecord.from_dict(...).to_quantity()` handshake and use MolSysMT to
install them in a copy. Identity-placement results have `alignment=None`.

## Evidence and remaining work

The durable guard `tests/test_rigid_search.py` uses real MolSysMT public tools.
Controls cover proper-motion recovery, reflection and distortion negatives,
donor directions, aromatic planes/formal-charge groups, zero-weight essential
anchors, optional coverage, exclusion veto, source/other-atom/other-frame
preservation, units, bounded enumeration and provider/failure accounting.

Verification uses the same published pinned provider sources and existing
scientific environment as the other native slices. It does not qualify clean
wheels, the hosted matrix or biological-pilot enrichment. Legacy screening
continues to require migration; native rigid search is an explicit new route.

Prepared multi-conformer inputs, provider-supported conformer generation,
consensus, native pocket hypotheses and workflow/viewer adapters remain subsequent
classical steps. Profiling should guide acceleration after these reference
controls; no Rust/GPU/distributed PHMT implementation is claimed here.

On 2026-10-02, the complete local suite passed **98 tests** on Python 3.13.14,
including all eleven rigid-search/precision controls. The documented construction,
ranking and reusable-alignment examples were executed successfully. Verification
used MolSysMT source `4d490427e38c5836be82472348fdf61934442bda` and PyUnitWizard
source `2ffe1885675f47c76af03c08e51bc889a5e99a05` on PYTHONPATH, with
`python -m pytest --receptor=llm -p no:cacheprovider -p no:rerunfailures tests`.
The existing scientific environment supplied other dependencies. Ruff, generated
report indexes, three offline reporting tests and `git diff --check` also passed.

## Shared seed eligibility review — 2026-10-10

Distinct feature records do not necessarily have distinct spatial centers: a
donor and acceptor can refer to the same atom. Automatic proposal tools require
non-collinear represented centers on both axes. Their shared private criterion
subtracts an existing center before the relative NumPy rank check; mean-centering
can introduce roundoff that wrongly admits exactly co-located anchors at a
translated origin. This does not introduce a physical near-collinearity cutoff
or guarantee numerical conditioning below float64 representable resolution.

The guard `tests/test_correspondence_geometry.py` covers all four public proposal
routes, three origins, query order permutations, valid identity proposals and
complete empty degenerate candidates whose pair-distance tolerances independently
pass. Its 60 cases and the complete 680-test scientific suite pass on Python
3.14.7. The immutable result/producer identities and prepared EST recovery under
both refinement policies are retained in
`evidence/seed_eligibility_review_py314_summary.json` and its checksum-qualified
full archive. The reviewed resolution is uibcdf/pharmacophoremt#31.

This criterion belongs to pharmacophoric seed selection; molecular fit validation
and transformations remain MolSysMT responsibilities. The ownership audit in
uibcdf/pharmacophoremt#41 separately reproduces the same roundoff mechanism in
MolSysMT's public fit validator, reported as uibcdf/molsysmt#367. A caller can
supply a mapping directly to `align_to_pharmacophore()` without automatic seed
selection. The #31 guard therefore does not qualify arbitrary explicit mappings
or repair the provider contract. Keep that dependency explicit rather than add a
consumer molecular validator or import a private provider helper.

## Current prepared rigid source/API acceptance — 2026-11-03

#15 is resolved with its [archive](archive/native_rigid_pose_search.md) and
[new receipt](evidence/rigid_search_acceptance_20261103_summary.json). Clean receiving
1e00aca passes 68 fresh controls in 42.89 s (13 rigid search, 26 seeded scoring,
eight retrospective, 21 attribution), zero failures/errors/skips. Ten intentional
attribution-failure warnings retain their original logs/groups. No new full suite
is claimed. Existing source/frame/selection, angular/chemical, provider-error,
exclusion, score and accounting contracts remain guarded.

Fresh off/on prepared-input controls verify recovery and standalone provider tools.
Identity and fitted admissible coverage-one hits can prove the compatibility
maximum despite incomplete enumeration, retaining zero and one fitted seeds
respectively. An exclusion-vetoed fit at one is not an admissible maximum; without
one, incomplete work raises search_budget with PHMT-E105 cause. Complete negatives
retain checked scores. Explicit seed-only no-pose negatives retain fit_value=None,
pose_evaluated=False/no assignments and valid binary zero, distinguished by status
from failed searches. No initial-frame coverage is silently used as a molecular score.

| Control | Retained outcome | Completion/criterion evidence |
| --- | --- | --- |
| Valid supplied identity, one-product bound | matched, fit 1, no fit call | enumeration incomplete; optimal_fit_found |
| Valid ionic fitted seed, six-product bound | matched, fit 1, one fit | enumeration incomplete; optimal_fit_found |
| Unproven moved-source bound | failed, no fit value | search_budget caused by PHMT-E105 |
| Fully enumerated exclusion veto | not_matched, fit 1 | enumeration_complete, retained clashes |
| Truncated exclusion-vetoed work | failed, no fit value | no admissible maximum proof |
| Complete seed-only no-pose negative | not_matched, fit None, ranking 0 | enumeration complete; pose_evaluated=False |

The compatibility retrospective route explicitly selects checked_pose_coverage.
A full six-input analytical ranking retains repeated/generator identity, three
active hits and AUC/BEDROC one. A limited run preserves original classes 3/3,
failures at [1,3], evaluated indices [0,2,4,5] and scores [1,1,0,0]; two evaluated
inputs remain in each class. Failures never become scored negatives. JSON/YAML
read under changed unit policies retains metadata and reference/moved/negative
results (1/1/0). Molecular-domain fingerprints remain unchanged under each same
unit policy; off/on science agrees with actual credit 3 items/6 uses host-off and 13/50 host-on.

Both unchanged Python examples pass (13 items/50 uses); strict isolated original-page
rendering passes with three neighbor stubs. Full source/native/helper/test/input/
metadata identity remains stable in all three phases. An initial wrong-path
launcher never started tests/imports and is retained separately. No runtime/test/
input/provider/prefix/sibling change is needed. All molecular work remains public
MolSysMT calls; PHMT owns pharmacophoric proposal/pose/termination/scoring decisions.

This accepts the declared finite source/API method, not continuous/global pose
or conformational completeness, minimum-RMSD tie optimization, biology, affinity
or performance. #63's binary criterion remains independently declared. Clean
installed/public/platform/hosted #23/#10/#9, workspace #82 and #41 public/legacy
receiving (review 2026-11-11) remain separate. Earlier provider inspections and
future-work lists above retain their dated scope; prepared conformers, consensus
and refinement now have their own delivered/accepted contracts. Next accept #14's
reference-ligand route; #13/#19 retain their owning reviews. Owned resources remain
LMMV/dprada for review 2026-11-17.
