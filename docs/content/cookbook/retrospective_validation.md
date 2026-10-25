# Validate a labeled set and inspect failures

Use `RetrospectiveValidator` with an explicit native evaluator to rank labeled
inputs and report coverage metrics, accepted hits and failed calculations.
Choose `PoseEvaluator` for existing placements, `RigidPoseSearch` for one prepared
frame, or `ConformerScreening` for each molecule's requested prepared frames.

## Executable example

The reference propane matches; its displaced copy is a valid negative for a
placed-pose evaluator. A molecule without coordinates illustrates a calculation
failure. This analytical fixture verifies accounting, not biological enrichment.

```python
import molsysmt as msm
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import PoseEvaluator
from pharmacophoremt.validation import RetrospectiveValidator

source = msm.convert(
    msm.convert('smiles:CCC', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity(
    [[[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]]], 'nm'))
query = from_ligand(source, features=['hydrophobicity'], radius='0.10 nm')
displaced = msm.structure.translate(
    source, translation=puw.quantity([[[2, 0, 0]]], 'nm'), in_place=False,
)
missing_coordinates = msm.convert(
    msm.convert('smiles:CCC', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)

validator = RetrospectiveValidator(query, evaluator=PoseEvaluator(query))
report = validator.run(
    (item for item in [source]),
    (item for item in [displaced, missing_coordinates]),
    on_error='record',
)
assert report['n_actives'] == 1 and report['n_decoys'] == 2
assert report['n_evaluated'] == 2 and report['n_failed'] == 1
assert report['n_actives_found'] == 1
assert report['evaluated_indices'].tolist() == [0, 1]
assert report['scores'].tolist() == [1, 0]
assert report['AUC'] == report['BEDROC'] == 1
assert report['failures'][0]['input_index'] == 2
assert report['failures'][0]['fit_value'] is None
```

## Understand the report

| Field | Meaning |
| --- | --- |
| `n_actives`, `n_decoys` | Original input counts |
| `n_evaluated`, `n_failed` | Resolved inputs and excluded calculation failures |
| `n_actives_evaluated`, `n_decoys_evaluated` | Class counts actually entering metrics |
| `n_actives_found` | Evaluated actives accepted by the chosen native tool |
| `scores`, `labels`, `evaluated_indices` | Coverage scores, labels and original input positions used in metrics |
| `evaluations`, `failures` | Per-input evidence and failed entries |
| `AUC`, `BEDROC`, `EF@1%`, `EF@5%`, `EF@10%` | Coverage-ranking metrics with tie handling |

Coverage ranks the inputs; a high score alone does not establish an accepted hit
or predicted affinity. Ties share ranking credit instead of receiving credit
from favorable input order. Use `ef_fractions` and `bedroc_alpha` to configure
the metric parameters explicitly.

Default failures raise. Explicit recording excludes failures from metric inputs
and preserves their identity and diagnostic evidence. The resulting metrics
describe the evaluated subset, so inspect failures and class counts alongside
the scores. A batch with no successfully evaluated inputs raises. AUC and BEDROC
are NaN when only one class remains in the evaluated subset.

## Verified ranking conventions

For a balanced four-input set with distinct descending scores, a perfect
ranking gives AUC and BEDROC 1; its reversal gives 0. Alternating active/decoy
labels give AUC 0.75. Untied analytical rankings are checked against
[RDKit's public scoring functions](https://www.rdkit.org/docs/source/rdkit.ML.Scoring.Scoring.html).
Reference lists are supplied in descending score order.

EF uses `ceil(fraction * n_evaluated)` entries. A tie at the cutoff receives
fractional active credit; BEDROC averages exponential positional weights within
each tie group. These conventions preserve results under input permutation.
The original dataset counts remain in the report, while class prevalence and
metrics use the successfully evaluated subset. Failures in either class can
change that subset, so retain the failures alongside the reported metrics.

Accepted-hit counts use the native evaluator's `status`. A pose with complete
positive coverage and an exclusion clash can have score 1 and still contribute
zero accepted hits. An explicit evaluator is required; the legacy fallback and
partial-essential threshold are retired. An empty or entirely failed dataset raises rather
than returning manufactured zero metrics.

## Use prepared-conformer screening

Pass `evaluator=ConformerScreening(query)` for the
[prepared-conformer workflow](prepared_conformers.md), with its three-essential-
non-collinear-center query requirement. Supply `structure_indices` and
`chemical_state` to `validator.run()`; they are forwarded to the native tool.
For placed evaluation or single-frame rigid search, use `structure_index` instead.

The conformer route contributes one resolved score per molecule, rather than
one metric input per frame. An unresolved ensemble appears in `failures` with
its per-frame evidence. A proven unit-fit hit can remain evaluated despite
other failed frames; inspect `entry['ensemble']['n_failed']` and
`entry['conformers']` in `evaluations`. Failed-molecule and failed-frame counts
therefore need not coincide. Labels, curation and benchmark preparation remain
your scientific choices; these recipes do not establish biological validation.

## Summarize saved results against the original cohort

`summarize_screening_results` reads detached native results and recomputes metrics
without molecular access or another search. Supply every original sample and its
label, an explicit mapping from native batch indices, and a cause for every input
that could not reach the native tool. Molecular preparation remains in MolSysMT.

```python
from pharmacophoremt.validation import summarize_screening_results

summary = summarize_screening_results(
    cohort=[
        {'input_index': 10, 'label': 1, 'source_id': 'active-A'},
        {'input_index': 20, 'label': 0, 'source_id': 'inactive-B'},
        {'input_index': 30, 'label': 1, 'source_id': 'unavailable-C'},
    ],
    evaluations=saved_native_batch,  # native input_index 0 and 1
    input_mapping=[
        {'native_input_index': 0, 'input_index': 10},
        {'native_input_index': 1, 'input_index': 20},
    ],
    unscored=[{'input_index': 30, 'stage': 'acquisition', 'reason': 'HTTP 404'}],
    score_method='seeded_hit',
    source_metadata={'producer': saved_producer, 'attribution': saved_attribution},
)
assert summary['n_total'] == 3
assert summary['n_upstream_unscored'] == 1
```

Choose `seeded_hit` for saved seed-only binary search evidence or
`checked_pose_coverage` for recorded placed/legacy coverage. The existing
`get_screening_score` contract validates the native evidence. A completed seed-only
negative can have no fitted pose. A failed search remains unscored, with its full
native error retained. Missing upstream inputs never receive native failure
records or zero scores.

Original indices may be sparse. Repeated source IDs with distinct sample indices
remain separate observations; this tool does not infer chemical identity or
independence. Duplicate, unknown, overlapping or incomplete mappings, native label
conflicts and missing causes raise. `records` preserves original order, detached
cohort fields, native evidence and explicit causes. Original/evaluated/unscored
class counts and upstream/search counts remain separate. `metrics` describes
scored inputs only. Undefined AUC/BEDROC are `None`, including single-class sets;
all empty-set metrics are `None`. No-active EF retains the native metric's zero.

For `seeded_hit`, `missing_binary_score_AUC_sensitivity` additionally reports
label-dependent hypothetical worst/best 0/1 scores for missing entries. These are
sensitivity bounds, not imputation or confidence intervals. They do not alter
the recorded scores or the evaluated-subset metrics.

## Compare saved arms on their common scored subset

```python
from pharmacophoremt.validation import compare_screening_results

paired = compare_screening_results(
    original_cohort, saved_baseline_arm, saved_comparison_arm,
    ef_fractions=(0.1,), bedroc_alpha=20.0,
)
common = paired['common_subset']
delta_auc = common['delta_comparison_minus_baseline']['AUC']
```

Each arm is a dictionary with `evaluations`, `input_mapping`, explicit
`score_method`, optional `unscored` and `source_metadata`, as above. Both arms must
use the same criterion. Full original-cohort summaries remain in `arms`; the
common subset intersects scored original indices and recomputes both sets of
metrics on exactly those inputs. Ties use the existing unbiased metric contracts.
Undefined deltas are `None`. Matching criteria do not establish equivalent
queries, producers or chemical-series independence.

Source metadata and source attribution are copied unchanged. With
`pharmacophoremt.attribution()` enabled, attribution of these new operations and
the metrics actually recomputed is separate; reading old evidence never credits
its preparation, recognition or fitting again. See the
[saved-result API](../../api/saved_results.md) and the
[frozen ERα comparison](../validation/esr1_consensus_comparison.md).
