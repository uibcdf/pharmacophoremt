---
summary: Compare complete curation payloads separately from the public native schema envelope.
issue: uibcdf/pharmacophoremt#102
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: medium
verification: measured
area: [tests, io]
guard: tests/test_prepared_workflow.py::test_curation_preserves_observations_and_declared_constraints
normative: devguide/native_schema.md
blocked_by: []
supersedes: []
---

# Prepared workflow schema-envelope oracles

## Resolution

Commit `5a860171c38e46708a1e5c6df3da8caf33366388` changes only two workflow assertions. Each requires public `pharmacophoremt.native@1`, then compares all other fields exactly with the internal curation snapshot. The separate search guard is `tests/test_prepared_search_workflow.py::test_declared_anchors_and_prior_query_contract`.

**111 selected cases pass**, including both corrected guards, curation, native schema and four deliberate encoder-failure controls; no failures/skips and complete before/after identity equality. [Receiving record](../source_suite_receiving_20261106.md) and [original receipt](../evidence/source_suite_receiving_20261106_summary.json) preserve the failed hosted source, incomplete local attempts and their independent acceptance limits. Broader exact-source/platform/installed gates remain #9/#23.

## What and why

Old-head hosted Linux/Python 3.14 CI executes 2,073 cases: 2,071 pass and two assertions fail. Both diffs show ten identical fields and only an additional public schema marker. Since #76, public JSON/YAML export is tagged, but internal `_to_dict` and curation history deliberately keep the historical payload shared with the separate SDF @1 format. These two integration expectations had not accounted for that distinction.

## Evidence and alternatives

The correction keeps every scientific-field comparison and explicitly checks the known schema. It does not add arbitrary field ignoring, rebaseline geometry/constraints/scores/maps/attribution, change historical archives, or retag SDF. The initial local task-hook failure from globally patched json.dumps is a separate instrumentation defect, not either hosted assertion failure. A later bounded local full attempt ends at its 1 GiB memory cap; neither incomplete attempt is accepted full coverage.

## Acceptance

Both independently sourced workflow payloads retain exact evidence/constraints while their public schema marker is checked separately. The existing focused schema/curation/encoder controls pass. No production, molecular operation, provider, dependency or version-plan change is needed.
