"""Original-cohort accounting and paired statistics over detached native evidence."""

import math
from copy import deepcopy

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_score_method,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.screening import get_screening_score

from .metrics import _positive, bedroc, enrichment_factor, roc_auc


def _error(argument, reason):
    raise ArgumentError(argument=argument, reason=reason)


def _records(value, argument):
    if not isinstance(value, (list, tuple)) or any(
        not isinstance(row, dict) for row in value
    ):
        _error(argument, "expected a list of records")
    return value


def _index(value, argument):
    if type(value) is not int or value < 0:
        _error(argument, "indices must be nonnegative integers")
    return value


def _cohort(cohort):
    result = {}
    for row in _records(cohort, "cohort"):
        index = _index(row.get("input_index"), "cohort")
        if index in result:
            _error("cohort", "duplicate original input index")
        if type(row.get("label")) is not int or row["label"] not in (0, 1):
            _error("cohort", "each original input requires a binary integer label")
        result[index] = row
    return result


def _settings(ef_fractions, bedroc_alpha):
    try:
        fractions = tuple(ef_fractions)
    except TypeError as error:
        raise ArgumentError(
            argument="ef_fractions", reason="expected a sequence of fractions"
        ) from error
    fractions = tuple(_positive(f, "ef_fractions", maximum=1) for f in fractions)
    keys = [f"EF@{100 * f:g}%" for f in fractions]
    if len(set(keys)) != len(keys):
        _error("ef_fractions", "fractions must have distinct reported keys")
    return fractions, _positive(bedroc_alpha, "bedroc_alpha")


def _metrics(rows, fractions, alpha):
    labels, scores = [r["label"] for r in rows], [r["score"] for r in rows]
    result = {
        "n_evaluated": len(rows),
        "n_actives": sum(labels),
        "n_inactives": len(rows) - sum(labels),
        "AUC": roc_auc(labels, scores) if rows else None,
        "BEDROC": bedroc(labels, scores, alpha) if rows else None,
    }
    for fraction in fractions:
        result[f"EF@{100 * fraction:g}%"] = (
            enrichment_factor(labels, scores, fraction) if rows else None
        )
    return {
        key: None if isinstance(value, float) and not math.isfinite(value) else value
        for key, value in result.items()
    }


@signal(tags=["validation", "screening", "summary"])
@arg_digest()
@attributed()
def summarize_screening_results(
    cohort,
    evaluations,
    *,
    input_mapping,
    score_method,
    unscored=(),
    source_metadata=None,
    ef_fractions=(0.01, 0.05, 0.1),
    bedroc_alpha=20.0,
):
    """Summarize saved native evaluations against every original sample.

    Parameters
    ----------
    cohort : list of dict
        Original records with unique nonnegative integer ``input_index`` and
        integer ``label`` (1 active, 0 inactive). Sparse indices are supported.
        Optional source identities and other metadata are retained. Repeated
        source identities denote distinct samples when their indices differ.
    evaluations : list of dict
        Detached native results, each with its native ``input_index``. Failed
        native results remain failures. Completed seed-only negatives need no
        fitted pose. Optional evaluation labels must agree with the cohort.
    input_mapping : list of dict
        Exactly one ``native_input_index`` / original ``input_index`` pair per
        evaluation. Neither side may repeat. Order need not match the results.
    score_method : {'seeded_hit', 'checked_pose_coverage'}
        Explicit existing native criterion; recorded as version ``@1``.
    unscored : list of dict, optional
        Original ``input_index``, nonempty ``stage`` and ``reason`` for each
        upstream unavailable input. Stages ``search`` and ``native_evaluation``
        are reserved for native failures. Every original input must occur
        exactly once in either this
        list or the mapping; missing, unknown and overlapping indices are errors.
    source_metadata : dict, optional
        Detached producer, query identities or source attribution, preserved
        separately from attribution of the newly computed summary.
    ef_fractions : sequence of float, optional
        Fractions in (0, 1] for the existing tie-aware enrichment factor.
    bedroc_alpha : float, optional
        Positive finite exponential ranking parameter.

    Returns
    -------
    dict
        Original-order records containing detached ``cohort``, native evidence,
        score and explicit unscored cause; full class/failure counts; evaluated
        indices/labels/scores; statistics over scored inputs only. Undefined
        statistics are None. Binary missing-score AUC sensitivity uses explicit
        worst/best label-dependent hypothetical 0/1 scores, never imputation.

    Notes
    -----
    No molecular access, preparation, search or source re-attribution occurs.
    New metric calculations use the existing public metric contracts. Original
    inputs and producer/source attribution are copied without modification.
    Missing results never become negative scores. Single-class AUC/BEDROC and
    all empty-subset metrics are undefined; no-active EF retains its native zero.
    These descriptive statistics do not establish affinity or predictive validity.

    Examples
    --------
    After MolSysMT preparation and native screening, use the saved batch results:

    >>> summary = summarize_screening_results(
    ...     [{'input_index': 10, 'label': 1}], saved_evaluations,
    ...     input_mapping=[{'native_input_index': 0, 'input_index': 10}],
    ...     score_method='seeded_hit')
    """
    originals = _cohort(cohort)
    fractions, alpha = _settings(ef_fractions, bedroc_alpha)
    method = digest_score_method(score_method)
    if method is None:
        _error("score_method", "choose an explicit criterion")
    if source_metadata is not None and not isinstance(source_metadata, dict):
        _error("source_metadata", "expected a dictionary or None")
    mapping, destinations = {}, set()
    for pair in _records(input_mapping, "input_mapping"):
        if pair.keys() != {"native_input_index", "input_index"}:
            _error("input_mapping", "expected only native_input_index and input_index")
        native = _index(pair.get("native_input_index"), "input_mapping")
        original = _index(pair.get("input_index"), "input_mapping")
        if native in mapping or original in destinations or original not in originals:
            _error("input_mapping", "duplicate or unknown input mapping")
        mapping[native] = original
        destinations.add(original)
    native_results = {}
    for result in _records(evaluations, "evaluations"):
        native = _index(result.get("input_index"), "evaluations")
        if native in native_results or native not in mapping:
            _error("evaluations", "duplicate or unmapped native input index")
        if "label" in result and (
            type(result["label"]) is not int
            or result["label"] != originals[mapping[native]]["label"]
        ):
            _error("evaluations", "native and original labels disagree")
        native_results[native] = result
    if native_results.keys() != mapping.keys():
        _error("input_mapping", "every mapping requires one native evaluation")
    causes = {}
    for cause in _records(unscored, "unscored"):
        index = _index(cause.get("input_index"), "unscored")
        if index not in originals or index in causes or index in destinations:
            _error("unscored", "duplicate, unknown or already mapped original input")
        if any(
            not isinstance(cause.get(key), str) or not cause[key].strip()
            for key in ("stage", "reason")
        ) or cause["stage"] in {"search", "native_evaluation"}:
            _error("unscored", "declare an upstream stage and a nonempty reason")
        causes[index] = cause
    if destinations | causes.keys() != originals.keys():
        _error("cohort", "every original input needs native evidence or a cause")
    by_original = {mapping[native]: result for native, result in native_results.items()}
    records, stages = [], {}
    for index, original in originals.items():
        result = by_original.get(index)
        score = (
            None if result is None else get_screening_score(result, score_method=method)
        )
        cause = causes.get(index)
        if result is not None and score is None:
            cause = {
                "input_index": index,
                "stage": "native_evaluation",
                "reason": "native failure",
                "error": deepcopy(result.get("error")),
            }
        if cause is not None:
            stages[cause["stage"]] = stages.get(cause["stage"], 0) + 1
        records.append(
            {
                "input_index": index,
                "label": original["label"],
                "cohort": deepcopy(original),
                "score": score,
                "native_evaluation": deepcopy(result),
                "unscored_cause": deepcopy(cause),
            }
        )
    scored = [row for row in records if row["score"] is not None]
    labels = [row["label"] for row in scored]
    sensitivity = None
    if method == "seeded_hit" and records:
        full_labels = [row["label"] for row in records]
        sensitivity = {}
        for name, optimistic in (
            ("pessimistic_hypothetical", False),
            ("optimistic_hypothetical", True),
        ):
            scores = [
                row["score"]
                if row["score"] is not None
                else float(row["label"] if optimistic else 1 - row["label"])
                for row in records
            ]
            value = roc_auc(full_labels, scores)
            sensitivity[name] = value if math.isfinite(value) else None
    return {
        "schema": "pharmacophoremt.screening_summary@1",
        "score_method": method + "@1",
        "metric_settings": {"ef_fractions": list(fractions), "bedroc_alpha": alpha},
        "n_total": len(records),
        "n_actives": sum(row["label"] for row in records),
        "n_inactives": sum(1 - row["label"] for row in records),
        "n_evaluated": len(scored),
        "n_actives_evaluated": sum(labels),
        "n_inactives_evaluated": len(labels) - sum(labels),
        "n_actives_found": sum(
            row["label"] == 1 and row["native_evaluation"]["status"] == "matched"
            for row in scored
        ),
        "n_inactives_found": sum(
            row["label"] == 0 and row["native_evaluation"]["status"] == "matched"
            for row in scored
        ),
        "n_unscored": len(records) - len(scored),
        "n_actives_unscored": sum(r["label"] for r in records) - sum(labels),
        "n_inactives_unscored": sum(1 - r["label"] for r in records)
        - len(labels)
        + sum(labels),
        "n_native_failed": sum(
            r.get("status") == "failed" for r in native_results.values()
        ),
        "n_upstream_unscored": len(causes),
        "unscored_by_stage": stages,
        "evaluated_indices": [row["input_index"] for row in scored],
        "labels": labels,
        "scores": [row["score"] for row in scored],
        "metrics": _metrics(scored, fractions, alpha),
        "missing_binary_score_AUC_sensitivity": sensitivity,
        "records": records,
        "input_mapping": deepcopy(list(input_mapping)),
        "source_metadata": deepcopy(source_metadata),
    }


@signal(tags=["validation", "screening", "comparison"])
@arg_digest()
@attributed()
def compare_screening_results(
    cohort, baseline, comparison, *, ef_fractions=(0.01, 0.05, 0.1), bedroc_alpha=20.0
):
    """Compare two saved-result arms on the same original scored subset.

    Parameters
    ----------
    cohort : list of dict
        The shared original cohort accepted by summarize_screening_results.
    baseline, comparison : dict
        Each contains ``evaluations``, ``input_mapping``, explicit
        ``score_method`` and optional ``unscored`` / ``source_metadata`` accepted
        by summarize_screening_results. Both criteria must agree. Different
        queries/producers are retained, never inferred equivalent.
    ef_fractions, bedroc_alpha
        Identical metric settings for both arms and their common subset.

    Returns
    -------
    dict
        Complete arm summaries and recomputed common-subset statistics with
        original indices/labels/scores and comparison-minus-baseline deltas.
        Empty or single-class undefined metrics/deltas are None. Counts are
        descriptive, with no confidence interval or causal/predictive claim.

    Examples
    --------
    >>> paired = compare_screening_results(cohort, saved_baseline, saved_consensus)
    >>> shared_indices = paired['common_subset']['input_indices']
    """
    fractions, alpha = _settings(ef_fractions, bedroc_alpha)
    summaries = {}
    for name, arm in (("baseline", baseline), ("comparison", comparison)):
        if (
            not isinstance(arm, dict)
            or not {"evaluations", "input_mapping", "score_method"} <= arm.keys()
            or arm.keys()
            - {
                "evaluations",
                "input_mapping",
                "score_method",
                "unscored",
                "source_metadata",
            }
        ):
            _error(
                name,
                "expected saved results, mapping, criterion and optional causes/source metadata",
            )
        summaries[name] = summarize_screening_results(
            cohort, **arm, ef_fractions=fractions, bedroc_alpha=alpha
        )
    left, right = summaries.values()
    if left["score_method"] != right["score_method"]:
        _error("score_method", "paired arms require the same score criterion")
    common = set(left["evaluated_indices"]) & set(right["evaluated_indices"])
    rows = {
        name: [row for row in summary["records"] if row["input_index"] in common]
        for name, summary in summaries.items()
    }
    metrics = {
        name: _metrics(selected, fractions, alpha) for name, selected in rows.items()
    }
    deltas = {
        key: None
        if value is None or metrics["baseline"][key] is None
        else value - metrics["baseline"][key]
        for key, value in metrics["comparison"].items()
        if key not in {"n_evaluated", "n_actives", "n_inactives"}
    }
    return {
        "schema": "pharmacophoremt.screening_comparison@1",
        "score_method": left["score_method"],
        "arms": summaries,
        "common_subset": {
            "input_indices": [row["input_index"] for row in rows["baseline"]],
            "labels": [row["label"] for row in rows["baseline"]],
            "scores": {
                name: [row["score"] for row in selected]
                for name, selected in rows.items()
            },
            "metrics": metrics,
            "delta_comparison_minus_baseline": deltas,
        },
    }
