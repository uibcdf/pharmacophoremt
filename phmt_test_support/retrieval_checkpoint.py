"""Application-owned checkpoints for the two opt-in retrieval case drivers."""

import json
import os
import tempfile
from pathlib import Path


class RetrievalCheckpoint:
    """Retain progress and real session credit together on a caller-owned path.

    The driver reserves a new output before scientific imports. Replacement is
    atomic on the tested local filesystem; this is not a power-loss, concurrent
    writer, network-filesystem or general journal contract. No signal handler is
    installed: interruption leaves the last committed checkpoint authoritative.
    """

    def __init__(self, path, report, snapshot):
        self.path = Path(path)
        self.report = report
        self.snapshot = snapshot
        self.sequence = 0
        self.recorded_sequence = None

    def retain(self):
        sequence = self.sequence + 1
        actual = self.report.get("actual_attribution")
        attribution = {"status": "recorded", "recorded_sequence": sequence}
        try:
            observed = self.snapshot()
            json.dumps(observed, allow_nan=False)
            actual = observed
        except Exception as error:
            attribution = {
                "status": "unavailable",
                "recorded_sequence": self.recorded_sequence,
                "failure": {"type": type(error).__name__, "reason": str(error)},
            }
        checkpoint = {
            "schema": "pharmacophoremt.retrieval-driver-checkpoint@1",
            "sequence": sequence,
            "scope": "persisted application progress and observed session only",
            "uncommitted_work": "unknown",
            "attribution": attribution,
        }
        record = dict(self.report, checkpoint=checkpoint, actual_attribution=actual)
        raw = json.dumps(record, indent=2, allow_nan=False) + "\n"
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix="." + self.path.name + ".",
                suffix=".tmp",
                delete=False,
            ) as stream:
                temporary = Path(stream.name)
                stream.write(raw)
            os.replace(temporary, self.path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        self.sequence = sequence
        if attribution["status"] == "recorded":
            self.recorded_sequence = sequence
        self.report.update(checkpoint=checkpoint, actual_attribution=actual)
