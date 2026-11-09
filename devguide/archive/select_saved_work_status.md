---
summary: Select saved work by native or pending status through the public reader.
issue: uibcdf/pharmacophoremt#158
status: resolved
opened: 2026-11-08
closed: 2026-11-09
verification: measured
area: [results, usability]
guard: tests/test_public_work_selection.py::TestPublicWorkSelection::test_status_selection_preserves_original_positions_and_distinctions
normative: devguide/saved_work_selection.md
blocked_by: []
supersedes: []
---

# Locate failed and pending work without inspecting every key

Manifest pages show original identities and exact-key detail shows one outcome.
Add explicit status selection to locate work directly, composing the owned
reader rather than a new molecular collection, parser or ranking method.

`view.work_items(*, status=None)` keeps the original four manifest fields/order.
None retains the unchanged default path; matched/not_matched/failed select exact
confirmed native status and pending selects no published outcome. Staged drafts
remain pending regardless of their native payload. The stdlib core owns the
status domain and matching; ArgDigest delegates value admission to that domain,
and SMonitor retains structured storage/iteration errors.

`--work-items --status STATUS` uses the existing public progress counts in the
same verified snapshot. Opt-in `pharmacophoremt.screening-work-selection@1`
contains global declared_work, selected_work, exact status and selected-stream
offset/limit/next_offset, with unchanged global manifest ordinals. Ordinary
work-page@1 output stays unchanged. `--status` is refused outside work inspection
before database I/O. Full opening/count costs remain; this is no index/scale claim.

The [prospective plan](../evidence/work_selection_plan_20261108.json) and
[owning contract](../saved_work_selection.md) fix independent native/status/count
oracles, default command-byte controls, lazy/closed/thread/late-error behavior,
full verification, explicit legacy admission, fresh guarded commands, original85
reader cases and one exact owned installed receiving. No native payload or draft
is exposed; no molecular work, score/credit, manager transaction, dependency,
persisted schema or resource increase is introduced. #108 owns the public task;
#148, provider and full supported public/platform gates remain separate.

Source receiving: 99 selected bodies pass (14 new and all85 original controls).
Four ordinary command outputs remain byte-for-byte identical. Strict full docs,
Ruff and local reporting/index checks pass; the
[source receipt](../evidence/work_selection_source_20261108.json) preserves the
12-failure/2-pass baseline and actual limits. No complete source or
public-platform qualification is claimed.

## Bounded installed bridge received

Received 2026-11-09 UTC after the increment started on2026-11-08 UTC.

Exact source153ea506aa077f2811242cac3e63d04944fd1cc1 produces the owned
0.4.0+188.g153ea50 wheel. The same99unchanged test bodies pass outside the checkout
with the original public reader-support payloads.93guarded fresh children include
65successes and28expected exit2 refusals; eight documented status commands
preserve four original historical files and their independently checked native/
pending membership, order and counts.211wheel payloads,156runtime files, nine
fixture files, QA/support/SDK identities verify. The
[installed receipt](../evidence/work_selection_installed_20261108.json) closes
this bounded bridge with its actual512MiB per-process limits and own peak RSS;
aggregate cgroup/zero-swap/task/quota enforcement remains unavailable. Full
source, complete dependency/public installed-platform, human-usability,
biological, molecular-performance and release gates remain independent.
