# Explicit receptor contribution scientific controls

Run from the source checkout with the qualified scientific environment:

```bash
python -m pytest devtools/tests/scientific/test_receptor_contribution.py tests/test_receptor_contribution_plan.py --receptor=llm
```

This invokes the full frozen CLI study once. It is deliberately outside the
ordinary `testpaths = ['tests']` profile. Default tests verify the declaration
and compressed evidence; unchanged archived data do not qualify a new runtime.
Reexecute after the owning case/input/provider/scientific operations change.

For a read-only reanalysis, `PHMT_RECEPTOR_CONTRIBUTION_RESULT` may explicitly
identify an original result with its adjacent `.receipt.json`. The fixture
checks exact result, unchanged driver and frozen plan hashes before applying
the independent oracles. This is not molecular reexecution. The #90 receipt
retains the original source-bound use, failed attempts and exact commands.

## Native TYR dual-donor extension

```bash
python -m pytest devtools/tests/scientific/test_tyr_cardinality.py tests/test_tyr_cardinality_plan.py --receptor=llm
```

This executes the frozen #91 matrix once: 12 cells, 20 models, 100 primary
and 24 native-recovery evaluations. Two separate optional-provider simulations
each add 10 primary/two recovery calls. Default tests keep cheap plan/evidence
checks. For read-only reanalysis, `PHMT_TYR_CARDINALITY_RESULT` identifies the
original full JSON plus its adjacent `.receipt.json`; the fixture verifies
result/unchanged-driver/frozen-plan hashes before applying independent oracles.
Reanalysis does not execute molecular measurements. The
[case](../../../docs/content/validation/tyr_cardinality.md) distinguishes this
native separated-target control from overlapping-site one-to-one enforcement,
which retains its existing guard in `tests/test_pose_evaluation.py`.
