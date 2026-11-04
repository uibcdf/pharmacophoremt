# MolSysMT-backed placed-pose workflow

The first bounded workflow builds a pharmacophore from native MolSysMT
interaction observations and evaluates a molecular pose with existing
coordinates in that reference frame. Its owning issue is
`uibcdf/pharmacophoremt#13`; ranking and accounting corrections are tracked in
`uibcdf/pharmacophoremt#12`.

## Responsibilities and supported definitions

MolSysMT supplies molecular forms, coordinate frames, selections, source index
spaces, chemical states, participant recognition and interaction calculations.
PharmacophoreMT constructs pharmacophore geometry, assigns participants to query
sites and reports geometric coverage. Missing provider capabilities raise a
diagnostic; they do not trigger local chemistry implementations.

`pharmacophoremt.modeler.from_interactions()` consumes one evaluated frame of a
native `molsysmt.Interactions` result. `pharmacophoremt.model()` also exposes it
as `method='interaction-based'`, requiring `interactions` and `ligand_selection`.
The caller must supply the same unchanged source and local index space used in
the interaction calculation. Axis lengths and source labels cannot authenticate
molecular origin.

The initial extraction scope was atomic hydrophobic contacts and hydrogen bonds.
The [ionic continuation](ionic_interaction_workflow.md) under #33 now consumes
native ionic contacts through the shared public formal-charge feature tool.
The [aromatic continuation](aromatic_interaction_workflow.md) under #34 consumes
native pi-pi/cation-pi profiles through the shared feature inventory constructor,
with exact ring membership and explicit cation mapping alternatives.
The separate [reference-ligand workflow](reference_ligand_workflow.md), tracked
in `#14`, also extracts aromatic participants.
The [named analysis collection](interaction_composition_workflow.md) under #36
now calls these public adapters and composes compatible repeated participants,
retaining each original detector's criteria, references and local index scope.
Repeated observations of the same chemical participant contribute to one site.
Ligand donors become spheres with a donor-to-indexed-H direction; acceptors
become spheres without an invented lone-pair direction. Unsupported kinds,
uncovered frames, split donor-H or compound-charge selections and nonzero periodic image vectors
raise. A covered frame with no observations yields an empty model, which is not
a valid evaluation query.

`pharmacophoremt.screening.PoseEvaluator` uses MolSysMT's
`smarts_hydrophobic_atoms` and `smarts_donor_acceptor` definitions. These reproduce
the attributed ProLIF 2.2.2 recognition rules. ProLIF is a reference, while the
actual executed dependencies and versions come from MolSysMT's returned
metadata. Terminal methyl atoms do not automatically match the hydrophobic
definition. Hydrogen directions require an indexed source hydrogen; none is
added implicitly.

Extraction retains the upstream interaction's role definitions. Evaluation uses
the explicitly stated SMARTS recognition profile above. An upstream elemental
hydrogen-bond profile can recognize different candidates; its observations do
not guarantee a match under SMARTS recognition. This choice of chemical
definitions is a review point before broader workflow adoption.

The initial query supports Point, Sphere and donor SphereAndVector geometries, plus
heavy-atom included and spherical excluded volumes. Candidate features are
assigned one to one. All essential sites must match, including zero-weight
essential sites. Optional sites contribute their weight. Exclusion spheres veto
heavy atoms strictly inside their radius. Direction checks compare actual
donor-H vectors, including when the feature and query centers coincide.
Cosine comparisons include a declared float64 roundoff allowance, protecting
zero-angle source invariance (`#16`); it applies equally to aromatic normals.

Fit value is matched non-exclusion weight divided by total non-exclusion
weight. It is geometric coverage, not predicted affinity. A high fit value alone
does not establish a hit: essential requirements, exclusions and the configured
minimum fit value also determine `status`. Retrospective AUC, BEDROC and EF rank
coverage; `n_actives_found` separately counts the evaluator's accepted poses.

## Runnable analytical example

This disconnected pair of propanes is an analytical coordinate fixture. It is
not a prepared biological complex or an optimized conformer.

```python
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt.modeler import from_interactions
from pharmacophoremt.screening import PoseEvaluator
from pharmacophoremt.validation import RetrospectiveValidator

# Compose existing public MolSysMT conversion routes.
source = msm.convert(
    msm.convert('smiles:CCC.CCC', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=phmt.pyunitwizard.quantity([
    [[0, 0, 0], [.15, 0, 0], [.30, 0, 0],
     [0, .3, 0], [.15, .3, 0], [.30, .3, 0]],
], 'nm'))
observations = msm.interactions.hydrophobic.get_hydrophobic_interactions(
    source, selection=[0, 1, 2], selection_2=[3, 4, 5],
    selection_mode='between', structure_indices=[0], pbc=False,
)
query = from_interactions(source, observations, [0, 1, 2])
evaluator = PoseEvaluator(query)
result = evaluator.evaluate(source, selection=[0, 1, 2], pose_id='reference')
assert result['status'] == 'matched'
assert result['fit_value'] == 1.0
```

## Results, errors and physical boundaries

Each result carries the selected source atom/frame indices, chemical state,
assignments, missing essential sites, clashes, recognition metadata, criteria,
producer versions and detached provider bibliography. Each extracted site
retains its source participants, occurrence/relation indices, measurements and
evidence. Global provenance and site metadata survive native JSON/YAML export
and import. These records preserve observations; they do not automatically
constitute experimental Evidence in an orchestrator.

Lengths require quantities or strings with explicit units. Directions are finite
nonzero dimensionless vectors. Defaults state their units. Numeric calculations
convert explicitly to nm/degrees and preserve the caller's active PyUnitWizard
policy. New persistent distances, tolerances and provenance measurements use
PyUnitWizard QuantityRecords. The existing PHMT geometry format remains a fixed
nm/dimensionless compatibility schema, now with explicit `units` metadata;
older files without this field retain that convention. Other declared units
are rejected rather than silently reinterpreted.

`PoseEvaluator.evaluate()` raises `PHMT-E103` on a failed calculation and
retains the original cause. `run(..., on_error='record')` explicitly records
failures with `fit_value=None`, stage and cause. Repeated inputs retain separate
`input_index` values. A valid negative returns `status='not_matched'`.

For placed-pose validation, construct
`RetrospectiveValidator(query, evaluator=evaluator)` and pass `selection`,
`structure_index` or `chemical_state` through its `run()` method. Its default
error policy raises. Explicit recording excludes failed entries from ranking
and reports original counts, evaluated counts, failures and evaluated indices.
An entirely failed/empty batch raises. AUC and BEDROC are undefined (NaN) for
single-class evaluated datasets. Ties share ranking credit independently of
input order, avoiding optimistic EF when all scores are equal.

## Verification and release limits

The durable guards are `tests/test_pose_evaluation.py`,
`tests/test_retrospective.py`, `tests/test_validation_metrics.py` and
`tests/test_contracts.py`. They cover analytical positives/negatives, shared
rigid transforms, nm/angstrom and radian/degree policies, real MolSysMT hydrogen
bond/hydrophobic observations, unique assignment, essential sites, exclusions,
provenance, invalid inputs, optional-viewer absence and independent RDKit metric
references. They use public fixtures and no private pilot results.

The controlled CI source route is pinned to the published MolSysMT review
snapshot `4d490427e38c5836be82472348fdf61934442bda` and PyUnitWizard
`2ffe1885675f47c76af03c08e51bc889a5e99a05`. These supply experimental interaction
and QuantityRecord capabilities; a stable published dependency closure has not
been established. Local verification of exported pinned Python source trees
uses the existing scientific environment and does not establish clean wheel
builds or the hosted Python/OS matrix. Source-only support packages continue to
use the controlled pip route in test environments; production distribution
remains under `uibcdf/pharmacophoremt#10`.

On 2026-10-02, the complete local suite passed **80 tests** on Python 3.13.14
with those two exported source snapshots on PYTHONPATH. The command was
`python -m pytest --receptor=llm -p no:cacheprovider -p no:rerunfailures tests`.
The existing scientific environment supplied the remaining dependencies.
Ruff, the report index check, `git diff --check` and the three offline reporting
tests also passed. No commit, wheel build or hosted CI result is claimed.

**2026-10-10 qualification:** #18/#42/#44/#45 have since transitioned the
ligand/complex/structure modelers and screening facade to explicit prepared-native
tools. Retrospective validation requires an evaluator and has no legacy fallback;
see [the screening contract](virtual_screening_workflow.md). Unused molecular
utilities and native donor geometry remain #41 work. The dated measurements
above retain their original scope. New molecular operations belong in MolSysMT.

The [bounded rigid-search route](rigid_search_workflow.md) now supplies native
correspondence/alignment for prepared ligands (`#15`). Conformer generation, additional interaction families,
ensemble consensus, application-level Ackredit participation and docking/pocket
workflow adapters are subsequent work. Scientific acceptance for a biological
pilot requires its own independent controls after these contracts are agreed.

## Current placed-observation source/API acceptance — 2026-11-03

#13 is resolved with its [archive](archive/molsysmt_placed_pose_workflow.md) and
[receipt](evidence/placed_pose_acceptance_20261103_summary.json). Clean receiving
1eea04d passes 99 fresh controls in 16.66 s (14 pose, eight retrospective, 44 metric,
18 contract, 15 observed donor geometry), zero failures/errors/skips/warnings.
Real public MolSysMT controls cover current native observations and provider-vector
receiving. No new full suite or library/test/provider change is claimed.

Fresh host-off/on capsules preserve two hydrophobic observations in one site and
two donor observations in one directed site or two opposite-side acceptor spheres.
Local/source pair [1,0]/[21,20], frame 1 and declared structure sources [4,7] stay
explicit; labels do not authenticate source identity. Direct/dispatcher queries
agree; source/displaced scores are 1/0 and shared MolSysMT rigid motion preserves
the matched result. Wrong frame/donor direction rejects. One-to-one zero-weight
essential and steric veto controls both yield not_matched despite coverage one.
Essential priority, optional weighted coverage and explicit minimum-fit criteria
retain distinct effects. Covered-empty models and failed conversions/calculations
are separate; unsupported kinds and nonzero images are deliberate record controls.

The batch/facade preserves all input identities, negatives and source-stage failures
without a fabricated score. Analytical retrospective original classes 3/2, failures
[0,4], evaluated [1,2,3] and scores [1,1,0] produce AUC/BEDROC one. Six JSON/YAML
round trips per profile preserve metadata/constraints and physical geometry to
1e-12 across pm/fs/degrees and angstrom/ps/radians. Source domains and cached
observations remain unchanged. Off/on science agrees; actual capture is 3 items/
12 uses off and 12/43 on.

The chemical-profile review is settled for this API: extraction preserves upstream
roles, while evaluation independently uses the stated SMARTS definition. A caller-
declared explicit C-H donor geometric observation converts to a query but produces
a valid zero-coverage negative under smarts_donor_acceptor. No conventional C-H
hydrogen-bond claim, chemical repair or guarantee that observed roles match follows.
The original outputs retain both definitions and original attribution (4 items/
5 uses off; 12/22 on), so mismatches cannot silently become recognition equivalence.

The unchanged documented block passes (11 items/23 uses); strict isolated original-
page rendering passes with six neighbor stubs. Full identities stay stable across
four phases. The supplementary script's initial wrong recognition lookup key and
its correction are retained without runtime changes. Historical dependency pins,
80-test run and future-work lists above keep their dated scope; native modeler/
screening transitions and additional families/consensus now have separate delivered
contracts. The facade requires explicit method choice and does no local preparation.

MolSysMT owns molecular work. #41 public/floor/installed receiving and final
historical donor-absence retirement remain partial (review 2026-11-11); ideal
acceptor #375 remains independent. These are prepared-source analytical/API controls,
not biological, performance, clean installed/public/platform or hosted acceptance.
#23/#10/#9 and workspace #82 retain their gates. Next review #19's optional
attribution contract without promoting local source evidence into delivered-package/
all-minor public receiving. Temporary resources: LMMV/dprada, review 2026-11-17.
