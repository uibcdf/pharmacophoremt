"""Saved plans and recoverable native screening of producer-prepared inputs.

Molecular input correspondence remains the producer's responsibility. Exact
software/recipe binding permits conservative reexecution; it establishes neither
chemical identity nor complete provider/native provenance.
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

from argdigest import arg_digest
from smonitor import signal

import pharmacophoremt
import pharmacophoremt_results
from pharmacophoremt._private.arg_digestion.prepared_runs import CONFIG
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json
from pharmacophoremt_results import ScreeningRunStore, canonical_json

from .conformer_screening import ConformerScreening
from .pose_evaluation import PoseEvaluator
from .prepared_screening import PreparedInput, screen_prepared
from .rigid_search import RigidPoseSearch
from .scoring import _resolve_score_method

_PLAN_SCHEMA = "pharmacophoremt.prepared-run-plan@1"
_MAX_QUERY_BYTES = 2 * 1024 * 1024
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
    # The native codec owns schema and unit reconstruction. Retain exact bytes.
    with tempfile.TemporaryDirectory(prefix="phmt-prepared-query-") as directory:
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


def _source_digest(root):
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*.py")):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _runtime_identity():
    """Location-independent conservative binding, not provider/native closure."""
    versions = {}
    for name in (
        "molsysmt",
        "rdkit",
        "numpy",
        "scipy",
        "networkx",
        "argdigest",
        "smonitor",
        "depdigest",
        "pyunitwizard",
    ):
        versions[name] = metadata.version(name)
    return {
        "python": list(sys.version_info[:3]),
        "phmt_python_sources_sha256": _source_digest(
            Path(pharmacophoremt.__file__).resolve().parent
        ),
        "results_python_sources_sha256": _source_digest(
            Path(pharmacophoremt_results.__file__).resolve().parent
        ),
        "provider_versions": versions,
    }


def _declared_compatibility(compatibility):
    if not isinstance(compatibility, Mapping) or set(compatibility) != _COMPATIBILITY:
        raise ArgumentError(
            argument="compatibility", reason="declare all six compatibility boundaries"
        )
    for key in _COMPATIBILITY - {"index"}:
        if compatibility[key] is None:
            raise ArgumentError(argument=key, reason="an explicit identity is required")
    return json.loads(canonical_json(dict(compatibility)))


def _context(context_json):
    if type(context_json) is not str:
        raise ArgumentError(
            argument="context_json", reason="expected canonical JSON text"
        )
    try:
        context = json.loads(context_json)
        if canonical_json(context) != context_json:
            raise ValueError("plan context must be canonical finite JSON")
        if type(context) is not dict or set(context) != {
            "schema",
            "compatibility",
            "execution",
            "runtime",
        }:
            raise ValueError("unrecognized plan context")
        if context["schema"] != _PLAN_SCHEMA:
            raise ValueError("unsupported prepared-run plan schema")
        _declared_compatibility(context["compatibility"])
        execution = context["execution"]
        if type(execution) is not dict or set(execution) != {
            "screening_method",
            "score_method",
            "constructor_options",
            "evaluation_options",
            "on_error",
        }:
            raise ValueError("invalid saved execution recipe")
        if execution["screening_method"] not in _TOOLS:
            raise ValueError("unsupported saved screening method")
        if execution["score_method"] not in {"seeded_hit", "checked_pose_coverage"}:
            raise ValueError("unsupported saved score criterion")
        if execution["on_error"] not in {"raise", "record"}:
            raise ValueError("unsupported saved native error policy")
        for name in ("constructor_options", "evaluation_options"):
            if type(execution[name]) is not dict:
                raise ValueError("saved native options must be JSON objects")
            _options(execution[name], name)
        if type(context["runtime"]) is not dict:
            raise ValueError("saved runtime binding must be a JSON object")
    except (TypeError, ValueError, KeyError) as error:
        raise ArgumentError(argument="context_json", reason=str(error)) from error
    return context


@dataclass(frozen=True, repr=False)
class PreparedRunPlan:
    """Exact query bytes and a detached, versioned native execution recipe.

    Build plans with :func:`build_prepared_run_plan`. Fields are immutable;
    ``context`` returns a detached JSON record. The runtime fingerprint is a
    conservative exact-reexecution condition, not molecular identity. Moving
    unchanged artifacts is permitted; source/version changes require a newly
    reviewed plan/run even when chemistry is unchanged. Saved reading has no
    such current-runtime comparison and preserves original producer evidence.

    Use describe() to inspect exact query identity and the complete captured
    context without reconstruction or a current-runtime compatibility check.
    Console representation is compact and omits query/context payloads.
    """

    query_bytes: bytes
    context_json: str

    def __post_init__(self):
        if (
            type(self.query_bytes) is not bytes
            or len(self.query_bytes) > _MAX_QUERY_BYTES
        ):
            raise ArgumentError(
                argument="query_bytes",
                reason="expected exact query bytes at most 2 MiB",
            )
        _context(self.context_json)

    @property
    def context(self):
        """Return detached original declarations, execution and runtime binding."""
        return _context(self.context_json)

    def _description(self):
        return {
            "query": {
                "bytes": len(self.query_bytes),
                "sha256": hashlib.sha256(self.query_bytes).hexdigest(),
            },
            "context": self.context,
        }

    def __repr__(self):
        description = self._description()
        execution = description["context"]["execution"]
        query = description["query"]
        return (
            f"PreparedRunPlan(screening_method={execution['screening_method']!r}, "
            f"score_method={execution['score_method']!r}, "
            f"query_size_bytes={query['bytes']}, query_sha256={query['sha256']!r})"
        )

    @signal(tags=["screening", "prepared", "inspect"])
    @arg_digest(config=CONFIG)
    def describe(self):
        """Return detached query byte identity and the original complete context.

        The query record contains bytes and sha256 for the exact captured
        artifact, without its content or a molecular interpretation. The context
        preserves the existing schema, producer compatibility declarations,
        expanded native options/explicit units and original runtime binding.
        It may contain private caller metadata; inspection is not disclosure
        authorization, source authentication or admission for current execution.

        No query file or prepared input is read, no evaluator is reconstructed,
        no current runtime is checked and no scientific credit is earned.
        The returned finite JSON record is detached; changing it cannot change
        the frozen plan. It is not a new saved-plan format.
        """
        return self._description()

    @signal(tags=["screening", "prepared", "reconstruct"])
    @arg_digest(config=CONFIG)
    def new_evaluator(self):
        """Reconstruct a private native tool from captured bytes and saved options."""
        execution = self.context["execution"]
        return _TOOLS[execution["screening_method"]](
            _load_query(self.query_bytes), **execution["constructor_options"]
        )


def _current_plan(plan):
    if not isinstance(plan, PreparedRunPlan):
        raise ArgumentError(argument="plan", reason="expected a PreparedRunPlan")
    context = plan.context
    if context["runtime"] != _runtime_identity():
        raise ArgumentError(
            argument="plan",
            reason="software binding changed; review a new linked run, not molecular identity",
        )
    return context


def _bound_plan(ledger, plan):
    if not isinstance(ledger, ScreeningRunStore):
        raise ArgumentError(argument="ledger", reason="expected a ScreeningRunStore")
    # A closed writer fails before a reader is pulled or an evaluator created.
    ledger.expected(0)
    context = _current_plan(plan)
    if (
        ledger.query_bytes != plan.query_bytes
        or canonical_json(ledger.context) != plan.context_json
    ):
        raise ArgumentError(argument="plan", reason="incompatible saved run binding")
    return context


@signal(tags=["screening", "prepared", "plan"])
@arg_digest(config=CONFIG)
def build_prepared_run_plan(
    query_path,
    *,
    screening_method,
    score_method,
    compatibility,
    constructor_options=None,
    evaluation_options=None,
    on_error="record",
):
    """Capture query bytes, native effective settings and explicit declarations.

    ``compatibility`` has exactly ``prepared_snapshot``, ``preparation``,
    ``features``, ``index``, ``grouping`` and ``numerical``. All except ``index``
    require non-None producer declarations. These records do not authenticate
    molecular data. Options must be finite plain JSON; dimensional options use
    explicit native unit strings. The native constructor and empty-batch public
    preflight own scientific/option admission, without reading prepared inputs.

    Expanded defaults come from the defining native signatures. The plan keeps
    the exact native query artifact (at most 2 MiB), not its path. Query/recipe,
    source-code or declared compatibility changes require a separate run, with
    an optional parent link. Such changes do not prove a chemical difference.
    No whole-workflow attribution is earned by constructing this plan.
    """
    if screening_method not in _TOOLS:
        raise ArgumentError(argument="screening_method", reason="unknown native method")
    declared = _declared_compatibility(compatibility)
    with Path(query_path).open("rb") as stream:
        raw = stream.read(_MAX_QUERY_BYTES + 1)
    if len(raw) > _MAX_QUERY_BYTES:
        raise ArgumentError(argument="query_path", reason="native query exceeds 2 MiB")
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
        "schema": _PLAN_SCHEMA,
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
    return PreparedRunPlan(raw, canonical_json(context))


@signal(tags=["screening", "prepared", "resume"])
@arg_digest(config=CONFIG)
def resume_prepared_run(ledger, inputs, *, plan):
    """Return newly confirmed outcomes; saved ``results()`` is the complete view.

    Binding checks happen now, before ``iter(inputs)``. Reopen caller-owned
    prepared inputs from their declared beginning: every mapping, including
    confirmed work, must match the ordered manifest. Already confirmed failures
    remain terminal and unscored. Retrying them uses a separate linked run.

    Native evaluation occurs on consumption. Started/staged attempts remain
    retained; interrupted unconfirmed work may be recomputed. Confirmation is
    atomic before yield, so interruption between commit and yield can leave a
    saved result not delivered to this iterator. Use the saved complete view for
    authoritative export. Exactly-once computation/external delivery, power-loss
    durability, provider seek/snapshot authentication and parallel writing are
    not established. Closing this iterator never explicitly closes its caller's
    reader or store; manage their lifetimes separately.
    """
    context = _bound_plan(ledger, plan)
    execution = context["execution"]
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


class PreparedScreeningRun:
    """Own one compatible writer and plan for a recoverable prepared-input task.

    Use ``create`` for a fresh destination or ``open`` for a matching saved run;
    both return a context manager. Only the writer is owned. Input readers and
    original query/manifest files remain caller-owned. One consumer owns the
    writer; use a closed read-only ``ScreeningRunView`` for historical analysis.
    Public creation/opening never overwrites or silently upgrades a legacy run.
    """

    @signal(tags=["screening", "prepared", "run"])
    @arg_digest(config=CONFIG)
    def __init__(self, store, *, plan):
        _bound_plan(store, plan)
        self._store = store
        self._plan = plan

    @classmethod
    @signal(tags=["screening", "prepared", "create"])
    @arg_digest(config=CONFIG)
    def create(cls, path, *, plan, manifest_path, run_id, parent_run_id=None):
        """Create one new public-format run without replacing existing files."""
        _current_plan(plan)
        store = ScreeningRunStore.create(
            path,
            run_id=run_id,
            parent_run_id=parent_run_id,
            query_bytes=plan.query_bytes,
            context=plan.context,
            manifest_path=manifest_path,
        )
        try:
            return cls(store, plan=plan)
        except BaseException:
            store.close()
            raise

    @classmethod
    @signal(tags=["screening", "prepared", "open"])
    @arg_digest(config=CONFIG)
    def open(cls, path, *, plan, manifest_path):
        """Open matching query/recipe/manifest/software; never create a missing run."""
        _current_plan(plan)
        store = ScreeningRunStore.open(
            path,
            query_bytes=plan.query_bytes,
            context=plan.context,
            manifest_path=manifest_path,
        )
        try:
            return cls(store, plan=plan)
        except BaseException:
            store.close()
            raise

    @property
    def run_id(self):
        return self._store.run_id

    @property
    def parent_run_id(self):
        return self._store.parent_run_id

    @property
    def query_bytes(self):
        return self._store.query_bytes

    @property
    def context(self):
        return self._store.context

    @signal(tags=["screening", "prepared", "resume"])
    @arg_digest(config=CONFIG)
    def resume(self, inputs):
        """Preflight now and confirm/yield new work lazily from the original order."""
        return resume_prepared_run(self._store, inputs, plan=self._plan)

    def results(self):
        """Read every saved terminal outcome in manifest order, including failures."""
        return self._store.results()

    @signal(tags=["screening", "prepared", "attempts"])
    @arg_digest(config=CONFIG)
    def attempts(self, work_key):
        """Inspect retained attempts without evaluating or retrying work."""
        return self._store.attempts(work_key)

    @signal(tags=["screening", "prepared", "progress"])
    @arg_digest(config=CONFIG)
    def summary(self):
        """Inspect work/attempt coverage using this plan's saved score criterion.

        Counts refer to work items, not independent compounds. Complete declared
        work may include terminal failures; it does not establish biological or
        chemical completeness. This scans stored evidence, without new science.
        """
        method = self._plan.context["execution"]["score_method"] + "@1"
        return self._store.summary(score_method=method)

    @signal(tags=["screening", "prepared", "ranking"])
    @arg_digest(config=CONFIG)
    def top_results(self, *, limit=10):
        """Select observed scored work under the saved criterion and stable ties.

        Pending/failed work remains outside this observed ranking; valid zero
        nonmatches are eligible scored observations. This is a scan retaining
        at most ``limit`` payloads, not an index or a proven global hit ranking.
        Returned evidence remains caller-owned and can contain native geometry.
        """
        method = self._plan.context["execution"]["score_method"] + "@1"
        return self._store.top_results(score_method=method, limit=limit)

    def close(self):
        """Release only the owned writer connection; caller readers stay owned."""
        self._store.close()

    def __enter__(self):
        self._store.expected(0)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
