---
summary: Keep the scientific matrix stoppable while retaining skipped-needs recovery.
issue: uibcdf/pharmacophoremt#169
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: measured
area: [ci, resources]
guard: tests/test_ci_routes.py::test_contributor_routes_and_complete_supported_matrix
normative: .github/workflows/CI.yaml
blocked_by: []
supersedes: []
---

# Scientific matrix cancellation

The source job begins `always() && ...` to retain execution after the conditional
backlog job is skipped. A normal cancellation of our failed candidate42651970337
is accepted, but fresh native evidence still shows four running Linux jobs and
four queued macOS jobs. GitHub documents that a true `always()` job condition
survives cancellation and recommends `!cancelled()` for cancellable work.
Only our invalid source run receives the documented force-cancel request after
normal cancellation fails to stop it. No unrelated job or process is touched.

Replace only that status predicate, preserve all remaining recovery/input/event
conditions and scientific matrix/commands/dependencies, and update the reviewed
consumer workflow hash. The existing complete-route guard is changed to require
a leading `!cancelled() &&` without `always()`. Its red receiving has one failure
and two passing route cases against the original workflow. Keep source counts,
actual cancellation and local predicate receiving distinct.

[GitHub cancellation semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-cancellation),
[recommended inverse predicate](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows)
and [bounded force-cancel route](https://docs.github.com/en/rest/actions/workflow-runs#force-cancel-a-workflow-run)
are the primary contract. This is a PHMT orchestration correction, not an
upstream GitHub defect or weaker scientific gate. The [local receipt](../evidence/numerical_reader_ci_recovery_20261109.json)
receives eight route/backlog controls and final distribution/preflight checks,
with all other decoded workflow fields unchanged. The original force-cancel
is independently verified terminal with eight cancelled scientific cells. The
new predicate is not deliberately cancelled in another remote experiment;
corrected-candidate full source receiving remains pending. Frozen policy pin and public
package/provider/runtime meanings remain unchanged; #148/#165 remain stopped.

[MolSysSuite#177](https://github.com/uibcdf/molsyssuite/issues/177) owns explicit cancellation
scenarios in the existing bounded inventory tool. Its current unknown result is
correct; no local parser fork or provider/SDK pin update is introduced. The local
orchestration correction resolves this report with its durable guard; exact-head
full source and supported/public/platform gates retain separate acceptance.
