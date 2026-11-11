"""Actual CI coverage must retain all three roots and unexecuted source files."""

import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ci_xml_keeps_same_basename_files_separate_and_unexecuted_files_visible():
    commands = re.findall(
        r"^\s*(python -m pytest .*--cov[^\n]*)$",
        (ROOT / ".github/workflows/CI.yaml").read_text(),
        re.M,
    )
    assert len(commands) == 1
    arguments = [
        "-p",
        "pytest_receptor.plugin",
        "-p",
        "pytest_cov.plugin",
        *shlex.split(commands[0])[3:],
    ]
    with tempfile.TemporaryDirectory(prefix="phmt-coverage-identity-") as directory:
        root = Path(directory)
        (root / ".coveragerc").write_bytes((ROOT / ".coveragerc").read_bytes())
        expected = set()
        for package in [
            "pharmacophoremt",
            "pharmacophoremt_results",
            "pharmacophoremt_features",
        ]:
            path = root / package
            path.mkdir()
            (path / "__init__.py").write_text("MARKER = " + repr(package) + "\n")
            (path / "shared.py").write_text(
                "def choose(flag):\n    if flag:\n        return 1\n    return 0\n"
            )
            (path / "unused.py").write_text("UNUSED = 42\n")
            expected.update(
                f"{package}/{name}.py" for name in ["__init__", "shared", "unused"]
            )
        private = root / "pharmacophoremt/_private"
        private.mkdir()
        (private / "__init__.py").write_text("")
        (private / "hidden.py").write_text("VALUE = 1\n")
        (root / "pharmacophoremt_results/_store.py").write_text("VALUE = 1\n")
        expected.add("pharmacophoremt_results/_store.py")
        (root / "test_probe.py").write_text(
            "import importlib\n"
            "def test_fixture():\n"
            "    for name in ['pharmacophoremt', 'pharmacophoremt_results', 'pharmacophoremt_features']:\n"
            "        assert importlib.import_module(name).MARKER == name\n"
            "        assert importlib.import_module(name+'.shared').choose(True) == 1\n"
            "    assert importlib.import_module('pharmacophoremt._private.hidden').VALUE == 1\n"
            "    assert importlib.import_module('pharmacophoremt_results._store').VALUE == 1\n"
        )
        environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("COV_CORE_") and key != "COVERAGE_PROCESS_START"
        }
        environment.update(
            PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
            PYTEST_ADDOPTS="",
            COVERAGE_FILE=str(root / ".coverage"),
        )
        child = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                "-c",
                "import json,sys;sys.path.insert(0,sys.argv[1]);import pytest;raise SystemExit(pytest.main(json.loads(sys.argv[2])))",
                str(root),
                json.dumps(arguments),
            ],
            cwd=root,
            env=environment,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        assert child.returncode == 0, child.stdout + child.stderr
        xml = ET.parse(root / "coverage.xml")
        classes = xml.findall(".//class")
        filenames = [row.attrib["filename"] for row in classes]
        assert len(filenames) == len(set(filenames))
        assert set(filenames) == expected, filenames
        assert int(xml.getroot().attrib["branches-valid"]) > 0
        for row in classes:
            hits = [int(line.attrib["hits"]) for line in row.findall("./lines/line")]
            assert hits
            if row.attrib["filename"].endswith("/unused.py"):
                assert set(hits) == {0}
            else:
                assert any(hits)
