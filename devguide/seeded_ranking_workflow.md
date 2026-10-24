# Explicit seed-only molecular ranking

PharmacophoreMT #63 separates checked-pose coverage from a bounded molecular
ranking criterion. Existing `PoseEvaluator` coverage remains a statement about a
declared pose. The compatibility rigid search includes the supplied placement;
its partial `fit_value` is not a frame-independent molecular score.

## Choose the criterion

```python
search = RigidPoseSearch(query, search_method='seeded_hit', max_trials=10000)
screen = ConformerScreening(query, search_method='seeded_hit', max_trials=10000)
validator = RetrospectiveValidator(query, evaluator=search)
facade = VirtualScreening(query, screening_method='conformers',
                          search_method='seeded_hit')
```

The explicit `rigid_triplet_seed_hit@1` method reuses the existing public feature
inventory, chemically compatible essential triplet proposals, public MolSysMT
fitting and placed-pose evaluation. It never tests the supplied placement as an
additional candidate. It inherits the requirement for three non-collinear
essential centers and the finite raw-product budget. It performs no conformer,
chemical-state, hydrogens or molecular geometry generation in PharmacophoreMT.

`screening.get_screening_score(result, score_method='seeded_hit')` is a reusable
read-only operation over portable native evidence:

| Outcome | Molecular score | Meaning |
| --- | ---: | --- |
| Admissible fitted-seed hit | 1 | At least one tested seed satisfies all essential sites, exclusions and the explicit minimum coverage |
| Completed seed enumeration without a hit | 0 | This discrete search returned no hit; every such negative ties |
| Calculation failure or unresolved ensemble | None | No score; do not substitute an inactive label or a zero |

`ranking_score` is this dimensionless binary criterion. `fit_value` retains the
weighted coverage of an actually evaluated pose, even for a negative. When no
seed is fitted, a completed negative has `pose_evaluated=False`, `fit_value=None`
and no assignments: there is no evaluated pose to describe. This is still a
valid molecular score zero. In contrast, a failed record has `status='failed'`
and no definitive score. The scoring reader refuses legacy identity-pose search
evidence and incomplete unproven negatives; it does not relaunch molecular work.

A first admissible hit proves maximum binary score one, even when its optional
coverage is below one or raw enumeration was truncated. Search stops with
`termination='hit_found'`; it does not claim maximum optional coverage or minimum
RMSD. Without that hit, exhausted enumeration raises the existing search-budget
diagnostic and remains unscored. Complete negative results retain any checked
partial geometry separately; partial coverage never breaks their molecular tie.

## Frames, ensembles and scope

Triplet proposals use distances and chemical identities. Their fitted poses
transform covariantly under proper rotations/translations of the prepared input;
the arbitrary initial placement contributes no extra candidate. Invariance is
subject to the provider's numerical precision and declared matching tolerances.
Reflection, torsional changes, a changed chemical state, differently generated
coordinates or boundary-roundoff sensitivity are not a proper-frame equivalence.

The criterion is **binary success of a discrete search**, not an exhaustive
continuous-pose optimum, a graded similarity, an affinity or activity predictor.
Absence of a seed hit does not prove physical nonbinding. Query tolerances,
minimum coverage, explicit state/selection and finite budget remain part of the
method. No new claim of orientation-defined one/two-anchor search is made.

Every requested prepared conformer is attempted. Binary ties retain the first
requested frame. A hit proves molecular score one even if other frames fail;
all failed-frame evidence and `ensemble.complete=False` remain. A negative with
any failed frame is unresolved and has no score. Complete no-fit ensembles have
no `pose_coordinates`; a selected fitted frame retains actual fitted coordinates.
The selected pose's `fit_value` is diagnostic, not a maximum over all conformers.

Retrospective metrics use the declared binary scores and tie-aware native metric
tools, with original/evaluated class counts and failure indices. Facade hit lists
use the same criterion and stable input ties. CSV/DataFrame exports distinguish
`ranking_score`, `score_method` and raw `fit_value`. AUC/enrichment over binary
scores measure this hit decision, not the discrimination of continuous coverage.

## Compatibility and migration

`RigidPoseSearch` and `ConformerScreening` preserve their direct compatibility
default `search_method='placed_and_triplets'`, with `rigid_triplet_fit@1` evidence.
To deliberately rank that existing checked coverage, request
`score_method='checked_pose_coverage'` explicitly in `RetrospectiveValidator` or
`VirtualScreening`. Those consumers refuse implicit legacy rigid/conformer
coverage ranking. This is an explicit compatibility restriction, not a silent
conversion of old scores into new molecular scores. Placed `PoseEvaluator`
consumers keep their declared-frame coverage default.

The two criteria cannot be mixed within one run. A seed-only result with no
fitted pose cannot supply checked-pose coverage. The pure scoring reader leaves
source results/provenance unchanged and attributes only its own operation;
loading an archived source calculation does not credit recognition/fitting again.

Preserve the original #62 activity result and source identities. A new binary
replay requires a distinct predeclared experiment identity, the frozen original
query/inputs and a compatible qualified runtime. The already exposed dataset
is development evidence, not a new independent holdout. A score/metric change
between criteria is not a demonstrated improvement in biological prediction.

## Verification

`tests/test_seeded_scoring.py` protects independent proper-motion counterexamples,
fitted negatives/hits, raw versus binary coverage, incomplete-search decisions,
failed-frame resolution, stable ties, saved-evidence scoring without molecular
access and explicit compatibility choices. Existing rigid/conformer/facade and
retrospective controls retain their legacy checked-coverage expectations under
explicit opt-in. Original evidence archives are not rewritten.
