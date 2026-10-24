"""Opt-in #64 paired evaluation of two committed, checksum-frozen queries.

Case orchestration only: public MolSysMT owns every molecular operation; native
PHMT search/retrospective/metric tools own scientific calculations. Missing
source inputs stay unscored in the 64-input study ledger, not fabricated native
failure objects or replacement molecules. No training/model selection occurs.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import time
import traceback
import urllib.error
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "paired_training_support", Path(__file__).with_name("esr1_consensus_training.py")
)
training = importlib.util.module_from_spec(spec)
spec.loader.exec_module(training)
pilot = training.pilot
spec = importlib.util.spec_from_file_location(
    "paired_archive_reader", Path(__file__).with_name("evidence_archive.py")
)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
DECLARATION = ROOT / "tests/data/esr1_consensus_comparison/readiness_declaration.json"
TRAINING_SUMMARY = (
    ROOT / "devguide/evidence/esr1_consensus_readiness_training_20261024_summary.json"
)
QUERY_HASHES = dict(
    baseline="c165f3755e1a76603a69f7fd1c24259e8f4706c20407eb3fdf653a4b5f7804f3",
    consensus="f80a09a68e21a8826a399467bb449082765e10328c8480717811049aa1d93a6d",
)


def frozen_context():
    protocol = training.declaration(DECLARATION)
    if pilot.digest(DECLARATION.read_bytes()) != training.READINESS_DECLARATION_SHA256:
        raise ValueError("paired evaluation requires the second frozen declaration")
    _, trained = reader.read_archived_evidence(TRAINING_SUMMARY)
    if (
        trained["outcome"]
        != dict(status="ready", stage="training_complete", evaluation_opened=False)
        or trained["declaration"]["sha256"] != training.READINESS_DECLARATION_SHA256
        or not trained["producer_stable"]
        or trained["producer"]["dirty"]
    ):
        raise ValueError("a qualified committed training query is required")
    queries = {}
    for arm, summary in (
        (
            "baseline",
            ROOT / "devguide/evidence/esr1_activity_pilot_20261023_summary.json",
        ),
        ("consensus", TRAINING_SUMMARY),
    ):
        _, raw = reader.read_archived_bytes(summary, identity_key="saved_query_archive")
        if pilot.digest(raw) != QUERY_HASHES[arm]:
            raise ValueError("preserve both frozen query identities")
        queries[arm] = raw
    return protocol, trained, queries


def evaluation_entries(protocol):
    return [e for e in protocol["cohort"] if e["role"] == "evaluation"]


def acquire(directory):
    protocol, _, queries = frozen_context()
    directory.mkdir(parents=True, exist_ok=False)
    for arm, raw in queries.items():
        (directory / f"{arm}.query.json").write_bytes(raw)
    records = []
    for index, entry in enumerate(evaluation_entries(protocol)):
        record = dict(entry, cohort_index=index)
        path = directory / f"CID{entry['cid']}.sdf"
        try:
            pilot.fetch(entry["url"], path)
        except urllib.error.HTTPError as error:
            response = directory / f"CID{entry['cid']}.http-error.txt"
            with error:
                response.write_bytes(error.read())
            record["acquisition"] = dict(
                status="failed",
                http_status=error.code,
                response=pilot.identity(response),
            )
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            record["acquisition"] = dict(
                status="failed", error_type=type(error).__name__, message=str(error)
            )
        else:
            record["acquisition"] = dict(status="completed", **pilot.identity(path))
        records.append(record)
        print(
            f"acquired evaluation {index + 1}/64 CID {entry['cid']}: {record['acquisition']['status']}",
            flush=True,
        )
        time.sleep(0.25)
    receipt = dict(
        schema="pharmacophoremt.esr1_paired_evaluation_acquisition@1",
        issue=64,
        acquired_at=datetime.now(timezone.utc).isoformat(),
        declaration=pilot.identity(DECLARATION),
        frozen_queries={
            arm: pilot.identity(directory / f"{arm}.query.json") for arm in queries
        },
        training_summary=pilot.identity(TRAINING_SUMMARY),
        producer=dict(
            git_head=training.git("rev-parse", "HEAD"),
            dirty=training.git("status", "--porcelain"),
            driver=pilot.identity(Path(__file__)),
        ),
        records=records,
        scope="all 64 unchanged evaluation inputs; one request each, all failures retained, no replacements",
    )
    pilot.dump(directory / "acquisition.json", receipt)
    return receipt


def validate_acquisition(directory, protocol, queries):
    receipt = json.loads((directory / "acquisition.json").read_text())
    expected = evaluation_entries(protocol)
    if (
        receipt.get("schema") != "pharmacophoremt.esr1_paired_evaluation_acquisition@1"
        or receipt["declaration"]["sha256"] != training.READINESS_DECLARATION_SHA256
        or len(receipt["records"]) != 64
        or len(expected) != 64
    ):
        raise ValueError("preserve the complete frozen evaluation cohort")
    for arm, raw in queries.items():
        if (directory / f"{arm}.query.json").read_bytes() != raw:
            raise ValueError("saved query substituted")
    for index, (record, entry) in enumerate(
        zip(receipt["records"], expected, strict=True)
    ):
        if record["cohort_index"] != index or any(
            record[k] != v for k, v in entry.items()
        ):
            raise ValueError("evaluation identity/order changed")
        acquired = record["acquisition"]
        identity = (
            acquired if acquired["status"] == "completed" else acquired.get("response")
        )
        if identity is not None:
            name = f"CID{entry['cid']}." + (
                "sdf" if acquired["status"] == "completed" else "http-error.txt"
            )
            if identity["file"] != name or pilot.identity(directory / name) != {
                k: identity[k] for k in ("file", "sha256", "byte_count")
            }:
                raise ValueError("original evaluation response changed")
    return receipt


def prepared_mapping(records):
    """Keep native prepared-batch indices separate from all 64 study indices."""
    return [
        r["cohort_index"]
        for label in (1, 0)
        for r in records
        if r["label"] == label and r["preparation"]["status"] == "completed"
    ]


def metrics(labels, scores, settings):
    from pharmacophoremt.validation.metrics import bedroc, enrichment_factor, roc_auc

    if not labels:
        return dict(
            n_evaluated=0,
            n_actives=0,
            n_inactives=0,
            AUC=None,
            BEDROC=None,
            **{"EF@10%": None},
        )
    return dict(
        n_evaluated=len(labels),
        n_actives=sum(labels),
        n_inactives=len(labels) - sum(labels),
        AUC=roc_auc(labels, scores),
        BEDROC=bedroc(labels, scores, alpha=settings["bedroc_alpha"]),
        **{
            "EF@10%": enrichment_factor(
                labels, scores, fraction=settings["ef_fractions"][0]
            )
        },
    )


def study_accounting(records, arm, settings):
    """Case denominators and hypothetical binary missing-score sensitivity."""
    from pharmacophoremt.validation.metrics import roc_auc

    valid = [r for r in records if r["arms"][arm]["ranking_score"] is not None]
    labels = [r["label"] for r in valid]
    scores = [r["arms"][arm]["ranking_score"] for r in valid]
    result = metrics(labels, scores, settings)
    result.update(
        n_total=len(records),
        n_unscored=len(records) - len(valid),
        unscored_by_stage=dict(
            Counter(
                r["arms"][arm]["stage"]
                for r in records
                if r["arms"][arm]["ranking_score"] is None
            )
        ),
        evaluated_cohort_indices=[r["cohort_index"] for r in valid],
        labels=labels,
        scores=scores,
    )
    original_labels = [r["label"] for r in records]
    result["missing_binary_score_AUC_sensitivity"] = {
        name: roc_auc(
            original_labels,
            [
                r["arms"][arm]["ranking_score"]
                if r["arms"][arm]["ranking_score"] is not None
                else (r["label"] if optimistic else 1 - r["label"])
                for r in records
            ],
        )
        for name, optimistic in (
            ("pessimistic_hypothetical", False),
            ("optimistic_hypothetical", True),
        )
    }
    return result


def input_integrity(systems):
    """Read-only case audit of numeric/state preservation, not chemical grouping."""
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw

    return {
        index: pilot.digest(
            json.dumps(
                pilot.portable(
                    dict(
                        coordinates_nm=puw.get_value(
                            msm.get(system, coordinates=True), to_unit="nm"
                        ),
                        states=msm.convert(
                            system.chemical_states,
                            to_form="molsysmt.ChemicalStatesDict",
                        ).to_dict(),
                        atom_ids=msm.get(system, element="atom", atom_id=True),
                        elements=msm.get(system, element="atom", atom_type=True),
                    )
                ),
                sort_keys=True,
                allow_nan=False,
            ).encode()
        )
        for index, system in systems.items()
    }


def execute(directory, output):
    protocol, trained, queries = frozen_context()
    acquisition = validate_acquisition(directory, protocol, queries)
    journal_path = output.with_suffix(".preparation.json")
    arm_journals = {arm: output.with_suffix(f".{arm}.json") for arm in queries}
    for path in (output, journal_path, *arm_journals.values()):
        if path.exists():
            raise FileExistsError(
                "retain the original evaluation/journal; choose a new output"
            )
    import ackredit
    import molsysmt as msm

    import pharmacophoremt as phmt
    from pharmacophoremt.io import load_json
    from pharmacophoremt.screening import RigidPoseSearch, get_screening_score
    from pharmacophoremt.validation import RetrospectiveValidator

    initial = training.producer(phmt, msm)
    if initial["runtime_files"] != trained["producer"]["runtime_files"]:
        raise ValueError(
            "product/provider code differs from qualified training; inspect before evaluation"
        )
    systems, records, reports = {}, [], {}
    integrity = {}
    with (
        ackredit.session("ERalpha #64 paired evaluation"),
        ackredit.capture("frozen paired evaluation", record_evidence=True) as captured,
        phmt.attribution(True),
    ):
        ackredit.register_item(
            id="phmt:dataset:aid743075",
            type="dataset",
            title="PubChem BioAssay 743075: ER-alpha signaling agonist assay",
            url=pilot.ASSAY_URL,
        )
        ackredit.track_item(
            "phmt:dataset:aid743075",
            roles=["input_data"],
            context={
                "scope": "64 frozen evaluation CID/SID/outcomes, no affinity claim"
            },
        )
        for entry in acquisition["records"]:
            record = {
                k: entry[k]
                for k in ("cid", "sid", "label", "cohort_index", "acquisition")
            }
            record["arms"] = {}
            if entry["acquisition"]["status"] != "completed":
                record["preparation"] = dict(
                    status="unavailable",
                    stage="acquisition",
                    message="original acquisition failed; no replacement",
                )
            else:
                item_id = "phmt:dataset:pubchem-3d:" + entry["cid"]
                ackredit.register_item(
                    id=item_id,
                    type="dataset",
                    title="PubChem computed 3D CID " + entry["cid"],
                    url=entry["url"],
                )
                ackredit.track_item(
                    item_id,
                    roles=["input_data"],
                    context={
                        "sha256": entry["acquisition"]["sha256"],
                        "scope": "evaluation preparation attempt",
                    },
                )
                try:
                    prepared, _, observation = pilot._prepare_pilot_entry(
                        entry,
                        directory,
                        features=protocol["consensus"]["parameters"]["features"],
                    )
                except Exception as error:
                    record["preparation"] = dict(
                        status="failed",
                        stage="preparation",
                        error_type=type(error).__name__,
                        message=str(error),
                        traceback=traceback.format_exc(),
                    )
                else:
                    systems[entry["cohort_index"]] = prepared
                    record["preparation"] = observation
            records.append(record)
            print(
                f"prepared evaluation {len(records)}/64 CID {entry['cid']}: {record['preparation']['status']}",
                flush=True,
            )
        pilot.dump(
            journal_path,
            pilot.portable(
                dict(
                    declaration=pilot.identity(DECLARATION),
                    acquisition=pilot.identity(directory / "acquisition.json"),
                    records=records,
                )
            ),
        )
        mapping = prepared_mapping(records)
        integrity["before"] = input_integrity(systems)
        for arm in ("baseline", "consensus"):
            print(
                f"scoring {arm}: {len(mapping)} prepared inputs; original study denominator 64",
                flush=True,
            )
            query = load_json(str(directory / f"{arm}.query.json"))
            search = RigidPoseSearch(
                query,
                **{
                    k: protocol["screening"][k]
                    for k in (
                        "search_method",
                        "max_trials",
                        "point_tolerance",
                        "direction_tolerance",
                        "min_fit_value",
                    )
                },
            )
            report = None
            if mapping:
                report = RetrospectiveValidator(query, evaluator=search).run(
                    [systems[i] for i in mapping if records[i]["label"] == 1],
                    [systems[i] for i in mapping if records[i]["label"] == 0],
                    on_error="record",
                    ef_fractions=protocol["screening"]["ef_fractions"],
                    bedroc_alpha=protocol["screening"]["bedroc_alpha"],
                )
                for evaluation in report["evaluations"]:
                    index = mapping[evaluation["input_index"]]
                    records[index]["arms"][arm] = dict(
                        stage="search",
                        native_input_index=evaluation["input_index"],
                        ranking_score=get_screening_score(
                            evaluation, score_method="seeded_hit"
                        ),
                        native_evaluation=evaluation,
                    )
            for record in records:
                if arm not in record["arms"]:
                    record["arms"][arm] = dict(
                        stage=record["preparation"]["stage"],
                        native_input_index=None,
                        ranking_score=None,
                        native_evaluation=None,
                    )
            integrity["after_" + arm] = input_integrity(systems)
            reports[arm] = dict(
                native_prepared_input_report=report,
                study=study_accounting(records, arm, protocol["screening"]),
            )
            pilot.dump(
                arm_journals[arm],
                pilot.portable(
                    dict(
                        arm=arm,
                        report=reports[arm],
                        records=records,
                        integrity_before=integrity["before"],
                        integrity_after=integrity["after_" + arm],
                    )
                ),
            )
            if integrity["after_" + arm] != integrity["before"]:
                raise ValueError(
                    "prepared molecular input changed between arms; preserve journal and inspect"
                )
            print(
                json.dumps(
                    dict(
                        arm=arm,
                        study={
                            k: v
                            for k, v in pilot.portable(reports[arm]["study"]).items()
                            if k not in {"scores", "labels", "evaluated_cohort_indices"}
                        },
                    )
                ),
                flush=True,
            )
        common = [
            r
            for r in records
            if all(
                r["arms"][arm]["ranking_score"] is not None
                for arm in ("baseline", "consensus")
            )
        ]
        common_reports = {
            arm: metrics(
                [r["label"] for r in common],
                [r["arms"][arm]["ranking_score"] for r in common],
                protocol["screening"],
            )
            for arm in ("baseline", "consensus")
        }
        delta = (
            None
            if len({r["label"] for r in common}) < 2
            else common_reports["consensus"]["AUC"] - common_reports["baseline"]["AUC"]
        )
    final = training.producer(phmt, msm)
    result = dict(
        schema="pharmacophoremt.esr1_paired_evaluation_run@1",
        issue=64,
        measured_at=datetime.now(timezone.utc).isoformat(),
        producer=dict(initial, evaluation_driver=pilot.identity(Path(__file__))),
        producer_stable=initial == final,
        producer_after=final if initial != final else None,
        product_provider_files_match_training=True,
        declaration=pilot.identity(DECLARATION),
        training_summary=pilot.identity(TRAINING_SUMMARY),
        acquisition=pilot.identity(directory / "acquisition.json"),
        queries={
            arm: pilot.identity(directory / f"{arm}.query.json") for arm in queries
        },
        preparation_journal=pilot.identity(journal_path),
        arm_journals={arm: pilot.identity(path) for arm, path in arm_journals.items()},
        prepared_cohort_indices=mapping,
        records=records,
        arms=reports,
        common_subset=dict(
            cohort_indices=[r["cohort_index"] for r in common],
            arms=common_reports,
            delta_AUC_consensus_minus_baseline=delta,
        ),
        input_integrity=integrity,
        attribution=captured.attribution.to_dict(),
        scope="fixed descriptive same-assay CID-disjoint paired evaluation; no tuning, replacement, independent-series, affinity or predictive-acceptance claim; binary missing-score scenarios are sensitivity bounds, not imputation/CI",
    )
    pilot.dump(output, pilot.portable(result))
    print(
        json.dumps(
            pilot.portable(
                dict(
                    producer_stable=result["producer_stable"],
                    common_subset=result["common_subset"],
                )
            )
        ),
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--acquire", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.acquire:
        acquire(args.data_dir)
    if args.output:
        execute(args.data_dir, args.output)


if __name__ == "__main__":
    main()
