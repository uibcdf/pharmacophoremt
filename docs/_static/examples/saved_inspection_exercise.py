"""Create synthetic saved work for inspection practice; no scientific calculation."""

from __future__ import annotations

import argparse
from pathlib import Path

from pharmacophoremt_results import ScreeningRunStore, canonical_json


def create_exercise(destination: Path) -> None:
    """Write one small public run into a fresh, caller-selected directory."""
    destination.mkdir(mode=0o700)
    source = " --source α "
    mappings = [
        {"work_key": key, "source_key": label, "occurrence_key": "same"}
        for key, label in (
            (" --failed key α ", source),
            ("other:matched", "source:other"),
            ("negative zero", source),
            ("staged α", source),
            ("never α", source),
            ("0", "0"),
            ("other:failed", "source:other"),
            ("matched α", source),
        )
    ]
    manifest = destination / "work.jsonl"
    manifest.write_text(
        "".join(canonical_json(row) + "\n" for row in mappings), encoding="utf-8"
    )
    confirmed = {
        " --failed key α ": ("failed", None),
        "other:matched": ("matched", 1),
        "negative zero": ("not_matched", 0),
        "0": ("matched", 1),
        "other:failed": ("failed", None),
        "matched α": ("matched", 1),
    }
    context = {
        "purpose": "Synthetic inspection exercise; no molecular evaluation",
        "execution": {"score_method": "seeded_hit"},
        "producer": {"name": "saved-inspection-exercise", "version": "1"},
    }
    query = canonical_json({"synthetic": True, "exercise": "saved-inspection"})
    with ScreeningRunStore.create(
        destination / "run.sqlite3",
        run_id="exercise:saved-inspection:1",
        query_bytes=query.encode("utf-8"),
        context=context,
        manifest_path=manifest,
    ) as store:
        for mapping in mappings:
            key = mapping["work_key"]
            if key not in confirmed and key != "staged α":
                continue
            status, score = confirmed.get(key, ("failed", None))
            outcome = {
                **mapping,
                "native_result": {
                    "pose_id": key,
                    "status": status,
                    "fit_value": score,
                    "synthetic": True,
                    "producer": {"name": "synthetic-exercise", "version": "1"},
                },
                "ranking_score": score,
                "score_method": "seeded_hit@1",
            }
            attempt = store.begin(key)
            store.stage(attempt, outcome)
            if key in confirmed:
                store.publish(attempt)
    (destination / "README.txt").write_text(
        "Synthetic inspection exercise. No molecules were screened.\n"
        "run.sqlite3 is public saved work; work.jsonl is its original manifest.\n"
        "Inspect these files read-only. Use a new directory to create another copy.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="A new exercise directory.")
    arguments = parser.parse_args()
    if arguments.directory.exists():
        parser.error("Choose a new directory; an existing directory is never replaced.")
    try:
        create_exercise(arguments.directory)
    except OSError as error:
        parser.error(str(error))
    print(f"Created synthetic inspection exercise: {arguments.directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
