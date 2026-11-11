# Accumulated source checkpoint toward 0.6.0

Owners LMMV/dprada; PHMT#95/#9/#192/#23; selected 2026-11-11 UTC.
This selects one deliberate validation checkpoint for accumulated development,
without selecting a 0.6.0 tag, Release, package or documentation publisher.
The existing immutable 0.5.0 source remains unchanged.

## Preparation and source identity

Start at clean published `158dabf11f571d821f33aeaa7962a0bfaa16a710` and its
[scope review](release_0_6_0_scope_review.md). Refresh version-specific
[unreleased notes](../docs/content/about/release_notes.md), verify compatibility,
dependency/resource inventories, collection and coverage expectations, and run
the relevant administrative and strict-documentation checks before committing.
No new runtime capability, provider pin, workflow command, test exclusion or
publication-plan change is selected by this preparation.

The focused preparation commit is the source proposed for validation. Record its
full local/remote SHA, frozen workflow/configuration hashes and prospective
issue receipt before dispatch. Both source and later evidence-only heads keep
their own identities. Current local selected/owned receiving is not promoted to
a complete checkpoint merely because preparation passes.

## Required exact-source evidence

| Gate | Required observation |
| --- | --- |
| Full source CI | `.github/workflows/CI.yaml`, explicit `probe_backlog=false`, reporting governance and all eight Linux x86_64/macOS arm64 × Python 3.11–3.14 cells at the frozen source. Preserve the complete existing pytest command and assertions. |
| Acquisition and runtime | Reviewed exact sibling/SDK pins, actual preflight, package installation, out-of-source import, actual interpreter and macOS arm64 architecture. Source-qualified dependencies remain distinct from public dependency closure. |
| Tests and warnings | Native terminal success for every required step/cell; actual counts/skips and original warnings. Confirm the added capture/payload/archive/recovery cases are executed. #192's Python/platform isolation receiving remains open until these actual results support closure. |
| Coverage | Exact qualified filenames from all three configured roots, including new feature companion files and unexecuted files. Reject basename collisions, omissions, unexpected roots or a printed table in place of complete XML. |
| Frozen conformance | `.github/workflows/molsyssuite-policy.yml` at its existing policy-v1.5.4 pin; executed conformance/lint/format, plus the separate current-guide/instruction audit. |
| Publication governance | `.github/workflows/conda_publication_governance.yaml`: executed workflow/recipe/resource controls without a build or registry write. The prospective 0.5.0 Conda plan retains its identity. |

Use one manual request per absent required workflow, with `[skip ci]` retained on
routine commits. Verify remote source first and inspect any existing same-source
run before dispatch. An accepted HTTP request is not execution evidence. Discover
actual numeric handles and attempts independently; never automatically duplicate
an uncertain request, rerun successful cells or relabel an earlier run.

Use published GH Run Receptor 1.4.0 for the first compact inspection, then native
GitHub facts for gaps and exact-source acceptance. Keep raw logs/captures local;
publish only reviewed scalar facts, own-source identities and qualified evidence.
Preserve first failures and distinguish failed science, infrastructure and
unfinished runs. A checkpoint failure receives an owning diagnosis and focused
repair before a new source can be selected; no skips or relaxed assertions to
make a release appear ready.

## Shared-resource execution and separate gates

Local work remains serial on one allowed CPU and one numerical thread, with low
CPU/I/O priority, admission/monitoring and finite process/time limits. Start from
the previously measured 512 MiB DATA preparation envelope; use the measured
768 MiB attribution envelope only if relevant. Preserve a 20% physical-memory
reserve plus the task margin, and stop only own work under pressure. A capacity
observation is not a reservation. No local full scientific suite, heavy benchmark
or #148/#165 retry is selected; the required matrix uses its managed hosted jobs.

Successful controlled-source CI qualifies that exact source only. Full exact-file
installed/platform/public delivery stays #10/#23-owned; MolSysMT#624 collection,
biological validation, independent human receiving and scale remain separate.
Record the checkpoint result under #9/#95 and the maintained checkpoint/roadmap,
then decide the next development or release action from actual evidence.

## Local preparation received — 2026-11-11 UTC

The [receipt](evidence/source_060_preparation_20261111.json) receives ten quality
checks, strict full source/docs rendering and rendering against the reused exact
f722b45 owned artifact. It retains the collect-only 3,388-case inventory, all 127
expected coverage paths, fourteen frozen configuration identities, actual public
PUW0.28.1 bytes and serial resource observations. Pip check passes in the routine
Python3.14.10 environment. An older broken relative #9 report link was refused
and corrected; the original failed command/output is retained. No local full
scientific execution or complete candidate/public delivery follows from this.
