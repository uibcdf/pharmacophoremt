"""Freeze #64's case-specific assay split and methods before molecular work.

Standard-library ID/CSV orchestration only. This does not interpret molecules,
acquire new structures, fit models, screen compounds or register scientific use.
Restore the original #62 inputs with its existing standalone driver first.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import tarfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests/data/esr1_activity_pilot/manifest.json"
OUTPUT = ROOT / "tests/data/esr1_consensus_comparison/declaration.json"
PREFIX = "phmt-esr1-consensus-comparison-v1:"
FEATURES = ["hb donor", "hb acceptor", "aromatic ring"]


def _ordered_population(assay_rows, excluded_cids):
    """Read the case's eligible external-ID population without molecular inference."""
    by_cid = defaultdict(list)
    for row in assay_rows:
        if row["CID"]:
            if not row["CID"].isdigit() or not row["SID"].isdigit():
                raise ValueError("assay requires numeric CID/SID identifiers")
            by_cid[row["CID"]].append(row)
    ambiguous = {
        cid
        for cid, rows in by_cid.items()
        if len({row["Activity Outcome"] for row in rows}) != 1
    }
    groups = {"Active": [], "Inactive": []}
    for cid, rows in by_cid.items():
        label = rows[0]["Activity Outcome"]
        if cid not in excluded_cids and cid not in ambiguous and label in groups:
            groups[label].append(cid)
    ordered = {
        label: sorted(
            cids, key=lambda cid: hashlib.sha256((PREFIX + cid).encode()).hexdigest()
        )
        for label, cids in groups.items()
    }
    return by_cid, ordered, len(ambiguous)


def select_cohort(assay_rows, excluded_cids):
    """Select IDs by declared labels/hash; no chemical equivalence is inferred."""
    by_cid, ordered, ambiguous_count = _ordered_population(assay_rows, excluded_cids)
    if len(ordered["Active"]) < 19 or len(ordered["Inactive"]) < 48:
        raise ValueError("insufficient unambiguous new CIDs; do not substitute")
    cohort = []
    for label, cids in ordered.items():
        for index, cid in enumerate(cids[: 19 if label == "Active" else 48]):
            row = min(by_cid[cid], key=lambda row: int(row["SID"]))
            cohort.append(
                dict(
                    cid=cid,
                    sid=row["SID"],
                    label=int(label == "Active"),
                    role="training"
                    if label == "Active" and index < 3
                    else "evaluation",
                    assay_outcome=label,
                    selection_hash=hashlib.sha256((PREFIX + cid).encode()).hexdigest(),
                    url=f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/SDF?record_type=3d",
                )
            )
    return dict(
        cohort=cohort,
        population=dict(
            assay_rows=len(assay_rows),
            assay_unique_cids=len(by_cid),
            all_ambiguous_cids=ambiguous_count,
            excluded_bath_cids=len(excluded_cids),
            eligible_counts={label: len(cids) for label, cids in ordered.items()},
        ),
    )


def _source_population(directory):
    """Reuse verified original response bytes; never reacquire a refreshed source."""
    manifest = json.loads(MANIFEST.read_text())
    sources = {key: manifest[key] for key in ("source", "assay", "assay_description")}
    payloads = {}
    for key, record in sources.items():
        payload = (directory / record["file"]).read_bytes()
        if (
            hashlib.sha256(payload).hexdigest() != record["sha256"]
            or len(payload) != record["byte_count"]
        ):
            raise ValueError(f"original source identity changed: {key}")
        payloads[key] = payload
    with tarfile.open(fileobj=io.BytesIO(payloads["source"])) as archive:
        with archive.extractfile("ESR1ago/ESR1ago_data_full.csv") as stream:
            excluded = {
                row["PUBCHEM_CID"] for row in csv.DictReader(io.TextIOWrapper(stream))
            }
    assay = list(csv.DictReader(io.StringIO(payloads["assay"].decode())))
    if any(row["AID"] != "743075" for row in assay):
        raise ValueError("unexpected assay identity")
    return sources, assay, excluded


def build_declaration(directory):
    """Verify original source bytes, then reproduce the pre-score declaration."""
    original = json.loads(
        (
            ROOT / "devguide/evidence/esr1_activity_pilot_20261023_summary.json"
        ).read_text()
    )
    if (
        hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
        != original["manifest"]["sha256"]
    ):
        raise ValueError("original input manifest identity changed")
    sources, assay, excluded = _source_population(directory)
    selection = select_cohort(assay, excluded)
    return dict(
        schema="pharmacophoremt.esr1_consensus_comparison_declaration@1",
        issue=64,
        declared_on="2026-10-24",
        stage="pre-score; no new structures acquired or molecular calculations executed",
        sources=sources,
        selection=dict(
            hash_prefix=PREFIX,
            representative="lowest numeric SID among consistent rows for each CID",
            exclusion="all Bath ESR1ago CIDs; every assay CID with multiple outcomes, including inconclusive",
            split="first 3 Active training; next 16 Active and first 48 Inactive evaluation",
            missing_inputs="retain each failure without replacement or inactive imputation",
            **selection["population"],
        ),
        cohort=selection["cohort"],
        preparation=dict(
            provider="molsysmt",
            qualified_route="public MolSysMT 0.23.0; new runs must record actual provider/runtime identities",
            source="one unchanged PubChem computed 3D SDF per CID, supplied state/hydrogens",
            operations="convert SDF to MolSys with discard_properties=True, stereo_engine='rdkit'; convert through rdkit.Mol back to MolSys using public MolSysMT only",
            acceptance="source byte/state/coordinates unchanged; IDs/elements/charge/unpaired-electrons/stereo preserved; coordinate RMSD < 1e-12 nm; retain every unsupported/failure outcome",
        ),
        baseline=dict(
            query_sha256=original["saved_query_archive"]["uncompressed_sha256"],
            query_summary="devguide/evidence/esr1_activity_pilot_20261023_summary.json",
            identity_key="saved_query_archive",
            changes="none",
        ),
        consensus=dict(
            tool="pharmacophoremt.modeler.from_rigid_ligands",
            parameters=dict(
                reference_index=0,
                correspondence_strategy="association_cliques",
                n_seeds=None,
                refinement_strategy=None,
                orientation_policy="final",
                features=FEATURES,
                min_matches=3,
                min_support=2,
                min_sites=3,
                distance_tolerance="0.15 nm",
                direction_tolerance="30 degrees",
                radius="0.15 nm",
                max_graph_nodes=128,
                max_cliques=10000,
                max_trials=10000,
                max_fits=256,
                max_layouts=256,
                max_combinations=100000,
                max_matrix_entries=1000000,
            ),
            selection="descending site count; descending hypothesis joint_support_count; ascending layout_id, hypothesis_id; select exactly one model before evaluation",
            readiness="all three training inputs must prepare; complete nonempty consensus; selected query must produce at least one native seeded_hit training hit, without selecting another model on failure",
            stop="any failed prerequisite keeps evaluation structures/scores unopened; no fallback, budget increase, relaxed threshold or replacement in this declared run",
            freeze="retain all original training evidence, alternatives, selected query and query SHA-256 in a committed receipt before evaluation acquisition",
        ),
        screening=dict(
            tool="pharmacophoremt.screening.RigidPoseSearch",
            search_method="seeded_hit",
            score_method="seeded_hit@1",
            max_trials=10000,
            point_tolerance="0.10 nm",
            direction_tolerance="30 degrees",
            min_fit_value=0.0,
            ef_fractions=[0.1],
            bedroc_alpha=20.0,
        ),
        comparison=dict(
            primary="difference in descriptive ROC AUC on the common successfully evaluated subset; undefined if either class is absent",
            additional="per-arm and common-subset counts, all failures, AUC, tie-aware EF10%, BEDROC20; missing-score hypothetical AUC sensitivity, not a confidence interval",
            no_tuning="no query/feature/radius/method/model/budget changes from evaluation outcomes",
            scope="previously unscreened CID-disjoint compounds from the same assay; labels used for sampling; no independent-assay or chemical-series independence, affinity or predictive-acceptance claim",
            molecular_overlap_provider_issue="uibcdf/molsysmt#447",
            molecular_overlap="unqualified beyond external CID exclusion; no consumer molecular identity/scaffold routine",
        ),
        owners=["LMMV", "dprada"],
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    declaration = build_declaration(args.source_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(json.dumps(declaration, indent=2, allow_nan=False) + "\n")
    print(
        json.dumps(
            dict(
                stage=declaration["stage"],
                counts=dict(Counter(e["role"] for e in declaration["cohort"])),
                output=str(args.output),
            )
        )
    )


if __name__ == "__main__":
    main()
