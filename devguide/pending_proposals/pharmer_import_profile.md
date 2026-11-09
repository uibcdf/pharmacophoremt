---
summary: Define and enforce an explicit supported Pharmer query import profile.
issue: uibcdf/pharmacophoremt#163
status: open
opened: 2026-11-09
closed:
verification: asserted
area: [io, semantics, interoperability]
guard:
normative:
blocked_by: []
supersedes: []
---

# Supported scientific meaning of Pharmer inputs

The existing reader has a fixed feature/geometry mapping but no comprehensive
admission or loss/refusal policy for fields such as requirement, size restrictions
and vector activation. Session/display annotations and engine/job settings need
different treatment from scientific constraints. This is a source-derived design
gap; it is not an executed external comparison or an upstream defect.

[#162](../pharmer_interoperability.md) separately qualifies enabled-point omission
and original-point mappings. P1#161uses its declared required-spherical subset.
Neither implies general optional/negated, size, direction/search-policy or
bidirectional equivalence. The r95requirement-field inconsistency also remains an
unexecuted version-specific source observation under#128.

Define the supported profile and reviewed compatibility policy; choose explicit
refusal and/or full loss reporting for scientific meaning that cannot be
preserved. Guided facade, direct reader and constructor must expose consistent
effective decisions, units and original identities. Preserve justified ordinary
inputs and molecular delegation. Freeze independent controls before implementing
new mappings; receive source/same-file installed behavior and maintain user/API
documentation. Full external execution stays under#128. This proposal alone
implements no new engine, provider operation, keyword, dependency floor or schema.
