"""Original-cohort statistics from verified saved work, without native reindexing."""

from copy import deepcopy

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_run_view,
    digest_score_method,
    digest_source_metadata,
)
from pharmacophoremt._private.arg_digestion.validation_results import CONFIG

from .saved_results import (
    _causes,
    _cohort,
    _compare,
    _error,
    _index,
    _records,
    _settings,
    _summarize,
)


@signal(tags=["validation", "screening", "saved_run"])
@arg_digest(config=CONFIG)
@attributed()
def summarize_screening_run(
    run_view,
    cohort,
    *,
    input_mapping,
    score_method,
    unscored=(),
    source_metadata=None,
    ef_fractions=(0.01, 0.05, 0.1),
    bedroc_alpha=20.0,
):
    """Analyze every declared saved work against an explicitly labelled cohort.

    ``run_view`` is a caller-owned open ``ScreeningRunView``. Each cohort record
    has a unique nonnegative integer input_index and binary integer label.
    ``input_mapping`` contains exactly work_key/input_index pairs, covering every
    declared work exactly once. Additional cohort entries require explicit
    upstream ``unscored`` causes with input_index, stage and reason. Source/work
    keys do not establish chemical identity, label authority or independence.

    The explicit unversioned score_method selects seeded_hit or
    checked_pose_coverage. It must agree with saved criteria and the recomputed
    native score must equal the stored score. No molecular access or rescreening
    occurs. Original native indices may be absent/repeated and remain unchanged.

    Returns schema pharmacophoremt.screening_run_summary@1 with existing metric
    settings/statistics and original/evaluated class counts. Pending work,
    confirmed native failure and upstream unavailability have separate counters
    and causes; missing work never becomes a negative. Records retain original
    cohort order, work_item and exact outcome envelopes, or None when absent.
    Run configuration and source metadata are detached. The view stays open.

    The complete manifest must be mapped; this function does not choose subsets
    or aggregate conformers/states. Undefined statistics remain None. Original
    attribution is retained separately from credit for newly executed analysis.
    These descriptive metrics do not establish predictive or biological validity.
    """
    digest_run_view(run_view)
    originals = _cohort(cohort)
    fractions, alpha = _settings(ef_fractions, bedroc_alpha)
    method = digest_score_method(score_method)
    if method is None:
        _error("score_method", "choose an explicit criterion")
    digest_source_metadata(source_metadata)
    configuration = run_view.configuration
    execution = configuration["context"].get("execution", {})
    if not isinstance(execution, dict):
        _error("run_view", "saved execution context must be a dictionary")
    declared = execution.get("score_method")
    if declared is not None and method != declared:
        _error("score_method", "requested criterion differs from saved execution")
    work = {row["work_key"]: row for row in run_view.work_items()}
    mapping, destinations = {}, set()
    for pair in _records(input_mapping, "input_mapping"):
        if pair.keys() != {"work_key", "input_index"}:
            _error("input_mapping", "expected only work_key and input_index")
        key = pair["work_key"]
        index = _index(pair["input_index"], "input_mapping")
        if not isinstance(key, str) or key not in work or key in mapping:
            _error("input_mapping", "duplicate or unknown declared work")
        if index not in originals or index in destinations:
            _error("input_mapping", "duplicate or unknown original input")
        mapping[key] = index
        destinations.add(index)
    if mapping.keys() != work.keys():
        _error("input_mapping", "map every declared work item exactly once")
    causes = _causes(
        originals, destinations, unscored, reserved_stages=("screening_run",)
    )
    upstream_count = len(causes)
    outcomes, by_original, stored_scores = {}, {}, {}
    for outcome in run_view.results():
        if outcome["score_method"] != method + "@1":
            _error("score_method", "saved outcomes use a different criterion")
        key = outcome["work_key"]
        index = mapping[key]
        outcomes[index] = outcome
        by_original[index] = outcome["native_result"]
        stored_scores[index] = outcome["ranking_score"]
        if "label" in by_original[index] and (
            type(by_original[index]["label"]) is not int
            or by_original[index]["label"] != originals[index]["label"]
        ):
            _error("evaluations", "native and original labels disagree")
    pending = destinations - outcomes.keys()
    for key, index in mapping.items():
        if index in pending:
            causes[index] = dict(
                input_index=index,
                stage="screening_run",
                reason="declared work has no confirmed outcome",
                work_key=key,
            )
    result = _summarize(
        originals,
        by_original,
        causes,
        method=method,
        fractions=fractions,
        alpha=alpha,
        input_mapping=input_mapping,
        source_metadata=source_metadata,
        stored_scores=stored_scores,
    )
    result.update(
        schema="pharmacophoremt.screening_run_summary@1",
        run_configuration=configuration,
        n_upstream_unscored=upstream_count,
        n_pending_work=len(pending),
    )
    work_by_original = {index: work[key] for key, index in mapping.items()}
    for row in result["records"]:
        index = row["input_index"]
        native = row.pop("native_evaluation")
        # The shared core already detached the native payload; envelope metadata
        # consists only of validated immutable scalar fields.
        outcome = outcomes.get(index)
        row["outcome"] = (
            None if outcome is None else dict(outcome, native_result=native)
        )
        row["work_item"] = deepcopy(work_by_original.get(index))
    return result


@signal(tags=["validation", "screening", "saved_run", "comparison"])
@arg_digest(config=CONFIG)
@attributed()
def compare_screening_runs(
    cohort, baseline, comparison, *, ef_fractions=(0.01, 0.05, 0.1), bedroc_alpha=20.0
):
    """Compare two verified saved runs on the same scored original samples.

    Parameters
    ----------
    cohort : list of dict
        The shared original labelled cohort accepted by summarize_screening_run.
        Original indices are unique nonnegative integers, and labels are binary
        integers. Sparse/reordered indices and repeated source keys are allowed;
        the caller owns label authority, chemical identity and independence.
    baseline, comparison : dict
        Each contains a caller-owned open ``run_view``, complete explicit
        ``input_mapping`` and ``score_method``, plus optional ``unscored`` and
        ``source_metadata`` accepted by summarize_screening_run. Both criteria
        must agree. Work keys may differ: only the declared original input
        mapping determines correspondence. Native batch indices remain original.
    ef_fractions, bedroc_alpha
        Identical existing metric settings for both complete arms and the
        common scored subset. No new metric definition or imputation is used.

    Returns
    -------
    dict
        Schema ``pharmacophoremt.screening_run_comparison@1`` with complete
        detached run summaries and recomputed common-subset statistics/deltas.
        The intersection preserves original cohort order and includes zero
        scores; pending, native-failed and upstream-unavailable samples remain
        separately counted in their full arms. Undefined metrics/deltas are None.

    Notes
    -----
    Views stay open and owned by the caller. No molecular access, reexecution,
    aggregation, work-key matching or source re-attribution occurs. Different
    queries/producers remain inspectable. Comparing the scored intersection
    does not remove selection bias, establish chemical/assay independence or
    demonstrate predictive/biological validity. Original source attribution is
    preserved separately from credit for newly executed analysis operations.
    """
    fractions, alpha = _settings(ef_fractions, bedroc_alpha)
    summaries = {}
    for name, arm in (("baseline", baseline), ("comparison", comparison)):
        if (
            not isinstance(arm, dict)
            or not {"run_view", "input_mapping", "score_method"} <= arm.keys()
            or arm.keys()
            - {
                "run_view",
                "input_mapping",
                "score_method",
                "unscored",
                "source_metadata",
            }
        ):
            _error(
                name,
                "expected a verified run view, mapping, criterion and optional causes/source metadata",
            )
        summaries[name] = summarize_screening_run(
            cohort=cohort, **arm, ef_fractions=fractions, bedroc_alpha=alpha
        )
    result = _compare(summaries, fractions, alpha)
    result["schema"] = "pharmacophoremt.screening_run_comparison@1"
    return result
