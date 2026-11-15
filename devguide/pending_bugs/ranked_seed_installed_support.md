---
summary: Include the unchanged ranked-seed cases in actual installed-test support staging.
issue: uibcdf/pharmacophoremt#230
status: active
opened: 2026-11-15
closed:
severity: medium
verification: asserted
area: [packaging, tests, screening]
guard: devtools/tests/test_distribution_contract.py::TestDistributionContract::test_installed_support_stages_actual_fixture_bytes_without_source_imports
normative: devguide/proposal_argument_controls.md
blocked_by: []
supersedes: []
---

# Ranked-seed installed support declaration

During #229 private-wheel receiving at source 32f4d2e, the ranking module fails
collection because its explicit tests/data/ranked_seed_cases.json input is absent
from the support declaration. The first attempt also lacked the harness tests/data
link; a second attempt with the actual stage link confirms the missing declaration.
Both collection failures and actual stage/link retirement remain original evidence.

Declare the existing file with its original SHA256 and extend the existing actual
SDK staging guard to load it through the staged helper, comparing original bytes
and cases. The task receiver links tests/data to this actual stage under context
retirement; no source runtime fallback or shipped support namespace is introduced.
Freeze the repaired support source and receive one exact private wheel and relevant
distribution/scientific consumers. Preserve prior wheel/source and original failed
attempts. The eight-validator public increment and scientific bodies are unchanged.

A scheduling error also overlapped the first failed ranking bootstrap with the end
of the first owned consensus group by 6.89 seconds. Both retained CPU19/backend1,
finite limits and monitored reserve, without pressure or foreign process changes.
Keep original timing evidence and do not label that interval serial. Remaining
work is serial after definitive predecessor completion; this is no speed evidence.
