# Current source receiving and schema-oracle correction

Owner LMMV/dprada, 2026-11-06; qualification [#9](https://github.com/uibcdf/pharmacophoremt/issues/9) / [#23](https://github.com/uibcdf/pharmacophoremt/issues/23), correction [#102](https://github.com/uibcdf/pharmacophoremt/issues/102).
[Original receipt](evidence/source_suite_receiving_20261106_summary.json).

## Result and scope

**The two source-test defects are repaired and 111 selected controls pass. Complete corrected-source receiving is still pending hosted execution.** The two local full attempts are incomplete (task hook, then the deliberate 1 GiB resource cap); neither is a passed full suite.
The immutable producer is `5a860171c38e46708a1e5c6df3da8caf33366388`.
Only two test assertions differ from the previous reviewed `bacc374`; production code, scientific inputs, source pins and release plan are unchanged. This is Linux/Python 3.14 source receiving. Hosted supported-platform/minor, exact-file installed-candidate and public molecular dependency delivery keep their independent gates. It adds no biological or predictive validation claim.

| Evidence | Actual result | Acceptance limit |
| --- | --- | --- |
| Old-head hosted Linux/Python 3.14, `bacc374`, run 42169030918/job 127732249759 | 2,071 passed, two failed; full 2,073-case execution | Two stale envelope comparisons; failed source is not accepted |
| Initial local full attempt, `bacc374` | 1,202 passing reports / 1,185 distinct node IDs, then task-hook INTERNALERROR | Incomplete, no after-snapshot/full-suite acceptance; raw JUnit is preserved separately |
| Short diagnostic | Stopped during idle-priority page I/O, before its initial snapshot; exit 143 | No scientific result |
| Corrected local controls, `bacc374` plus the exact two-test overlay | 111 actual JUnit/progress cases pass, no skips/failures | Selected controls only, overlapping the complete suite |
| Corrected local full attempt, `5a86017` | 1,428 passing reports / 1,411 distinct node IDs; exit 137 / scope oom-kill | Incomplete; no after-snapshot or full-suite acceptance |

| Current corrected hosted Linux/Python 3.14, `5a86017` | Run 42174357921: four Linux cells executing, four macOS cells queued at the recorded observation; no complete corrected full result yet | Exact-source hosted source gate; independent of installed/public/platform gates |

Raw progress also includes 17 unittest subtest reports from three evidence-archive guards. Report totals are not unique pytest-node totals; collection itself contains 2,073 distinct nodes. Do not add these overlapping counts. The focused runner's original result contains an overly broad generic scope string; actual arguments select 111 cases. The receipt preserves that string and its explicit correction rather than altering the original result.

## What failed and what changed

The old hosted diffs show ten identical fields and one additional public-envelope field: `schema: pharmacophoremt.native@1`. Since #76, public JSON/YAML exports are tagged, while `_to_dict` intentionally preserves the historical payload used by SDF @1 and curation `metadata.source_model` history. No source geometry, constraint, score, map, metadata or attribution loss was observed in these diffs.

Both workflow guards now require the exact known public schema and compare every remaining field with the internal snapshot. The change does not alter serialization or silently retag SDF. Existing curation, native-schema and encoder-failure controls are included in the 111-case selection. The durable selectors are:

- `tests/test_prepared_workflow.py::test_curation_preserves_observations_and_declared_constraints`
- `tests/test_prepared_search_workflow.py::test_declared_anchors_and_prior_query_contract`

The initial local interruption is separate: a task-owned progress hook looked up globally patched `json.dumps` during a deliberate encoder-failure control. The corrected task runner captures its serializer before pytest. All four failure-injection cases pass with the corrected hook. Original attempts, script bytes, full output, identities and the interpretation correction remain in the receipt.

## Executed environment

Borrowed Python 3.14.7 source environment, explicit current checkout and previously received public ArgDigest 0.17.1 extraction. MolSysMT `0faf1584d05ac47ddcebfc20d9c9978b7f4f230e`, MolSysViewer `ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352`, and DepDigest `13cc73780a7cb645546ae3f396177f98b86a8792` are identified controlled source providers. Actual PyUnitWizard/SMonitor/Ackredit source heads and every inspected module/source/native/metadata identity are retained in the before/after snapshots.

The shared SDK verifies current direct runtime bounds and declared acquisition routes. The literal hosted `ci-3.14` acquisition preflight refuses this borrowed directory-source profile; it is not a reviewed root-Git installation context. Some support heads differ, and ArgDigest is an exact received public extraction rather than a VCS install. No acquisition-context equivalence is inferred.

Environment-wide pip check returns seven existing auxiliary-package requirement conflicts, retained verbatim and already owned by [MolSysSuite #82](https://github.com/uibcdf/molsyssuite/issues/82). This run does not establish a clean dependency closure. Shared/borrowed prefixes and provider sources are not modified.

## Commands, resources and reproduction

The archived task runner imports the explicit checkout/public ArgDigest overlay and invokes the published Pytest Receptor 1.2.2 with complete `tests` selection and raw JUnit. PYTHONPATH is unset for science. Use the recorded compatible receiving environment; the hosted route is independently declared in the committed workflow and dependency inventory. Administrative SDK/receptor imports use separate processes.

Actual source-process controls: CPU19/100% quota, 1 GiB memory maximum, zero swap, 32 tasks, nice19, idle I/O and all six backend thread variables one. Heavy phases run serially. Initial global memory pressure triggers an owned-scope freeze/thaw, with original observations retained. The short diagnostic waits on page I/O and is explicitly stopped. The corrected full local attempt reaches the deliberately configured 1 GiB maximum and ends with systemd result oom-kill after 1,428 passing reports. The journal and missing after-snapshot remain explicit. This is an insufficient full-run local memory budget, not a diagnosed production memory leak. No higher-memory full rerun is launched on the shared host. Runtime is not a benchmark and includes resource controls/suspension where recorded.

Owned capsule: `build/phmt-full-source-20261105-cdf3ayvo`, owner LMMV/dprada, review 2026-11-19 or relevant source/provider change. Required original receipts are retained; borrowed resources stay untouched. All owned local scientific scopes have ended; no continuing local scientific process is required.

## Next gates

Fresh fix-head CI [42174357921](https://github.com/uibcdf/pharmacophoremt/actions/runs/42174357921) identifies immutable 5a86017. Reporting governance has passed; Linux 3.11–3.14 scientific cells are executing and macOS 3.11–3.14 remain queued at this observation. Policy 42174358507 and Conda 42174358642 retain their own observed facts; no complete matrix or new candidate acceptance is claimed. Subsequent documentary/report-inventory changes need their relevant local checks and a fresh unskipped head inspection.
Old-head cancellation was requested only after fresh fix-head CI existed. A request is not terminal cancellation or a passing matrix; preserve actual job/step facts and omitted/queued cells. Daily recovery/weekly full routes under #9 remain unchanged.

Return to [proposed 0.5.0 readiness](release_0_5_0_readiness.md): receive a supported public MolSysMT artifact containing the required already-reviewed modern capabilities, then justify the actual minimum/scope and choose an immutable candidate. MolSysMT owns molecular inspection, formats, preparation, transformations and geometry. No local molecular fallback or provider patch is added. #9/#10/#23 retain the applicable source/installed/public/platform gates. Actual plan/tag/Release remains 0.4.0; no version freeze, package, tag, Release, addon or suite publication notice is created here.
