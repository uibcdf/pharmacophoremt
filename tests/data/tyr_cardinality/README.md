# Frozen native TYR cardinality controls

Owner LMMV/dprada, 2026-11-05, PharmacophoreMT #91. `eligibility_rule.json`
predates the public MolSysMT inspection; `eligibility.json` retains all five
eligible source-ordered TYR groups. The first two, 328/331, are fixed before any
model or pose evaluation. `plan.json` SHA-256 is
`29b62982967e19855c0429716815a2c39f645cea7fd2042be0f86567925aac81`.
These scientific declarations are immutable; amendments need a new identity.

The original prepared #52 H5MSM has SHA-256
`a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`.
[The original case](../../../docs/content/validation/prepared_receptor_workflow.md#inputs-and-preparation)
owns acquisition, redistribution, chemical/preparation history and unrefined-H
limitations. No molecular input is recopied or newly prepared here. Public
MolSysMT owns loading, selection, recognition, geometry, construction, transforms
and merge. The O/O/benzene witnesses are disconnected analytical controls.

[Protocol](../../../devguide/tyr_cardinality_protocol.md),
[measured case](../../../docs/content/validation/tyr_cardinality.md) and
[original evidence](../../../devguide/evidence/tyr_cardinality_20261105_summary.json)
separate the fixed expectations, actual measurements and limits. From the
qualified source environment:

```bash
python -m phmt_test_support.tyr_cardinality --output /path/to/result.json
python -m pytest devtools/tests/scientific/test_tyr_cardinality.py tests/test_tyr_cardinality_plan.py --receptor=llm
```

The explicit scientific selection executes the frozen 12 cells/20 models,
100 primary and 24 recovery evaluations, plus two separately counted optional
provider simulations. Ordinary tests check frozen declarations and compressed
evidence without rerunning the experiment. One protein/two TYR regions is not
an independent ligand/target cohort, biological validation or a benchmark.
