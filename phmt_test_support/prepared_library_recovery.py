"""Unshipped saved-query composition and recovery experiment for #108.

Molecular input authentication remains the producer's responsibility. The
reference store owns confirmed publication, not exactly-once external delivery.
"""

import hashlib
import inspect
import json
import sys
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

import pharmacophoremt
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json
from pharmacophoremt.screening import (
    ConformerScreening,
    PoseEvaluator,
    RigidPoseSearch,
)
from pharmacophoremt.screening.scoring import _resolve_score_method
from phmt_test_support.prepared_library_reference import PreparedInput, screen_prepared
from phmt_test_support.reference_run_store import canonical_json

_TOOLS = {
    "placed": PoseEvaluator,
    "rigid": RigidPoseSearch,
    "conformers": ConformerScreening,
}
_COMPATIBILITY = {
    "prepared_snapshot",
    "preparation",
    "features",
    "index",
    "grouping",
    "numerical",
}


def _load_query(raw):
    # Public native I/O remains the schema/unit authority. The exact saved
    # artifact is copied once into an owned temporary file, never reserialized.
    with tempfile.TemporaryDirectory(prefix="phmt-reference-query-") as directory:
        path = Path(directory) / "query.json"
        path.write_bytes(raw)
        return load_json(str(path))


def _options(values, argument):
    if values is not None and not isinstance(values, Mapping):
        raise ArgumentError(argument=argument, reason="expected JSON option mapping")
    output = json.loads(canonical_json(dict(values or {})))
    if {"skip_digestion", "pose_id", "on_error"} & output.keys():
        raise ArgumentError(argument=argument, reason="reserved execution options")
    return output


def _defaults(function, positional, options, excluded):
    bound = inspect.signature(function).bind_partial(*positional, **options)
    bound.apply_defaults()
    return {key: value for key, value in bound.arguments.items() if key not in excluded}


def _runtime_identity():
    """Conservative PHMT-code/version binding, not complete provider closure."""
    root = Path(pharmacophoremt.__file__).resolve().parent
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*.py")):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    own = {
        name: hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
        for name in (
            "prepared_library_reference.py",
            "prepared_library_recovery.py",
            "reference_run_store.py",
        )
    }
    versions = {}
    for name in ("molsysmt", "argdigest", "smonitor", "pyunitwizard", "numpy", "scipy"):
        versions[name] = metadata.version(name)
    return {
        "python": list(sys.version_info[:3]),
        "phmt_python_sources_sha256": digest.hexdigest(),
        "reference_sources": own,
        "provider_versions": versions,
    }


@dataclass(frozen=True)
class RecoveryPlan:
    """Exact saved query and detached resolved recipe; experimental, unshipped."""

    query_bytes: bytes
    context_json: str

    @property
    def context(self):
        return json.loads(self.context_json)

    def new_evaluator(self):
        execution = self.context["execution"]
        return _TOOLS[execution["screening_method"]](
            _load_query(self.query_bytes), **execution["constructor_options"]
        )


def build_recovery_plan(
    query_path,
    *,
    screening_method,
    score_method,
    compatibility,
    constructor_options=None,
    evaluation_options=None,
    on_error="record",
):
    """Bind saved query bytes, explicit JSON settings and declared compatibility.

    Compatibility records prepared_snapshot/preparation/features/index/grouping/
    numerical identities. They must be supplied by the qualified producer; names
    and hashes do not authenticate a molecular snapshot. Native constructors and
    an empty reference screen perform scientific/option preflight. Defaults are
    expanded from their defining signatures; unit strings retain their spelling.
    """
    if screening_method not in _TOOLS:
        raise ArgumentError(argument="screening_method", reason="unknown native method")
    if not isinstance(compatibility, Mapping) or set(compatibility) != _COMPATIBILITY:
        raise ArgumentError(
            argument="compatibility", reason="declare all six compatibility boundaries"
        )
    for key in _COMPATIBILITY - {"index"}:
        if compatibility[key] is None:
            raise ArgumentError(argument=key, reason="an explicit identity is required")
    declared = json.loads(canonical_json(dict(compatibility)))
    with Path(query_path).open("rb") as stream:
        raw = stream.read(2 * 1024 * 1024 + 1)
    if len(raw) > 2 * 1024 * 1024:
        raise ArgumentError(
            argument="query_path", reason="reference query exceeds 2 MiB"
        )
    constructor = _options(constructor_options, "constructor_options")
    evaluation = _options(evaluation_options, "evaluation_options")
    tool = _TOOLS[screening_method]
    query = _load_query(raw)
    evaluator = tool(query, **constructor)
    method = _resolve_score_method(evaluator, score_method)
    screen_prepared(
        (),
        evaluator,
        score_method=method,
        on_error=on_error,
        evaluation_options=evaluation,
    ).close()
    constructor = _defaults(
        tool.__init__, (None, query), constructor, {"self", "pharmacophore"}
    )
    evaluation = _defaults(
        tool.evaluate,
        (None, None),
        evaluation,
        {"self", "molecular_system", "pose_id", "on_error"},
    )
    context = {
        "schema": "phmt.reference-recovery-plan@1",
        "compatibility": declared,
        "execution": {
            "screening_method": screening_method,
            "score_method": method,
            "constructor_options": constructor,
            "evaluation_options": evaluation,
            "on_error": on_error,
        },
        "runtime": _runtime_identity(),
    }
    return RecoveryPlan(raw, canonical_json(context))


def resume_prepared(ledger, inputs, *, plan):
    """Confirm/yield only new outcomes; use ledger.results() for the full view.

    Reopen the producer-owned source from its declared beginning. Every entry,
    including committed entries, must match the ordered manifest. No seek/reader
    closure is assumed. Uncommitted attempts may be recomputed; committed terminal
    failures are skipped like every other confirmed outcome. A crash between
    commit and yield cannot guarantee delivery to an external consumer.
    """
    if (
        ledger.query_bytes != plan.query_bytes
        or canonical_json(ledger.context) != plan.context_json
    ):
        raise ArgumentError(argument="plan", reason="incompatible saved run binding")
    if plan.context["runtime"] != _runtime_identity():
        raise ArgumentError(
            argument="plan", reason="runtime changed since plan construction"
        )
    execution = plan.context["execution"]
    evaluator = plan.new_evaluator()
    current = {}

    def pending():
        ordinal = 0
        for entry in inputs:
            if not isinstance(entry, PreparedInput):
                raise ArgumentError(
                    argument="inputs", reason="expected PreparedInput entries"
                )
            actual = {
                key: getattr(entry, key)
                for key in ("work_key", "source_key", "occurrence_key")
            }
            if actual != ledger.expected(ordinal):
                raise ArgumentError(
                    argument="inputs", reason="work manifest correspondence changed"
                )
            ordinal += 1
            if ledger.committed(entry.work_key) is None:
                current["attempt"] = ledger.begin(entry.work_key)
                yield entry
        if ledger.expected(ordinal) is not None:
            raise ArgumentError(
                argument="inputs", reason="source ended before declared work"
            )

    outcomes = screen_prepared(
        pending(),
        evaluator,
        score_method=execution["score_method"],
        on_error=execution["on_error"],
        evaluation_options=execution["evaluation_options"],
    )

    def confirmed():
        try:
            for outcome in outcomes:
                ledger.stage(current["attempt"], outcome)
                ledger.publish(current["attempt"])
                yield outcome
        finally:
            outcomes.close()

    return confirmed()
