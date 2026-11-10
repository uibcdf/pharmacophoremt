"""Run the fixed analytical experiment after explicit private source admission."""

import argparse
import importlib.metadata
import json
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    # The case-owned isolated launcher admits exact third-party bytes first.
    # This command never acquires/installs a dependency or allocates resources.
    with args.output.open("x") as output:
        import ackredit
        import pmapper

        import pharmacophoremt as phmt
        from phmt_test_support.pmapper_controls import (
            cache_controls,
            compare_stage,
            file_identity,
            load_declaration,
            rational_oracles,
        )

        declaration = load_declaration()
        report = {
            "schema": "pharmacophoremt.pmapper-controls-result@1",
            "case_id": declaration["case_id"],
            "python": sys.version,
            "runtime_version": phmt.__version__,
            "pmapper_version": pmapper.__version__,
            "pmapper_source": declaration["pmapper_source"],
            "versions": {
                n: importlib.metadata.version(n)
                for n in (
                    "pharmacophoremt",
                    "molsysmt",
                    "numpy",
                    "networkx",
                    "rdkit",
                    "pyunitwizard",
                    "ackredit",
                )
            },
            "oracles": rational_oracles(declaration),
            "cases": [],
            "molecular_inputs": 0,
            "performance_measured": False,
            "scope": declaration["scope"],
        }

        def retain():
            output.seek(0)
            json.dump(report, output, indent=2, allow_nan=False)
            output.write("\n")
            output.truncate()
            output.flush()

        with ackredit.session("pmapper analytical stage controls"), phmt.attribution():
            ackredit.register_item(
                id="phmt-study:pmapper",
                type="software",
                title="pmapper",
                authors=["Pavel Polishchuk"],
                url="https://github.com/DrrDom/pmapper/commit/"
                + declaration["pmapper_source"],
            )
            retain()
            for case in declaration["cases"]:
                row = {"key": case["key"]}
                try:
                    row["actual"] = compare_stage(case, declaration["limits"])
                    row["status"] = "completed"
                    ackredit.track_item("phmt-study:pmapper")
                except Exception as error:
                    row.update(
                        status="failed",
                        error_type=type(error).__name__,
                        error=str(error),
                    )
                report["cases"].append(row)
                retain()
            try:
                report["cache_controls"] = cache_controls(declaration)
                ackredit.track_item("phmt-study:pmapper")
            except Exception as error:
                report["cache_control_failure"] = {
                    "type": type(error).__name__,
                    "reason": str(error),
                }
            report["attribution"] = ackredit.get_attribution().to_dict()
        report["all_declared_observations_match"] = all(
            r["status"] == "completed" and r["actual"]["expected_observations_match"]
            for r in report["cases"]
        ) and report.get("cache_controls", {}).get("expected_observations_match", False)
        report["cache_equivalence_passed"] = bool(report.get("cache_controls")) and all(
            report["cache_controls"][key]["cache_equivalence_passed"]
            for key in ("bin_change", "coordinate_reload")
        )
        report["actual_loaded_origins"] = {
            name: {"path": str(module.__file__), **file_identity(module.__file__)}
            for name, module in sys.modules.copy().items()
            if getattr(module, "__file__", None)
            and name.split(".")[0]
            in {"pmapper", "pharmacophoremt", "molsysmt", "rdkit", "numpy", "networkx"}
            and str(module.__file__).endswith((".py", ".so"))
        }
        retain()
        print(
            json.dumps(
                {
                    "all_declared_observations_match": report[
                        "all_declared_observations_match"
                    ],
                    "cache_equivalence_passed": report["cache_equivalence_passed"],
                    "completed_cases": sum(
                        r["status"] == "completed" for r in report["cases"]
                    ),
                }
            )
        )
        return 0 if report["all_declared_observations_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
