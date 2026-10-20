"""Read checksum-qualified local evidence without executing scientific workflows.

The owning producer defines the result schema and scientific assertions. This
reader checks the existing gzip/JSON archive envelope only; it preserves failed,
partial and unknown result fields, and never grants scientific acceptance.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
from pathlib import Path


def _check_bytes(payload, identity, prefix):
    expected = identity.get(f"{prefix}_sha256")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError(f"Missing or invalid {prefix} SHA-256")
    if hashlib.sha256(payload).hexdigest() != expected:
        raise ValueError(f"{prefix.capitalize()} SHA-256 mismatch")
    size_key = f"{prefix}_bytes"
    size = identity.get(size_key)
    if size_key in identity and (type(size) is not int or size != len(payload)):
        raise ValueError(f"{prefix.capitalize()} byte count mismatch")


def read_archived_bytes(summary_path, *, identity_key="full_evidence"):
    """Return ``(summary, raw_bytes)`` after validating the archive envelope.

    Accept one sibling gzip named by the selected summary identity, requiring
    compressed/uncompressed SHA-256 and checking optional byte counts. Historical
    ``file`` names remain supported. Refuse absolute/traversal/escaping-symlink
    paths. No payload decoding, scientific imports, file writes or usage recording
    occur. Consumers own payload interpretation (including native molecular I/O).
    Invalid identity raises ValueError; unreadable/gzip bytes raise OSError.
    """
    summary_path = Path(summary_path).resolve()
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if not isinstance(summary, dict):
        raise ValueError("Evidence summary must be a JSON object")
    identity = summary.get(identity_key)
    if not isinstance(identity, dict):
        raise ValueError(f"Missing archive identity: {identity_key}")
    name = identity.get("path", identity.get("file"))
    if (
        not isinstance(name, str)
        or not name
        or Path(name).name != name
        or name in {".", ".."}
        or ("file" in identity and identity["file"] != name)
    ):
        raise ValueError("Archive identity must name one sibling file")
    archive_path = (summary_path.parent / name).resolve()
    if archive_path.parent != summary_path.parent:
        raise ValueError("Archive path escapes summary directory")
    compressed = archive_path.read_bytes()
    _check_bytes(compressed, identity, "compressed")
    raw = gzip.decompress(compressed)
    _check_bytes(raw, identity, "uncompressed")
    return summary, raw


def read_archived_evidence(summary_path, *, identity_key="full_evidence"):
    """Return ``(summary, original_report)`` from a verified gzip/JSON envelope.

    Reuse read_archived_bytes for path/identity validation, then require a JSON
    object. Preserve failed, partial and unknown fields. No scientific acceptance
    or citation registration is implied; invalid report JSON raises ValueError.
    """
    summary, raw = read_archived_bytes(summary_path, identity_key=identity_key)
    report = json.loads(raw)
    if not isinstance(report, dict):
        raise ValueError("Archived report must be a JSON object")
    return summary, report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path)
    parser.add_argument("--identity-key", default="full_evidence")
    args = parser.parse_args(argv)
    summary, report = read_archived_evidence(
        args.summary, identity_key=args.identity_key
    )
    print(
        json.dumps(
            {
                "scope": "archive integrity; scientific acceptance is producer-owned",
                "summary_schema": summary.get("schema"),
                "report_schema": report.get("schema"),
                "recorded_at_utc": report.get("recorded_at_utc"),
                "archive_bytes_verified": True,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
