"""Freeze #64 attempt 2's bounded training-readiness policy before acquisition."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tests/data/esr1_consensus_comparison/readiness_declaration.json"
spec = importlib.util.spec_from_file_location(
    "esr1_original_declaration",
    Path(__file__).with_name("esr1_consensus_declaration.py"),
)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
ORIGINAL_SHA256 = "a1a476e7e94fd3480ee3845fbc5cca138221c4052eb7165a254499fd526ff647"
PRIOR = ROOT / "tests/data/esr1_consensus_comparison/training_20261024/acquisition.json"


def build_declaration(directory):
    original_bytes = base.OUTPUT.read_bytes()
    if hashlib.sha256(original_bytes).hexdigest() != ORIGINAL_SHA256:
        raise ValueError("preserve the original attempt's declaration")
    original = base.build_declaration(directory)
    if original != json.loads(original_bytes):
        raise ValueError("original source/split contract changed")
    _, assay, excluded = base._source_population(directory)
    by_cid, ordered, _ = base._ordered_population(assay, excluded)
    if len(ordered["Active"]) < 28:
        raise ValueError("insufficient candidates; do not expand the declared pool")
    prior_summary = json.loads(
        (
            ROOT / "devguide/evidence/esr1_consensus_training_20261024_summary.json"
        ).read_text()
    )
    if (
        hashlib.sha256(PRIOR.read_bytes()).hexdigest()
        != prior_summary["acquisition"]["sha256"]
    ):
        raise ValueError("preserve prior acquisition identities, including failures")
    prior = json.loads(PRIOR.read_text())
    original_training = [e for e in original["cohort"] if e["role"] == "training"]
    if [e["cid"] for e in prior["records"]] != [e["cid"] for e in original_training]:
        raise ValueError("prior training acquisition does not match original split")
    candidates = []
    for cid in ordered["Active"][:3] + ordered["Active"][19:28]:
        row = min(by_cid[cid], key=lambda row: int(row["SID"]))
        candidates.append(
            dict(
                cid=cid,
                sid=row["SID"],
                label=1,
                role="training_candidate",
                assay_outcome="Active",
                selection_hash=hashlib.sha256((base.PREFIX + cid).encode()).hexdigest(),
                url=f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/SDF?record_type=3d",
            )
        )
    protocol = copy.deepcopy(original)
    protocol.update(
        schema="pharmacophoremt.esr1_consensus_comparison_declaration@2",
        attempt="bounded_training_readiness_02",
        prior_declaration_sha256=ORIGINAL_SHA256,
        stage="pre-acquisition attempt 2; original training observations known; evaluation unopened",
        cohort=candidates
        + [e for e in original["cohort"] if e["role"] == "evaluation"],
    )
    protocol["selection"].update(
        split="identical original 64 evaluation entries; training candidates = original first 3 actives plus active hash positions 19:28, excluding reserved evaluation actives",
        missing_inputs="retain every candidate failure; select first three eligible candidates in declared order; no expansion beyond 12 and no evaluation replacement",
    )
    protocol["training_readiness"] = dict(
        candidate_cap=12,
        required_inputs=3,
        acquisition="attempt every candidate once; reuse original three response identities without refresh, including the known 404; acquire only the other nine",
        prior_acquisition_path=str(PRIOR.relative_to(ROOT)),
        prior_acquisition_sha256=hashlib.sha256(PRIOR.read_bytes()).hexdigest(),
        prior_training_cids=[e["cid"] for e in original_training],
        eligibility="completed acquisition plus successful declared MolSysMT preparation, preservation checks and requested feature-inventory operation; no threshold on feature counts, geometry, similarity, model support or pharmacophore score",
        selection="first three completed preparations in fixed candidate order; prepare and retain all 12 candidates; freeze trio before consensus; pivot is first selected candidate",
        stop="fewer than three eligible candidates, failed/incomplete/empty consensus or failed selected-query readiness stops attempt; no alternate trio, pivot, model, budget or threshold",
        scientific_parameters="consensus parameters/model ordering, baseline, scoring and evaluation/comparison identical to original attempt; only training-readiness sampling changes",
        known_observations="the original three training responses and two preparation records are exposed training-development evidence, not unseen validation; no evaluation data are opened",
    )
    protocol["consensus"]["readiness"] = (
        "first three eligible candidates fixed before consensus; selected query must yield at least one native seeded_hit among that trio, with no alternate model on failure"
    )
    protocol["consensus"]["stop"] = protocol["training_readiness"]["stop"]
    protocol["consensus"]["freeze"] = (
        "retain all candidate responses/preparations/failures and selected trio; commit complete training receipt and exact valid query hash before evaluation acquisition"
    )
    return protocol


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    protocol = build_declaration(args.source_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(json.dumps(protocol, indent=2, allow_nan=False) + "\n")
    print(
        json.dumps(
            dict(
                attempt=protocol["attempt"],
                training_candidates=12,
                evaluation_inputs=64,
            )
        )
    )


if __name__ == "__main__":
    main()
