"""Unshipped workflow exercise over the bounded store; no query admission."""

import json

from phmt_test_support.feature_snapshot import FeatureSnapshotStudy, _request
from phmt_test_support.feature_store import (
    SCHEMA as STORE_SCHEMA,
)
from phmt_test_support.feature_store import (
    FeatureStoreReaderStudy,
    FeatureStoreStudy,
    _digest,
)
from phmt_test_support.search_asset_contract import family_coverage

SCHEMA = "pharmacophoremt.feature-store-workflow-study@1"
_UNSET = object()
MESSAGES = {
    "validate_quantities": "Validate the original quantities before reusing these captured features.",
    "empty_selection": "The selected inventory is empty; no source-level negative is established.",
    "evaluate_missing_families": "Evaluate the missing families explicitly before reusing this selection.",
    "resolve_incomplete_extraction": "Resolve the recorded incomplete extractions before reusing this selection.",
    "unknown_work_key": "Choose exact work keys from the inspected manifest, preserving spaces and case.",
    "generation_mismatch": "Reinspect the intended generation and explicitly choose its features.",
    "invalid_quantities": "The original quantities failed validation; inspect the cause before preparing replacement features.",
    "captured_features_ready": "Captured features passed quantity validation; query and source admission remain separate.",
    "candidate_is_current": "The candidate is published now. Use that generation; no publication retry is needed.",
    "candidate_not_current": "The candidate is not current. Validate it again before an explicit linked publication retry.",
    "publication_changed": "Another generation is current. Review it before requesting a different publication.",
    "writer_busy": "A writer holds this store. Close that writer before inspecting recovery or requesting a retry.",
    "unknown_attempt": "Choose an exact retained publication attempt identifier.",
    "not_publication_attempt": "This attempt is not a publication. Inspect its operation before choosing recovery.",
    "invalid_attempt": "The retained publication receipt is inconsistent; preserve it for inspection.",
    "inconsistent_reader": "Open the current generation while holding this writer before inspecting recovery.",
    "closed_session": "This session is closed. Open a new session explicitly.",
}


def _copy(value):
    from pharmacophoremt_results import canonical_json

    return json.loads(canonical_json(value))


def _decision(code):
    return {"code": code, "message": MESSAGES[code]}


class WorkflowRefusalStudy(ValueError):
    """Application-study refusal report; not a public PHMT diagnostic code."""

    def __init__(self, code, report=None):
        self.report = _copy({} if report is None else report)
        self.report["decision"] = _decision(code)
        self.code = code
        super().__init__(MESSAGES[code])


def _selection(work_keys):
    if work_keys is None:
        return None
    if not isinstance(work_keys, (list, tuple)) or any(
        type(k) is not str or not k or len(k.encode()) > 512 for k in work_keys
    ):
        raise ValueError("Choose a finite list of literal work keys")
    if len(work_keys) > 12 or len(set(work_keys)) != len(work_keys):
        raise ValueError("Choose at most twelve unique work keys")
    return set(work_keys)


def inspect_reuse(reader, required_families, *, work_keys=None):
    """Inspect a pinned selection without quantity interpretation or matching."""
    required = _request(required_families)
    selected = _selection(work_keys)
    try:
        description = reader.describe()
    except ValueError as error:
        raise WorkflowRefusalStudy("closed_session") from error
    records = description["records"]
    unknown = (
        [] if selected is None else sorted(selected - {r["work_key"] for r in records})
    )
    report = {
        "schema": SCHEMA,
        "operation": "inspect_captured_features",
        "generation": description["generation"],
        "required_families": required,
        "manifest_complete": description["complete"],
        "manifest_occurrence_count": len(records),
        "scope": "captured-inventory-only",
        "currentness": "pinned-generation; current alias not checked",
        "query_admitted": None,
        "match_outcome": None,
        "molecular_origin_authenticated": False,
        "quantity_semantics_checked": False,
        "occurrences": [],
    }
    if unknown:
        report["unknown_work_keys"] = unknown
        raise WorkflowRefusalStudy("unknown_work_key", report)
    for ordinal, row in enumerate(records):
        if selected is not None and row["work_key"] not in selected:
            continue
        occurrence = {"work_ordinal": ordinal, **row}
        if row["status"] == "ready":
            occurrence["coverage"] = family_coverage(
                FeatureSnapshotStudy(reader.snapshot(ordinal)), required
            )
        report["occurrences"].append(occurrence)
    rows = report["occurrences"]
    if any(r["status"] != "ready" for r in rows):
        code = "resolve_incomplete_extraction"
    elif any(not r["coverage"]["family_coverage_complete"] for r in rows):
        code = "evaluate_missing_families"
    else:
        code = "validate_quantities" if rows else "empty_selection"
    report["selected_extraction_complete"] = all(r["status"] == "ready" for r in rows)
    report["selected_family_evaluation_complete"] = all(
        r["status"] == "ready" and r["coverage"]["family_coverage_complete"]
        for r in rows
    )
    report["selection_ordinals"] = [r["work_ordinal"] for r in rows]
    report["decision"] = _decision(code)
    return report


def prepare_reuse(reader, required_families, *, expected_generation, work_keys=None):
    """Reinspect and decode original inventories; no cached admission token."""
    _digest(expected_generation)
    report = inspect_reuse(reader, required_families, work_keys=work_keys)
    if report["generation"] != expected_generation:
        raise WorkflowRefusalStudy("generation_mismatch", report)
    code = report["decision"]["code"]
    if code not in {"validate_quantities", "empty_selection"}:
        raise WorkflowRefusalStudy(code, report)
    inventories = []
    for row in report["occurrences"]:
        ordinal = row["work_ordinal"]
        try:
            inventory = reader.inventory(ordinal)
        except Exception as error:
            report["quantity_failure"] = {
                "work_ordinal": ordinal,
                "work_key": row["work_key"],
                "type": type(error).__name__,
                "previously_validated_ordinals": [
                    r["work_ordinal"] for r in inventories
                ],
            }
            raise WorkflowRefusalStudy("invalid_quantities", report) from error
        inventories.append(
            {
                "work_ordinal": ordinal,
                "work_key": row["work_key"],
                "inventory": inventory,
            }
        )
    report["quantity_semantics_checked"] = True
    report["decision"] = _decision(
        "captured_features_ready" if inventories else "empty_selection"
    )
    return {"report": report, "inventories": inventories}


def explain_reuse(report):
    """Application text from the same report; no diagnostic renderer copy."""
    lines = [report["decision"]["message"]]
    for row in report.get("occurrences", []):
        if row["status"] != "ready":
            lines.append(
                f"{row['work_key']!r}: {row['status']}; {row['cause']['reason']}"
            )
        elif row["coverage"]["unobserved_families"]:
            lines.append(
                f"{row['work_key']!r}: missing evaluation for {', '.join(row['coverage']['unobserved_families'])}."
            )
    return "\n".join(lines)


def _publication_attempt(writer, attempt):
    if type(attempt) is not str:
        raise ValueError("Choose a literal retained attempt identifier")
    row = next((r for r in writer.attempts() if r["attempt"] == attempt), None)
    if row is None:
        raise WorkflowRefusalStudy("unknown_attempt")
    started = row["started"]
    if started.get("operation") != "publish":
        raise WorkflowRefusalStudy("not_publication_attempt")
    base = {
        "schema",
        "attempt",
        "operation",
        "retry_of",
        "candidate",
        "expected_current",
    }
    if set(started) != base or started["schema"] != STORE_SCHEMA:
        raise WorkflowRefusalStudy("invalid_attempt")
    try:
        _digest(started["candidate"])
        if started["expected_current"] is not None:
            _digest(started["expected_current"])
    except ValueError as error:
        raise WorkflowRefusalStudy("invalid_attempt") from error
    terminal = row.get("terminal")
    if terminal is not None:
        state = terminal.get("state")
        extra = (
            {"state", "result"}
            if state == "completed"
            else {"state", "exception_type", "reason", "reason_truncated"}
        )
        if (
            type(state) is not str
            or state not in {"completed", "raised"}
            or set(terminal) != base | extra
            or any(terminal[k] != started[k] for k in base)
            or (state == "completed" and terminal["result"] != started["candidate"])
        ):
            raise WorkflowRefusalStudy("invalid_attempt")
    return row


def inspect_publication_recovery(writer, current_reader, attempt):
    """Observe visibility under the caller's writer lease; perform no retry."""
    current = writer.current()
    if current is None:
        if current_reader is not None:
            raise WorkflowRefusalStudy("inconsistent_reader")
    elif (
        current_reader is None
        or current_reader.describe()["generation"] != current
        or not current_reader.describe()["complete"]
    ):
        raise WorkflowRefusalStudy("inconsistent_reader")
    row = _publication_attempt(writer, attempt)
    started = row["started"]
    if current == started["candidate"]:
        code = "candidate_is_current"
    elif current == started["expected_current"]:
        code = "candidate_not_current"
    else:
        code = "publication_changed"
    return {
        "schema": SCHEMA,
        "operation": "inspect_publication_recovery",
        "attempt": attempt,
        "attempt_state": row["state"],
        "original_attempt": _copy(row),
        "current_generation": current,
        "candidate": started["candidate"],
        "candidate_is_current": current == started["candidate"],
        "candidate_validation": "not_performed; required again before retry",
        "historical_publication": "completed receipt claim"
        if row["state"] == "completed"
        else "unknown",
        "rollback_inferred": False,
        "automatic_retry": False,
        "decision": _decision(code),
    }


def retry_publication(writer, current_reader, attempt, *, expected_current):
    """Explicit linked retry, refusing a currently published or displaced candidate."""
    if expected_current is not None:
        _digest(expected_current)
    report = inspect_publication_recovery(writer, current_reader, attempt)
    code = report["decision"]["code"]
    if code != "candidate_not_current":
        raise WorkflowRefusalStudy(code, report)
    if expected_current != report["current_generation"]:
        raise WorkflowRefusalStudy("publication_changed", report)
    generation = writer.publish(
        report["candidate"], expected_current=expected_current, retry_of=attempt
    )
    return {
        "recovery_before_retry": report,
        "published_generation": generation,
        "retry_of": attempt,
    }


def recover_publication(root, attempt, *, retry=False, expected_current=_UNSET):
    """Guided composition; the existing writer owns admission and publication."""
    if type(retry) is not bool:
        raise ValueError("retry must be explicit boolean")
    if retry and expected_current is _UNSET:
        raise ValueError("An explicit retry requires expected_current, including None")
    if not retry and expected_current is not _UNSET:
        raise ValueError("expected_current applies only to an explicit retry")
    try:
        writer = FeatureStoreStudy(root)
    except BlockingIOError as error:
        raise WorkflowRefusalStudy("writer_busy") from error
    with writer:
        current = writer.current()
        reader = None if current is None else FeatureStoreReaderStudy(root)
        try:
            if retry:
                return retry_publication(
                    writer, reader, attempt, expected_current=expected_current
                )
            return inspect_publication_recovery(writer, reader, attempt)
        finally:
            if reader is not None:
                reader.close()


class FeatureStoreWorkflowStudy:
    """Guided session owning one reader; expert operations borrow their reader."""

    def __init__(self, root, generation=None):
        self._reader = FeatureStoreReaderStudy(root, generation)
        self._closed = False

    def _open(self):
        if self._closed:
            raise WorkflowRefusalStudy("closed_session")

    def inspect(self, required_families, *, work_keys=None):
        self._open()
        return inspect_reuse(self._reader, required_families, work_keys=work_keys)

    def reuse(self, required_families, *, expected_generation, work_keys=None):
        self._open()
        return prepare_reuse(
            self._reader,
            required_families,
            expected_generation=expected_generation,
            work_keys=work_keys,
        )

    def close(self):
        self._reader.close()
        self._closed = True

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, *args):
        self.close()
