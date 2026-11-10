"""Opt-in bounded snapshot case; execution resources are the caller's responsibility."""

import argparse
import json
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--snapshots", type=Path, required=True)
    parser.add_argument("--admission-sha256", required=True)
    args = parser.parse_args(argv)
    if args.output.exists() or args.snapshots.exists():
        raise FileExistsError("Preserve original output and snapshot destinations")
    args.snapshots.mkdir()
    with args.output.open("x") as output:
        import ackredit
        import molsysmt as msm
        import numpy as np

        import pharmacophoremt as phmt
        from pharmacophoremt import pyunitwizard as puw
        from pharmacophoremt.screening import evaluate_feature_correspondence
        from phmt_test_support.feature_snapshot import (
            FeatureSnapshotStudy,
            capture_feature_snapshot,
        )
        from phmt_test_support.feature_snapshot_case import (
            declaration,
            identity,
            independent_geometry,
            load_parent,
            producer_context,
            projection,
        )

        spec = declaration()
        report = {
            "schema": "pharmacophoremt.feature-snapshot-result@1",
            "case_id": "native-feature-snapshot-v1",
            "status": "running",
            "python": sys.version,
            "producer": producer_context(args.admission_sha256),
            "rows": [],
            "performance_measured": False,
            "source_authentication": "caller precondition, not performed by snapshot",
        }

        def retain():
            output.seek(0)
            json.dump(report, output, indent=2, allow_nan=False)
            output.write("\n")
            output.truncate()
            output.flush()

        retain()
        with ackredit.session("Native feature snapshots"), phmt.attribution():
            try:
                for unit in spec["unit_contexts"]:
                    with puw.context(standard_units=[unit, "ps", "radians"]):
                        for request in spec["requests"]:
                            source, parent = load_parent(request["parent"])
                            before = puw.get_value(
                                msm.get(source, coordinates=True), to_unit="nm"
                            ).copy()
                            baseline = phmt.modeler.get_features(
                                source,
                                features=request["features"],
                                chemical_state=0,
                            )
                            snapshot = capture_feature_snapshot(
                                source,
                                parent=parent,
                                features=request["features"],
                                producer=report["producer"],
                            )
                            path = args.snapshots / (
                                unit + "-" + request["key"] + ".json"
                            )
                            with path.open("xb") as stream:
                                stream.write(snapshot.to_bytes())
                            credits_before = ackredit.get_attribution().to_dict()
                            restored = FeatureSnapshotStudy(path.read_bytes())
                            description = restored.describe()
                            decoded = restored.decode_inventory()
                            assert restored.to_dict() == snapshot.to_dict()
                            assert (
                                ackredit.get_attribution().to_dict() == credits_before
                            )
                            independent_geometry(request["key"], baseline)
                            independent_geometry(request["key"], decoded)
                            assert projection(decoded) == projection(baseline)
                            assert description["coverage"] == {
                                kind: {
                                    "count": n,
                                    "status": "completed" if n else "evaluated_empty",
                                }
                                for kind, n in request["expected_counts"].items()
                            }
                            pairs = [[i, i] for i in range(len(decoded["features"]))]
                            check = evaluate_feature_correspondence(
                                baseline,
                                decoded,
                                pairs,
                                distance_tolerance="0.000000001 nm",
                            )
                            assert check["complete"] and check["all_pairs_valid"]
                            np.testing.assert_array_equal(
                                puw.get_value(
                                    msm.get(source, coordinates=True), to_unit="nm"
                                ),
                                before,
                            )
                            report["rows"].append(
                                {
                                    "unit_context": unit,
                                    "request": request["key"],
                                    "snapshot_file": path.name,
                                    "snapshot_identity": identity(path),
                                    "payload_sha256": description["payload_sha256"],
                                    "description": description,
                                    "scientific": projection(decoded),
                                    "pair_check": check,
                                    "original_attribution": restored.to_dict()[
                                        "payload"
                                    ]["inventory"].get("attribution"),
                                    "reading_created_no_credit": True,
                                    "source_coordinates_unchanged": True,
                                }
                            )
                            retain()
                report["status"] = "completed"
            except Exception as error:
                report.update(
                    status="failed",
                    failure={"type": type(error).__name__, "reason": str(error)},
                )
            report["actual_attribution"] = ackredit.get_attribution().to_dict()
        retain()
        print(
            json.dumps(
                {"status": report["status"], "completed_rows": len(report["rows"])}
            )
        )
        return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
