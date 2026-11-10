# Saved-inspection usability exercise

Owners LMMV/dprada; [#172](https://github.com/uibcdf/pharmacophoremt/issues/172),
under the mature-0.x milestone2/#108 workflow. The
[participant sheet](../docs/content/cookbook/saved_inspection_exercise.md) and
[downloadable builder](../docs/_static/examples/saved_inspection_exercise.py)
use a self-contained synthetic saved run. No molecular calculation, biological
prediction or representative human usability follows from this fixture.

## Facilitation and evidence boundary

Give a participant the setup and task sections before the CLI/API assistance.
Record whether they need the assistance, another hint or direct intervention.
Use the [unfilled observation template](templates/saved_inspection_observation.md)
for an actual session. Keep novice and API familiarity explicit; alternate the
first route in a comparison and record practice effects rather than treating a
second attempt as independent evidence. The facilitator answers below are not
participant observations.

A task succeeds only when its requested counts, identity, state and explanation
are correct. Record an incorrect but confident answer, a blocked task and a
successful recovery separately. Keep all attempted tasks in the denominator.
No arbitrary completion-time threshold or aggregate usability score is declared.
Only actual observed participants can support unaided-completion, confusion,
assistance or timing claims. Automated execution checks technical readiness.

## Frozen facilitator answers

The [prospective plan](evidence/saved_inspection_exercise_plan_20261110.json)
freezes the exact eight mappings and seven tasks before dry-run execution.

| Task | Correct observation and explanation |
| --- | --- |
| 1. Discover | Eight work entries; three literal sources in first encounter order: `" --source α "` with5, `"source:other"` with2, `"0"` with1. Their first original ordinals are0,1,5. Repeated labels/occurrences establish no chemical independence. |
| 2. Selected pending count | First source has two pending entries at global ordinals3and4. A one-row page displays ordinal3and has selected-stream next_offset1. The complete count remains2. Other chosen-source counts are matched1, not_matched1, failed1. |
| 3. Original failure | Literal work key `" --failed key α "`, global ordinal0, confirmed true, status failed, ranking_score/fit_value null and attempts started1/staged1/committed1. The synthetic original producer and full saved outcome remain. |
| 4. Pending distinctions | `"staged α"` at ordinal3is pending/unconfirmed with outcome null and attempts1/1/0; `"never α"` at ordinal4is pending/unconfirmed with outcome null and attempts0/0/0. The unpublished failure is not confirmed; neither read retries it or proves a worker is running. |
| 5. Valid zero | `"negative zero"` at ordinal2is confirmed not_matched with score0and attempts1/1/1. It is distinct from unscored failure and unpublished work. These synthetic seeded statuses/scores are consistent; they are not new scientific results. |
| 6. Empty source | Exact absent source gives selected_work0and records[] with a readable run; it is different from an open/read failure. |
| 7. Literal-key recovery | Trimmed `"--failed key α"` is unknown. CLI exits2with no success stdout; public API raises ScreeningRunError/PHMT-E201. Original exact key succeeds afterward on the same unchanged file. |

Global counts are committed6, scored4, matched3, not_matched1, failed2, pending2;
retained attempts are started7, staged7, committed6. The declared manifest and
all publication identities are unchanged by inspection. `source_key="0"` and
work_key `"0"` are literal strings, not a falsy missing value.

## Technical receiving

The initial frozen plan required source and unchanged owned208 dry-runs of the
original downloadable builder, all ten documented inspection commands (including
one deliberate refusal) and the full expert block outside the checkout, with
only declared run paths rebound. Independent literal manifest/readonly SQL/JSON
oracles protect complete counts, source order, global mappings, attempts and
original full outcomes. Compare source/installed observations and deterministic
fixture bytes. Duplicate setup must refuse replacement and preserve the fixture.

Retain original runtime/provider/artifact and earlier cookbook blocks, strict
docs/download/navigation and reporting evidence. The builder is an application
example; its one directory parameter uses argparse. It adds no public library
validation, quantity, attribution or optional-engine boundary. Existing
ArgDigest/SMonitor definitions are consumed through the already-qualified reader.
No new package, provider transaction, source connector or molecular collection
is added. MolSysMT#624 retains collection ownership;#148/#165 remain stopped.

The [executed receipt](evidence/saved_inspection_exercise_20261110.json) now
receives that technical scope: identical40960-byte fixture files, ten documented
inspection commands and one full expert body per context, plus a corrected-key
CLI request after each deliberate refusal. All26guarded children and seven
reader modules per context preserve159runtime/214wheel payload identities.
Independent literal/SQL/JSON counts and full details agree. Strict docs verify
the exact download and both navigation links. The original answer/task bodies
and unfilled template stay intact; this paragraph records receiving only.
One supplemental import-boundary harness startup refusal is preserved; its
isolated-parent correction runs only the two extra CLI recovery requests.
Actual human participant count is zero.

## Human receiving still open

No participant sessions are claimed here. Run the declared tasks with actual
novice and expert users, retain original observations, review concrete barriers
in owning issues and repeat only the affected tasks after changes. Complete
public/installed/platform, scientific prediction, scale/performance and release
gates remain independent of both this kit and any future usability result.
