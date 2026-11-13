---
summary: Align controlled MolSysMT acquisition with immutable H5MSM 1.0 inputs.
issue: uibcdf/pharmacophoremt#207
status: partial
opened: 2026-11-13
closed:
severity: medium
verification: measured
area: [ci, integration]
guard: tests/test_binding_interface_handoff.py::test_native_full_context_and_strict_group_scope_preserve_original_ids
normative:
blocked_by: []
supersedes: []
---

# Controlled H5MSM 1.0 acquisition

Scheduled source run43459510556/attempt1 at9b50fdeb552d89470f61be74c0b4a65dfb39f0cb
is terminal failure: four Linux test failures, four macOS cancellations and two
successful administrative jobs. The macOS acquisition/capacity annotations are
unverified hints; no scientific outcome is inferred for those cancelled cells.
Public GH Run Receptor1.5.0 retains native facts and a job-only Linux3.14 log.
That job132002544754 reports3655passes,41setup errors,1failure and48warnings.
Both grouped causes reach the old MolSysMT H5MSM0.5-only reader.

Both controlled manifests pinned0faf1584d05ac47ddcebfc20d9c9978b7f4f230e,
while the unchanged handoff fixtures explicitly use public H5MSM1.0. Local
receiving through a newer editable provider did not qualify this older context.
This is consumer acquisition debt, not a demonstrated molecular-provider defect.

## Correction and bounded receiving

Select published source05865fbb3ba499d4117d6ba3e1cf55d98a9e239e, the first explicit
H5MSM1.0 owner reader. The remote h5msm.py Git blob27e665f2b0ec6afa8d013979f8175b66b0352641
matches the inspected local object. Its metadata requires PUW>=0.28.1,
ArgDigest>=0.14.0 and SMonitor>=0.16.0, compatible with the existing controlled
support pins. It adds Jinja2>=3.1.2 to the provider's required surface; actual
installed closure remains a mandatory hosted SDK check. This source choice
avoids requiring the newer editable provider's PUW>=0.29.2 floor.

Advance only MolSysMT in both manifests and re-review their route checksums.
Keep all six other provider pins, workflow bytes, scientific commands, eight
supported cells, fixture bytes/hashes and runtime code unchanged. The existing
distribution guard refuses unreviewed manifest changes; native handoff guards
read the original artifacts and assert independent geometry, maps and decisions.

The selected-source interoperability probe passes52 cases with public PUW0.28.1,
ArgDigest0.17.1 and Pytest Receptor1.2.2 after the separate #208 oracle correction.
It stages original Git source and inherits the workstation Rust extension;
tracked Rust/toolchain bytes match the current local source. It does not build
or qualify a MolSysMT wheel, complete controlled closure or supported platform.
Its unstamped source truthfully reports0+unknown, not a manufactured version.
Original plugin-registration failure and48pass/1oracle-failure attempts remain.

#148's frozen client and SOURCE_SHA remain unchanged. Its real admission now
refuses the changed current manifest before installation; the unit guard asserts
that refusal. The downstream guard unit control supplies only a synthetic frozen
fingerprint to reach its own branch. Neither permits execution or reopens
#148/#165. A future restart needs separately reviewed inputs/context and limits.

## Acceptance still pending

Record and inspect a separate immutable corrected-source checkpoint under#9/#23.
Require every supported full scientific cell and its qualified coverage, reporting,
frozen policy and publication-governance checks. The original failed/cancelled run
must remain failed. Selected receiving or collection never clears that gate.
Public/installed package closure, #206 and any0.6.0 tag/publication stay separate.
The [consolidation receipt](../evidence/controlled_h5msm1_receiving_20261113.json)
records exact local inputs, original attempts and the resource envelope.

## Frozen recovery requested — 2026-11-13

Commit91eed32c55cbb53b2ba5f4a36d63add62c006798 is pushed with [skip ci].
[Prospective #9 notice](https://github.com/uibcdf/pharmacophoremt/issues/9#issuecomment-6860078462)
precedes complete all-page exact-head discovery and three single manual requests.
[Initial receiving](../evidence/source_060_h5msm1_pending_20261113.json) verifies
source43472677149, policy43472685859 and publication controls43472695075,
attempt1 and exact source. Policy/publication/reporting pass. Five scientific
cells execute and three macOS cells wait; four Linux cells reach Run tests.
The native run-level queued status is preserved separately from job progress.
No complete source/XML acceptance follows. Observe the same handles; do not
rerun/cancel originals or duplicate requests. #208 is closed with local guards;
this theme remains partial until full corrected source receiving succeeds.

## Terminal rejected source and ERalpha correction — 2026-11-13

Full attempt capture verifies 43472677149 / source 91eed32 / attempt 1 is
terminal failure. All five executed scientific jobs report 3,698 passes, two
failures and 48 warnings. The three other macOS jobs cancel without scientific
execution; annotations supply unverified capacity hints only. The two failures
are identical across those five jobs. H5MSM1.0 read failures are absent.

[#209](../archive/eralpha_controlled_provider_receiving.md) corrects the ERalpha
case's annotation-loss and reference-credit expectations, adds three negative
controls and receives both public recipes. [Local controlled receiving](../evidence/eralpha_controlled_receiving_20261113.json)
passes 76 cases and 16 nm/pm blocks with every selected provider revision, while
retaining the original inherited-native limitation. Runtime, pins, workflow bytes
and source fixtures stay unchanged. This resolves the bounded oracles, not the
complete supported-source gate. Freeze one corrected source, discover existing
runs before requesting each absent checkpoint once, and retain original failed
runs. Expected scope is 3,703 cases and the same 128 qualified XML paths per cell.

## Corrected ERalpha source requested — 2026-11-13

[Prospective notice](https://github.com/uibcdf/pharmacophoremt/issues/9#issuecomment-6866660765)
records frozen e7d3e4914dc7113ed9468c4a9c19eb3c5840bf6f before complete
all-page prior discovery and each of three single workflow requests. [Pending
receiving](../evidence/source_060_eralpha_pending_20261113.json) independently
verifies source43520902352, policy43520910099 and publication43520918803,
attempt 1. Policy/publication/reporting pass; all eight scientific jobs have
runners. Full terminal science and XML are still pending. #209 closes only its
case-oracle correction. Observe the same source execution; preserve all failed
originals and do not automatically duplicate, rerun or cancel jobs.
