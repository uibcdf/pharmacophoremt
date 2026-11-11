# Interruption-test process isolation

PHMT#192; owners LMMV/dprada; 2026-11-11 UTC.

The [complete corrected-source receipt](evidence/source_060_recovery_checkpoint_qualification_20261111.json)
now receives all eight Linux x86_64/macOS arm64 × Python3.11–3.14 source cells at
c5e952c/43109007084/attempt1:3420passes/zero skips each, preserving48warnings and
127qualified XML paths per cell. No controlled fork deprecation or
DeprecationWarning appears in any warning table. Required native/control steps
verify; [#192](archive/interruption_process_isolation.md) is resolved/archived for
the declared test-isolation scope. Earlier source/owned and failed-launcher
receipts below remain original; no generic process safety or public-installed
qualification is inferred.

The controlled #183/#186/#187 children use the explicit multiprocessing `spawn`
context. Their module-level targets receive only their output/store path,
candidate/current generation, declared mode/signal and pipe endpoint. They build
the needed configuration and test injections inside the child. No live molecular
handle, provider session, writer lease or parent monkeypatch must be inherited.
This is test infrastructure, not a production process manager or parallel API.

Driver controls still execute their bounded actual native prefix and real Ackredit
capture before parent-directed SIGTERM/SIGKILL or the interrupted atomic replace.
Store/workflow controls still pause immediately before or after publication,
reopen exact confirmed visibility and retain unknown publication attempts. The
separate lease probe starts while a real parent thread and parent writer are
active, independently verifies that the fresh child cannot obtain the lease,
and leaves the parent's ownership intact.

Startup/poll/join bounds and owned-child termination remain explicit; cleanup
never targets unrelated processes. The additional parent thread has a bounded
wait and is stopped/joined in cleanup. POSIX signals remain the platform
requirement for interruption; the former fork-availability skip is removed.
Run the relevant controls with `-W error::DeprecationWarning` so that the observed
threaded-parent fork deprecation cannot silently return.

Initial Linux/Python 3.14 source receiving passes all 103 existing controls across
`test_driver_checkpoints.py`, `test_feature_store.py` and
`test_feature_store_workflow.py`, with that warning policy. This does not establish
macOS or every supported minor. Full exact-head hosted/platform receiving remains
#9/#192-owned. Preserve the initial launcher correction (explicit pytest plugin
entry point) as an operator error, not a failed library test or a provider defect.

The later [combined receipt](evidence/native_feature_reconstruction_20261111.json)
also passes these same 103 controls in the exact owned wheel/public PyUnitWizard
0.28.1 context, without source fallback. Initial owned recursive-launcher failures
stay original; correcting only its main guard passes with the same artifact and
budgets. The supported platform/minor gate remains open.
