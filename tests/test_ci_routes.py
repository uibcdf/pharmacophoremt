"""Complete PR coverage and conditional recovery retain component test selection."""

import tomllib
from configparser import ConfigParser
from fnmatch import fnmatch
from pathlib import Path
from shlex import split

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_every_minor_acquires_one_reviewed_molsysmt_before_verification():
    """One pinned acquisition must reach verification without a second VCS fetch."""
    workflow = yaml.load(
        (ROOT / ".github/workflows/CI.yaml").read_text(), Loader=yaml.BaseLoader
    )
    steps = workflow["jobs"]["test"]["steps"]
    assert not any(
        "git+https://github.com/uibcdf/molsysmt@" in step.get("run", "")
        for step in steps
    ), "MolSysMT belongs to the reviewed requirements install, not a second VCS step"
    named = {step.get("name"): step for step in steps}
    install = named["Install pinned suite dependencies"]
    verify = named["Check dependency routes and installed Git context"]
    assert "if" not in install and "continue-on-error" not in install
    assert "if" not in verify and "continue-on-error" not in verify
    assert (
        steps.index(install)
        < steps.index(verify)
        < steps.index(named["Install package"])
    )
    assert steps.index(named["Install package"]) < steps.index(named["Run tests"])
    assert (
        "python devtools/check_dependency_routes.py --context ci-${{ matrix.cfg.python-version }}"
        in verify["run"]
    )
    routes = tomllib.loads((ROOT / "devtools/dependency_routes.toml").read_text())
    contexts = {row["name"]: row for row in routes["contexts"]}
    sources = {row["id"]: row for row in routes["source_routes"]}
    for minor in ("3.11", "3.12", "3.13", "3.14"):
        context = contexts["ci-" + minor]
        candidates = [
            sources[key]
            for key in context["sources"]
            if sources[key]["name"] == "molsysmt"
        ]
        assert len(candidates) == 1
        source = candidates[0]
        requirement = "git+" + source["url"] + "@" + source["commit"]
        assert len(source["commit"]) == 40 and source["install"] == "pip-no-deps-git"
        lines = (ROOT / source["input"]).read_text().splitlines()
        assert lines.count(requirement) == 1
        assert f"python -m pip install --no-deps -r {source['input']}" in install["run"]


def test_coverage_measures_the_core_and_both_reader_companions():
    """Shipped reader runtimes must not disappear from reported coverage."""
    workflow = yaml.load(
        (ROOT / ".github/workflows/CI.yaml").read_text(), Loader=yaml.BaseLoader
    )
    step = next(
        step
        for step in workflow["jobs"]["test"]["steps"]
        if step.get("name") == "Run tests"
    )
    commands = [
        line.strip()
        for line in step["run"].splitlines()
        if line.strip().startswith("python -m pytest ")
    ]
    assert len(commands) == 1
    tokens = split(commands[0])
    assert tokens.count("--cov") == 1
    assert not any(token.startswith("--cov=") for token in tokens)
    required = {
        "pharmacophoremt",
        "pharmacophoremt_results",
        "pharmacophoremt_features",
    }
    configuration = ConfigParser()
    configuration.read(ROOT / ".coveragerc")
    assert required == set(configuration["run"]["source_pkgs"].split())
    assert not configuration["run"].get("source", "").strip()
    assert configuration.getboolean("run", "branch")
    omitted = configuration["report"]["omit"].split()
    assert "pharmacophoremt/_private/**" in omitted
    for name in ("_api.py", "_store.py", "_exports.py"):
        relative = "pharmacophoremt_results/" + name
        assert not any(
            fnmatch(relative, pattern) or fnmatch((ROOT / relative).as_posix(), pattern)
            for pattern in omitted
        )
    for name in ("_api.py", "_schema.py", "_storage.py"):
        relative = "pharmacophoremt_features/" + name
        assert not any(
            fnmatch(relative, pattern) or fnmatch((ROOT / relative).as_posix(), pattern)
            for pattern in omitted
        )


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
    admission = " ".join(matrix["if"].split())
    assert admission.startswith("!cancelled() && ")
    assert "always()" not in admission
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
        "python -m pytest --receptor=ci -v --cov-config=.coveragerc --cov --cov-report=xml"
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


def test_supported_matrix_has_native_scientific_dependencies():
    """Every native-test lane needs OpenMM bonds and active type validation (#23)."""
    workflow = yaml.load(
        (ROOT / ".github/workflows/CI.yaml").read_text(), Loader=yaml.BaseLoader
    )
    environment_files = {
        cell["environment-file"]
        for cell in workflow["jobs"]["test"]["strategy"]["matrix"]["cfg"]
    }
    reference = yaml.safe_load(
        (ROOT / "devtools/conda-envs/test_env_py313.yaml").read_text()
    )

    def scientific_dependencies(environment):
        # Interpreter selectors and reporting-tool generations differ by minor.
        return {
            dependency
            for dependency in environment["dependencies"]
            if dependency.split()[0] != "python"
            and not dependency.startswith("pytest-receptor=")
        }

    for filename in sorted(environment_files):
        environment = yaml.safe_load((ROOT / filename).read_text())
        dependencies = scientific_dependencies(environment)
        assert {"openmm", "beartype"} <= dependencies, filename
        assert dependencies == scientific_dependencies(reference), filename
        assert environment["channels"] == reference["channels"], filename
