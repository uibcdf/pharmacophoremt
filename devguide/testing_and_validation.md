# Testing and scientific validation

Reviewed 2026-11-06 for onboarding. The [capability inventory](capability_inventory.md)
identifies implemented APIs; the [validation collection](validation_collection.md)
governs evidence. Historical results retain their producer and environment.
Passing software controls does not establish experimental predictive accuracy.

## Select the verification scope

| Scope | Evidence | Starting point |
| --- | --- | --- |
| Reporting/archive integrity | Issue records, indexes and original bytes | Commands below; [reporting protocol](reporting_protocol.md) |
| Selected source controls | Exercised code and actual provider combination | Tests linked from the capability inventory |
| Complete source qualification | Applicable complete suite on supported environments | [CI workflow](../.github/workflows/CI.yaml), #9/#23 |
| Installed/public delivery | Exact distributed file and dependency closure | [Release readiness](release_0_5_0_readiness.md), #10/#23/#95 |
| Scientific study | Declared inputs, labels, comparisons and uncertainty | Owning protocol and original evidence |

For documentation/report changes, run from the repository root:

```bash
python -B devtools/devguide_index.py --check
python -B -m unittest discover -s tests -p test_reporting_protocol.py
python -B -m unittest discover -s tests -p test_evidence_archive.py
git diff --check
```

After changing a queued report, first regenerate indexes with
`python -B devtools/devguide_index.py`. Archive checks do not execute science or
certify its conclusions. For Sphinx builds, follow the
[documentation contributor guide](../docs/README.md); notebook execution is off.

In a qualified Python 3.14 development environment, a focused selection is:

```bash
python -m pytest --receptor=llm tests/test_validation_metrics.py tests/test_retrospective.py
```

Select other tests by changed code, inputs and provider boundaries. Check actual
import origins and the matching dependency context first. The
[environment guide](../devtools/conda-envs/README.md) distinguishes ordinary,
controlled-source and public-provider routes. A justified optional-provider skip
does not satisfy its designated installed gate.

The complete source command is `python -m pytest --receptor=llm`; it requires
the complete selected dependency route and sufficient resources. Follow root
shared-workstation instructions: serial heavy phases, one allowed CPU/backend
thread, bounded memory and low priority. Select an available CPU on the new
machine and verify enforcement; do not copy CPU19 from an old receipt. Interrupted
or resource-limited attempts remain incomplete. Retain recovery under #9 rather
than increasing limits or presenting selected controls as a full-suite pass.

## Software and numerical controls

Use independent expected values and relevant positive, negative, degenerate and
failure cases. Existing modules are starting points, not a list of missing code:

| Boundary | Preserve | Starting controls |
| --- | --- | --- |
| Ligand consensus | Explicit native method, prepared inputs, distinct support, budgets and empty/failed distinction | [Ligand facade](../tests/test_ligand_based_facade.py), [rigid consensus](../tests/test_rigid_consensus.py) |
| Receptor projections | Complementary kinds, direction/frame/unit custody, exclusions and provider ownership | [Projections](../tests/test_receptor_projections.py), [aromatic-N receiving](public_cached_aromatic_n_generation.md) |
| Complex facade | Explicit cached observations/selection, same-source/frame coverage and failures | [Complex facade](../tests/test_complex_based_facade.py), [ERalpha interface](../tests/test_eralpha_interface.py) |
| Screening/ranking | Known geometric answers, valid zero/negative results, ties, budgets and failed-input accounting | [Pose evaluation](../tests/test_pose_evaluation.py), [rigid search](../tests/test_rigid_search.py), [virtual screening](../tests/test_virtual_screening.py) |
| Persistence | Declared field/schema fidelity and unsupported cases | [Native schema](native_schema.md), [fidelity matrix](persistence_fidelity.md) |
| Retrospective reporting | Original/evaluable counts, labels/scores, settings and failures | [Result contract](retrospective_result_contracts.md), [metric controls](../tests/test_validation_metrics.py) |

Test translation/rotation covariance of sites and invariance of relevant
distances, angles, matching and scores. Check equivalent physical units at
declared boundaries. Tolerances belong to the operation and quantity; one global
coordinate/angle tolerance cannot qualify every serializer or method. MolSysMT
owns molecular transforms and inspection; PHMT owns pharmacophore interpretation.

Assert independently known answers for analytical controls. Do not require every
real active to outrank every weak compound or update baselines merely to obtain
a green test. Changed scientific answers require investigation and an owning
issue. Format availability does not establish lossless support for every shape,
constraint, provenance field or molecular reference.

## Current scientific evaluation APIs

Actual exports are `validation.enrichment_factor`, `roc_auc`, `bedroc`,
`RetrospectiveValidator` and `LeaveOneOutValidator`; see the
[module exports](../pharmacophoremt/validation/__init__.py) and capability inventory.
Earlier `compute_*`, `validate_loo` and `load_benchmark` names in this document
were implementation sketches, not supported API instructions.

Scores rank higher first and must be finite; binary labels are explicit study
inputs. Native EF uses `ceil(fraction * N)` with shared credit at boundary ties.
AUC gives half credit to tied active/weak pairs. AUC/BEDROC return NaN when the
required class comparison is undefined. Declare score direction, fractions,
BEDROC alpha and ties before evaluation. The
[metric implementation](../pharmacophoremt/validation/metrics.py) and its controls
own exact definitions and edge cases.

LOO rebuilds from prepared inputs, requires an explicit evaluator factory and
selects the first native hypothesis. Its recall measures self-consistency; it
does not alone demonstrate generalization or supply a negative comparison.
Conformers, states and observations from one ligand are not independent examples.
Declare grouping and model selection before predictive claims.

For each study, qualify original assay methods, label/censoring semantics,
provenance/rights, molecular/series overlap, preparation assumptions, comparisons,
finite budgets and uncertainty. Keep tuning separate from evaluation. Report
original/evaluated denominators, valid negative scores and unscored failures;
failed calculations are not inactivity. Identity/scaffold/state work belongs to
MolSysMT.

No universal LOO-recall, EF or AUC cutoff defines a scientifically valid study or
successful library. Compare with a declared baseline and quantify uncertainty;
retain negative/inconclusive results. Property-matched decoys are not automatically
experimentally inactive, and a fixed active:decoy ratio is not a universal design.
Select comparators for the scientific question and explain the resulting limits.

## Current studies and future work

The [ERalpha review](receptor_validation_evidence_review.md) separates geometric/
preparation controls, the earlier cellular ligand-reference cohort and unqualified
binding sources under #66. The [first-study protocol](receptor_study1_admission_protocol.md)
and [BRD4 admission record](pending_proposals/qualify_brd4_second_receptor_study.md)
retain distinct gates. Both full studies under #103 are unfinished; follow the
[checkpoint](checkpoint.md). Existing ERalpha, DHFR and thrombin files/notebooks
are not an automatically admitted active/decoy benchmark collection.

Use the [case template](templates/evidence_case.md), retaining original inputs,
executable code, measured results, source/native identities and actual attribution.
Reading an archive differs from reexecuting science on new providers. Larger
workflows are opt-in and preserve failed/partial attempts.

Dynamics/MSM, specialized covalent/peptide/water methods and AI validation remain
future work. They will need their own questions, numerical controls and study
protocols when implemented; present receptor/software controls do not qualify them.
