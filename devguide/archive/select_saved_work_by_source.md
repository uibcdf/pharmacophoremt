---
summary: Select saved screening work by its exact original source key.
issue: uibcdf/pharmacophoremt#166
status: resolved
opened: 2026-11-09
closed: 2026-11-09
verification: measured
area: [screening, results]
guard: tests/test_public_work_source.py::TestPublicWorkSource::test_exact_source_and_status_intersections_keep_original_repeated_work
normative: devguide/saved_work_selection.md
blocked_by: []
supersedes: []
---

# Exact original source selection

## What

Expose an optional exact `source_key` on the independent saved-run work iterator
and CLI, composed with native/pending status selection. Preserve original
manifest ordinals, repeated occurrences and the full-file admission boundary.

## How

Use parameterized selection in the existing owned store. Keys remain opaque
nonempty strings. New CLI source selection uses work-selection@2 with exact
filters, global declared work, intersection count and selected offsets. Retain
only the requested page while finishing one selected stream in one snapshot.

## Why

Users reviewing chemical libraries need all original work for a source, including
failed and unconfirmed entries, without rerunning molecular evaluation.
MolSysMT#624 still has no delivered provider collection API; source/result
selection is PHMT's independent responsibility, not a substitute molecular reader.

## What is measured and what is assumed

The prospective plan is [recorded](../evidence/work_source_selection_plan_20261109.json).
The [source receipt](../evidence/work_source_selection_source_20261109.json)
retains 120 passing selected cases (13new/107existing), 11 original red failures,
eight exact original command outputs and strict docs/local governance. The
[installed receipt](../evidence/work_source_selection_installed_20261109.json)
receives the same120 bodies from source bd164dd / owned203, 131 guarded children,
16 documented historical commands on four unchanged files and eight ordinary
outputs identical to source. All214wheel payloads/159runtime files verify.
The original namespace-prefix sealing refusal is retained; only the private
comparison was corrected, with no runtime/test/receiving rerun. Full raw evidence
is archived with compressed/uncompressed hashes. No large-library performance,
new connector or chemical independence claim follows.

## Alternatives and refuted paths

Do not infer compound identity from source labels, expose drafts, bypass full
verification, change existing response formats or copy MolSysMT collection work.

## Scope and exclusions

No molecular execution, attribution changes, dependency acquisition, native build
or public release/platform qualification. Pharmer#165 and #148 stay stopped.

## Acceptance criteria

Independent mixed-status/source and opaque-key controls; original command/file
bytes retained; late failures have no success output; same tests from one exact
owned installed artifact with guarded fresh readers; public guidance and current
checkpoint. Resolved by the source/installed receipts and the guard above. Full supported
source/public/platform, biological, usability and release gates remain separate.
