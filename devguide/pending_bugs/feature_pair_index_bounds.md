---
summary: Unsigned explicit feature-pair indices wrap before shared-frame geometry evaluation.
issue: uibcdf/pharmacophoremt#221
status: active
opened: 2026-11-15
closed:
severity: high
verification: measured
area: [arguments, screening, geometry]
guard: tests/test_feature_pair_index_bounds.py
normative: devguide/selection_index_bounds.md
blocked_by: []
supersedes: []
---

# Explicit feature-pair index identity

The original public 12-case guard has four unsigned-overflow failures and eight
valid signed/unsigned order, empty-input and exact-boundary passes. Values above
int64 maximum can alias another feature or raise IndexError after conversion.
The [owning contract](../selection_index_bounds.md) requires representability
before casting, unchanged geometry and native range authority. Receive source
and exact-owned consumer groups, original guards/output, SDK retirement, strict
docs and relevant governance before closure. Broader #6 remains partial.
