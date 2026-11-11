# Feature-store inspection, reuse and recovery exercise

Owners LMMV/dprada; 2026-11-10 UTC;
[#187](https://github.com/uibcdf/pharmacophoremt/issues/187), following
[the bounded store](feature_store_study.md). This is unshipped application-study
code. It does not introduce a supported feature-store API or a human-usability
result. Guided sessions compose the same expert operations; there is no second
scientific method or automatic molecular preparation.

## Decisions before work

`inspect_reuse(reader, required_families, work_keys=...)` reads one already pinned
manifest and original snapshot coverage. The guided `FeatureStoreWorkflowStudy`
owns a reader and delegates to that function. Expert calls borrow a reader;
closing the guided session never closes another caller's reader. A session keeps
its generation across refresh. Reopening is an explicit operation.

Selection keeps original global work ordinals and manifest order. Literal keys
retain spaces, case, unit-like strings and Unicode. Duplicate selection keys
refuse; unknown keys refuse rather than become an empty selection. An explicit
empty selection remains empty; an evaluated-empty family differs from an
unobserved family. Report the whole manifest's completeness separately from
selected extraction/family coverage. An explicit complete subset of a sealed
incomplete generation can be inspected/reused in captured-inventory scope;
this does not publish that generation or excuse omitted occurrences.

| Decision | User action | Scientific meaning |
| --- | --- | --- |
| `validate_quantities` | Validate the original quantities before reuse | Required selected families were evaluated; no query is admitted |
| `evaluate_missing_families` | Explicitly evaluate the listed missing families | Their absence is unobserved, not a negative result |
| `resolve_incomplete_extraction` | Inspect retained causes and explicitly prepare a new attempt | Failed/partial/unsupported/unattempted records are not empty features |
| `unknown_work_key` | Choose the exact recorded key | Unknown input is not an empty collection |
| `generation_mismatch` | Reinspect and explicitly choose the intended generation | A path/current alias never silently changes the session binding |
| `invalid_quantities` | Inspect the original validation cause | No invalid occurrence is silently dropped; original exception remains chained |
| `empty_selection` | Review the explicit empty scope | No source-level negative follows |
| `captured_features_ready` | Use the decoded captured inventories within their declared scope | Quantity checks passed; molecular origin/query/lookup/run admission remains separate |

`prepare_reuse()` reinspects the selection and calls the original reader's
quantity decoder for every chosen occurrence. A metadata report or a caller's
mutated copy is not an admission token. Fresh calls reconstruct detached native
inventories, preserve original maps/order and return global ordinals with literal
work keys. A failure reports its original ordinal and prior validated ordinals;
no partial successful selection is returned as complete. The existing
FeatureSnapshotStudy/PyUnitWizard QuantityRecord contract remains the sole
quantity codec and retains its provisional provider status. Required families
check evaluation coverage; reuse returns each complete captured inventory,
including additional captured families, without filtering or renumbering it.

Every report leaves query admission/match outcome unset and molecular origin
unauthenticated. These reports qualify captured-feature reuse, not source-level
screening, compatibility with a changed predicate/query, a persisted lookup or
resume of a saved run. Currentness is explicitly not checked by a pinned reuse
reader; generation choice is visible rather than inferred from its path.

## Guided and expert composition

Run these examples inside the admitted source-study context after the opt-in
exercise driver creates its fresh store. Bind `original_generation` to the
report's `pinned_reader_generation` (the driver subsequently publishes a refresh).
These are technical exercises, not
installed-package user recipes. Keep the returned generation and exact work keys.

```python
from phmt_test_support.feature_store_workflow import (
    FeatureStoreWorkflowStudy,
    explain_reuse,
)

with FeatureStoreWorkflowStudy(store_path, original_generation) as features:
    preview = features.inspect(["hb donor"], work_keys=["nm", "1 nm", "repeat=α"])
    print(explain_reuse(preview))
    result = features.reuse(
        ["hb donor"],
        work_keys=["nm", "1 nm", "repeat=α"],
        expected_generation=preview["generation"],
    )
```

The equivalent expert composition borrows a reader and uses the same functions:

```python
from phmt_test_support.feature_store import FeatureStoreReaderStudy
from phmt_test_support.feature_store_workflow import inspect_reuse, prepare_reuse

with FeatureStoreReaderStudy(store_path, original_generation) as reader:
    preview = inspect_reuse(reader, ["hb donor"], work_keys=["nm", "1 nm", "repeat=α"])
    result = prepare_reuse(
        reader,
        ["hb donor"],
        work_keys=["nm", "1 nm", "repeat=α"],
        expected_generation=preview["generation"],
    )
```

`explain_reuse()` is ordinary application text from the same decision report.
Decision names are study actions, not public diagnostic IDs. This is not a
substitute SMonitor renderer/catalog or public ArgDigest boundary. Promotion
requires registering the public argument/diagnostic contracts through their
owners, preserving provider floors and qualifying installed delivery. No new
optional engine, acquisition route or runtime dependency is added here.

## Recovery observes publication before choosing an action

`inspect_publication_recovery(writer, current_reader, attempt)` borrows the
existing cooperating writer lease and verified current reader. Guided
`recover_publication(path, attempt)` opens/closes those same owners; it refuses
when another writer holds the store. Inspection/reuse needs no writer lease.
The recovery reader must name the same complete generation as current, or be
absent when no generation has been published. Retained inconsistent receipts
refuse interpretation rather than claim success.

| Current observation | Meaning and action |
| --- | --- |
| Candidate is current | Its verified generation is visible now; no linked publication retry is needed, even when the original receipt is unknown/raised |
| Current equals the original expected generation | Candidate is not current now; historical publication may remain unknown. An explicit retry revalidates the candidate and quantities |
| Another generation is current | Review the newer/different publication; the guided retry refuses to replace it |

Completed, raised and unknown receipts are separate from current visibility.
A candidate not current now may have been published earlier. A started receipt
without a terminal remains unknown even after a successful linked retry. No
rollback, historical absence, worker liveness, exactly-once computation or run
resume is inferred. Candidate readability/quantity validity is **not** established
by recovery metadata; retry calls the original writer publication validator.
Missing/corrupt/invalid candidates therefore fail before replacement and retain
the new operation's original failure while preserving the current generation.

An explicit guided retry supplies `retry=True` and `expected_current` (including
explicit None for an unpublished store). It delegates to expert
`retry_publication(writer, current_reader, attempt, expected_current=...)`, then
the existing writer's linked `publish`. Refuse an already-current candidate,
a displaced original expectation, wrong current reader or unknown/nonpublication
attempt. Native store exceptions retain their original semantics: an exception
after replacement still requires checking visibility. There is no automatic
retry, extraction, cleanup, rollback or source repair.

## Reproducible technical exercise and acceptance

`devtools/exercise_feature_store_workflow.py` reserves a new output and store,
requires an explicit original snapshot context/admission SHA, and uses only the
already captured eleven-entry corpus. Under nm and pm policies, six tasks compare
full reports and projected native inventories between guided and expert routes:
selected donor/charge reuse, known-empty aromatic evaluation, unobserved donors,
exact literal keys, generation mismatch and explicit empty selection. The driver
also receives pinned refresh, completed-but-superseded versus current publication,
and refusal of a needless retry. It preserves application checkpoints/actual
attribution using the existing #183 helper. Original snapshots and all store
bytes remain unchanged during inspection/reuse/recovery; refresh itself is an
explicit separate writer operation. No matching or molecular operation runs.

The [receipt/archive](evidence/feature_store_workflow_20261110.json) retains the
original cases, reports and receiving identities. Focused controls live in
`tests/test_feature_store_workflow.py`; unchanged #186 storage controls are rerun
as regression coverage. Additional controlled child termination before/after
publication verifies real unknown attempts and guided/expert linked-retry parity.
Cold receivers block scientific imports while exercising preview/recovery.
Real Ackredit sessions check no new credit from saved reads or feature reuse.

Actual human participants: **zero**. Next run the declared tasks with novice and
expert users, retain their unedited observations, and report concrete barriers.
Before public promotion, settle naming, selection/generation policy and public
argument/diagnostic admission. Persisted lookup identity/cost, scale, biological
validation, full exact-head/public/platform/release gates and MolSysMT#624 remain
separate. #148/#165 stay stopped.

## Later public-surface proposal — #188

The [minimal API proposal](feature_asset_public_api.md) receives names, selection/
generation/page policy and a real ArgDigest/SMonitor admission study. Those are
proposed public contracts; this workflow remains unshipped and unchanged.
