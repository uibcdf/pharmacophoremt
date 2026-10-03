"""Complete PR coverage and conditional recovery retain component test selection."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_contributor_routes_and_complete_supported_matrix():
    workflow = yaml.load(
        (ROOT / ".github/workflows/CI.yaml").read_text(), Loader=yaml.BaseLoader
    )
    assert (
        workflow["on"]["workflow_dispatch"]["inputs"]["probe_backlog"]["type"]
        == "boolean"
    )
    assert "paths-ignore" not in workflow["on"]["pull_request"]
    assert "paths" not in workflow["on"]["pull_request"]
    schedules = workflow["on"]["schedule"]
    assert {"cron": "0 9 * * MON"} in schedules
    assert {"cron": "7 2 * * *", "timezone": "America/Mexico_City"} in schedules
    matrix = workflow["jobs"]["test"]
    assert matrix["needs"] == "nightly-decision"
    assert "always()" in matrix["if"]
    assert "needs.nightly-decision.result != 'success'" in matrix["if"]
    assert "inputs.probe_backlog != true" in matrix["if"]
    assert "continue-on-error" not in matrix
    assert {
        (cell["os"], cell["python-version"])
        for cell in matrix["strategy"]["matrix"]["cfg"]
    } == {
        (os_name, version)
        for os_name in ("ubuntu-latest", "macos-15")
        for version in ("3.11", "3.12", "3.13", "3.14")
    }
    for cell in matrix["strategy"]["matrix"]["cfg"]:
        expected = (
            f"test_env_py{cell['python-version'].replace('.', '')}.yaml"
            if cell["python-version"] in {"3.13", "3.14"}
            else "test_env.yaml"
        )
        assert cell["environment-file"] == f"devtools/conda-envs/{expected}"
    steps = {step.get("name"): step for step in matrix["steps"]}
    command = steps["Run tests"]["run"]
    assert (
        "python -m pytest --receptor=ci -v --cov-config=.coveragerc --cov=pharmacophoremt"
        in command
    )
    assert "--noconftest" not in command
    assert "--ignore" not in command and "smoke" not in command
    assert "if" not in steps["Run tests"]
    assert "continue-on-error" not in steps["Run tests"]
    assert (
        'platform.machine() == "arm64"'
        in steps["Verify interpreter and macOS architecture"]["run"]
    )
