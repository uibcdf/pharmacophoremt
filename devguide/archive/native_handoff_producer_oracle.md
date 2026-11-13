---
summary: Separate rebuilt and historical producer versions in H0/H1 acceptance.
issue: uibcdf/pharmacophoremt#201
status: resolved
opened: 2026-11-12
closed: 2026-11-12
severity: low
verification: measured
area: [tests, provenance]
guard: tests/test_binding_interface_handoff.py::test_rebuilt_primary_preserves_labeled_evidence_and_saved_native_semantics
normative: devguide/native_handoff_producer_oracle.md
blocked_by: []
supersedes: []
---

# Historical versus rebuilt H0/H1 producers

The [contract](../native_handoff_producer_oracle.md) records the frozen-versus-new
producer distinction. The unmodified old private wheel0.5.0+27.g9158c71 exposes
one failing/eleven passing original H0/H1 tests. The incorrect whole-metadata
equality confuses a new reconstruction with reading the original saved query.
No scientific runtime or ArgDigest defect is established.

Explicitly check fresh producer declarations against the executing version and
stored declarations against the frozen manifest at root and component
paths; compare every other field unchanged. Preserve original input hashes,
saved-read/no-credit guards and original failed test/artifact identity. Receive
the corrected oracle on the same old artifact and the new #200 artifact. Full
supported/public/platform gates remain independent.

## Executed resolution — 2026-11-12 local date

The [combined receipt](../evidence/interaction_argument_controls_20261112.json)
receives source148f3ba and its exact isolated wheel with267 selected source/owned
cases each,51 public-ArgDigest controls per context, public PUW0.28.1 and24
guide-block executions. The old artifact receives all12 corrected oracle cases
while its original1failed/11passed result stays unchanged. Native inputs and
scientific bodies retain their scope; broader#6/full supported/public gates remain
independent. All initial failed probes/harnesses remain recorded.
