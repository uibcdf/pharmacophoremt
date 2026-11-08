# Compare two saved screening runs

Use `compare_screening_runs` to compare two verified saved runs against the same
labelled original cohort. Each arm supplies its open view, explicit work-key to
original-index mapping and score criterion. Work keys may differ between runs;
the mapping defines correspondence. Both criteria must agree.

The result keeps both complete run summaries. Paired metrics use only original
samples with scores in **both** arms, in original cohort order. Zero scores remain
eligible. Pending work, confirmed native failures and upstream unavailability
remain visible in each full arm; none becomes a negative score. Inspect the full
arms as well as the common subset: different failure rates can cause selection
bias even when a paired metric looks favorable.

This self-contained example creates **synthetic saved-format evidence** with
opposite rankings, a confirmed failure and pending work. It performs no molecular
calculation and uses no experimental activity labels. With existing runs, open
their original files and supply independently admitted cohort labels and mappings;
analysis leaves both views open and the saved evidence unchanged.

```python
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from pharmacophoremt.validation import compare_screening_runs
from pharmacophoremt_results import ScreeningRunStore, ScreeningRunView

cohort = [
    {"input_index": 10, "label": 1},
    {"input_index": 3, "label": 0},
    {"input_index": 80, "label": 1},
    {"input_index": 21, "label": 0},
]


def synthetic_run(root, name, scores):
    work = [
        {"work_key": f"{name}:{index}", "source_key": "synthetic:repeated",
         "occurrence_key": f"row:{index}"}
        for index in range(4)
    ]
    manifest = root / f"{name}.jsonl"
    manifest.write_text("".join(json.dumps(row) + "\n" for row in work))
    path = root / f"{name}.sqlite3"
    with ScreeningRunStore.create(
        path, run_id=f"synthetic:{name}", query_bytes=f"synthetic {name}".encode(),
        context={"execution": {"score_method": "checked_pose_coverage"}},
        manifest_path=manifest,
    ) as store:
        for row, score in zip(work[:3], scores, strict=True):
            status = "failed" if score is None else "matched" if score else "not_matched"
            native = {"pose_id": row["work_key"], "status": status, "fit_value": score}
            if score is None:
                native["error"] = {"stage": "source", "message": "synthetic failure"}
            attempt = store.begin(row["work_key"])
            store.stage(attempt, dict(row, native_result=native, ranking_score=score,
                                      score_method="checked_pose_coverage@1"))
            store.publish(attempt)
    mapping = [
        {"work_key": row["work_key"], "input_index": original["input_index"]}
        for row, original in zip(work, cohort, strict=True)
    ]
    return path, mapping


with TemporaryDirectory() as directory:
    root = Path(directory)
    baseline_path, baseline_mapping = synthetic_run(root, "baseline", (1.0, 0.0, None))
    comparison_path, comparison_mapping = synthetic_run(root, "comparison", (0.0, 1.0, None))
    original_bytes = baseline_path.read_bytes(), comparison_path.read_bytes()
    with ScreeningRunView.open(baseline_path) as baseline_view, \
            ScreeningRunView.open(comparison_path) as comparison_view:
        result = compare_screening_runs(
            cohort,
            {"run_view": baseline_view, "input_mapping": baseline_mapping,
             "score_method": "checked_pose_coverage"},
            {"run_view": comparison_view, "input_mapping": comparison_mapping,
             "score_method": "checked_pose_coverage"},
            ef_fractions=(0.5,),
        )
        assert baseline_view.progress()["counts"]["committed_work"] == 3
        assert comparison_view.progress()["counts"]["committed_work"] == 3
    assert (baseline_path.read_bytes(), comparison_path.read_bytes()) == original_bytes

assert result["schema"] == "pharmacophoremt.screening_run_comparison@1"
common = result["common_subset"]
assert common["input_indices"] == [10, 3]
assert common["scores"] == {"baseline": [1.0, 0.0], "comparison": [0.0, 1.0]}
assert common["metrics"]["baseline"]["AUC"] == common["metrics"]["baseline"]["BEDROC"] == 1
assert common["metrics"]["comparison"]["AUC"] == common["metrics"]["comparison"]["BEDROC"] == 0
assert common["delta_comparison_minus_baseline"] == {"AUC": -1, "BEDROC": -1, "EF@50%": -2}
for summary in result["arms"].values():
    assert summary["n_total"] == 4 and summary["n_evaluated"] == 2
    assert summary["n_native_failed"] == summary["n_pending_work"] == 1
    assert summary["n_upstream_unscored"] == 0
json.dumps(result, allow_nan=False)
```

The schema is `pharmacophoremt.screening_run_comparison@1`. Each `arms` entry is
the complete `screening_run_summary@1`, retaining original run configuration,
native outcomes, work identities and source metadata. `common_subset` reports
original indices/labels/scores, recomputed arm metrics and comparison-minus-baseline
deltas. Undefined metrics or deltas are `None`. Views remain caller-owned.

No reindexing, state/conformer grouping, new search or molecular access occurs.
Source/work keys cannot establish chemical equivalence, independence or label
authority. Original source attribution remains preserved; optional
`pharmacophoremt.attribution()` credits the newly executed analyses and metrics.
These descriptive comparisons do not provide confidence intervals or demonstrate
predictive, causal or biological validity.
