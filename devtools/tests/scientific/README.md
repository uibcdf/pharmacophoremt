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
