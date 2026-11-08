# Analyze a saved screening run

Use `ScreeningRunView.work_items()` to inspect every declared work item, including
pending work. Use `summarize_screening_run` to analyze a labelled original cohort
without molecular access, another search or changes to saved evidence.

Provide explicit `work_key`/original `input_index` correspondence and a binary
integer label for each cohort sample. Every declared work must be mapped exactly
once. Repeated source keys remain distinct samples; they do not establish chemical
identity or assay independence. The tool neither groups states/conformers nor
infers activity labels. Additional original samples that never entered the run
require explicit upstream `unscored` causes, as in the
[batch-result recipe](retrospective_validation.md).

This self-contained example creates **synthetic saved-format records** with known
ranking answers. Its labels are analytical fixtures, with no experimental activity
or molecular calculation. For a real study, open your original saved run and use
its declared criterion and independently admitted cohort/label mapping.

```python
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from pharmacophoremt.validation import summarize_screening_run
from pharmacophoremt_results import ScreeningRunStore, ScreeningRunView

with TemporaryDirectory() as directory:
    root = Path(directory)
    manifest = root / "work.jsonl"
    work = [
        {"work_key": key, "source_key": "synthetic:repeated",
         "occurrence_key": f"row:{index}"}
        for index, key in enumerate(("hit", "zero", "failed", "pending"))
    ]
    manifest.write_text("".join(json.dumps(row) + "\n" for row in work))
    path = root / "run.sqlite3"
    with ScreeningRunStore.create(
        path, run_id="synthetic:analysis", query_bytes=b"synthetic query",
        context={"execution": {"score_method": "checked_pose_coverage"}},
        manifest_path=manifest,
    ) as store:
        for row, status, score in zip(
            work[:3], ("matched", "not_matched", "failed"), (1.0, 0.0, None)
        ):
            native = {"pose_id": row["work_key"], "status": status, "fit_value": score}
            if status == "failed":
                native["error"] = {"stage": "source", "message": "synthetic failure"}
            attempt = store.begin(row["work_key"])
            store.stage(attempt, {
                **row, "native_result": native, "ranking_score": score,
                "score_method": "checked_pose_coverage@1",
            })
            store.publish(attempt)
    before = path.read_bytes()
    cohort = [
        {"input_index": index, "label": label}
        for index, label in zip((10, 20, 30, 40), (1, 0, 1, 0))
    ]
    mapping = [
        {"work_key": row["work_key"], "input_index": original["input_index"]}
        for row, original in zip(work, cohort)
    ]
    with ScreeningRunView.open(path) as view:
        assert [row["work_key"] for row in view.work_items()] == [
            "hit", "zero", "failed", "pending"
        ]
        summary = summarize_screening_run(
            view, cohort, input_mapping=mapping,
            score_method="checked_pose_coverage", ef_fractions=(0.5,),
        )
        assert view.progress()["counts"]["committed_work"] == 3
    assert path.read_bytes() == before

assert summary["n_total"] == 4
assert summary["n_evaluated"] == 2
assert summary["n_native_failed"] == summary["n_pending_work"] == 1
assert summary["n_upstream_unscored"] == 0
assert summary["scores"] == [1.0, 0.0]
assert summary["metrics"]["AUC"] == summary["metrics"]["BEDROC"] == 1.0
assert summary["metrics"]["EF@50%"] == 2.0
assert "input_index" not in summary["records"][0]["outcome"]["native_result"]
json.dumps(summary, allow_nan=False)
```

The result uses `pharmacophoremt.screening_run_summary@1`. Each original-order
record contains its detached cohort, work item, original saved outcome and explicit
unscored cause. Native indices may be absent or repeated; they are preserved.
`run_configuration` retains the original producer/query/manifest declarations.
The caller owns the view; analysis leaves it open.

Pending work includes staged but unconfirmed attempts. It remains unscored with
stage `screening_run`; confirmed native failures and upstream unavailable inputs
have separate counters. Missing work never becomes a zero score. Metrics use
only scored samples; undefined statistics are `None`. Binary `seeded_hit`
summaries retain the existing hypothetical missing-score AUC sensitivity bounds.

The explicit criterion must agree with saved declarations/outcomes. A recomputed
native score that disagrees with its stored score is refused. Opening checks
internal saved consistency; this does not authenticate molecular calculations.
Original attribution stays inside saved outcomes/source metadata. Enabling
`pharmacophoremt.attribution()` credits newly executed analysis and metrics.

This completes a descriptive analysis workflow. Biological validation also needs
admitted endpoints, preparation, independent splits and leakage/uncertainty controls.
For two runs, use the [paired comparison](saved_run_comparison.md); it retains
both complete summaries and recomputes metrics on their common scored originals.
