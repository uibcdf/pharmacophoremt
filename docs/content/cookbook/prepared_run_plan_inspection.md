# Inspect a prepared screening plan

Build and inspect a plan before creating a run or consuming prepared inputs.
Its compact console representation shows the method, scoring criterion and query
size/hash. `describe()` returns the exact query byte identity and the complete
captured context, including expanded settings and producer declarations.

This is a development-source public operation. Use the
[qualified installation context](../about/installation.md); full supported
installed/public delivery remains separate. This inspection reads no molecular
inputs and performs no screening or fitting.

## Supply a query and compatibility declarations

Provide `query_path` for an authorized native pharmacophore JSON file and
`compatibility` with your producer's six declarations: `prepared_snapshot`,
`preparation`, `features`, `index`, `grouping` and `numerical`. `index` may be
`None`. The [recoverable recipe](recoverable_prepared_screening.md#supply-prepared-inputs)
explains these input responsibilities. Do not invent identities just to construct
a plan; the declarations do not authenticate molecular contents.

The example explicitly chooses rigid `seeded_hit`, at most 10000 triplet trials
and frame/state 0. Its query needs at least three non-collinear essential centers.
Other methods and options retain their defining native admission rules.

```python
from pharmacophoremt.screening import build_prepared_run_plan

plan = build_prepared_run_plan(
    query_path,
    screening_method='rigid',
    score_method='seeded_hit',
    compatibility=compatibility,
    constructor_options={'search_method': 'seeded_hit', 'max_trials': 10000},
    evaluation_options={'structure_index': 0, 'chemical_state': 0},
    on_error='record',
)
description = plan.describe()
query_identity = description['query']
effective_settings = description['context']['execution']
```

Inspect `plan` in a console/notebook for a compact view. Inspect `query_identity`
for the original byte count and full SHA-256, and `effective_settings` for method,
score criterion, constructor/evaluation options and the error policy. The
remaining `description['context']` preserves compatibility declarations and the
original runtime binding. Changing this detached dictionary cannot change the
frozen plan; the public `query_bytes` and `context_json` fields remain available.

The hash covers the exact captured artifact, including JSON spelling. It is not
chemical identity or proof of correct preparation. The console representation
omits raw query bytes and context, while the explicit description can contain
private producer metadata. Review it before sharing.

## Continue with the captured plan

Use the [recoverable workflow](recoverable_prepared_screening.md#start-and-resume-a-run)
for creation/resumption or its public expert composition. Inspection does not
reconstruct an evaluator, reopen the query file, compare the current runtime or
credit a scientific calculation. A description of original settings does not
admit them for execution in a changed environment.

The source-code binding remains conservative: changed scientific code can require
a new linked run even when molecular inputs are unchanged. Historical reading
uses the [independent saved view](recoverable_prepared_screening.md#inspect-and-export-the-saved-view),
which retains original evidence without molecular reexecution. This addition
changes console display, with existing plan/query/run formats unchanged.
