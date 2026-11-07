"""Private streaming projections of the public saved-result view."""

import csv
import hashlib
import os
import tempfile
from contextlib import closing
from pathlib import Path

from ._diagnostics import ScreeningRunError
from ._store import canonical_json

_COLUMNS = (
    "work_key",
    "source_key",
    "occurrence_key",
    "status",
    "ranking_score",
    "score_method",
)


def _write(view, output, file_format):
    count = 0
    if file_format == "csv":
        writer = csv.DictWriter(output, fieldnames=_COLUMNS, lineterminator="\n")
        writer.writeheader()
    with closing(view.results()) as outcomes:
        for outcome in outcomes:
            if file_format == "jsonl":
                output.write(canonical_json(outcome) + "\n")
            else:
                writer.writerow(
                    {
                        name: (
                            outcome["native_result"]["status"]
                            if name == "status"
                            else outcome[name]
                        )
                        for name in _COLUMNS
                    }
                )
            count += 1
    return count


def _identity(path):
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            size += len(block)
            digest.update(block)
    return size, digest.hexdigest()


def export(view, path, file_format):
    """Publish a complete fresh file, retaining evidence of cleanup failures."""
    # Reject a closed view before touching the filesystem or pulling outcomes.
    configuration = view.configuration
    destination = Path(os.path.abspath(path))
    if os.path.lexists(destination):
        raise FileExistsError(f"export destination already exists: {destination}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".phmt-export-", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        try:
            output = os.fdopen(descriptor, "w", encoding="utf-8", newline="")
        except BaseException as error:
            try:
                os.close(descriptor)
            except OSError as cleanup_error:
                error.add_note(f"Could not close export descriptor: {cleanup_error}")
            raise
        with output:
            count = _write(view, output, file_format)
        size, digest = _identity(temporary)
        receipt = {
            "format": "pharmacophoremt.screening-export@1",
            "file_format": file_format,
            "path": str(destination),
            "encoding": "utf-8",
            "bytes": size,
            "sha256": digest,
            "configuration": configuration,
            "configuration_sha256": hashlib.sha256(
                canonical_json(configuration).encode("utf-8")
            ).hexdigest(),
            "exported_records": count,
            "pending_work": configuration["work_count"] - count,
            "published": True,
        }
        # Same-directory staging and an exclusive link protect concurrent files.
        # Unsupported filesystems fail rather than falling back to replacement.
        os.link(temporary, destination)
    except BaseException as error:
        try:
            temporary.unlink()
        except OSError as cleanup_error:
            error.add_note(
                f"Could not remove export staging file {temporary}: {cleanup_error}"
            )
        raise
    try:
        temporary.unlink()
    except OSError as error:
        raise ScreeningRunError(
            operation="clean up a published export",
            reason=str(error),
            published=True,
            receipt=receipt,
            temporary_path=str(temporary),
        ) from error
    return receipt
