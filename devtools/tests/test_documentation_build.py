"""Exercise the complete documentation in its installed ordinary environment."""

import subprocess
import sys
from pathlib import Path


def test_full_documentation_build_without_warnings(tmp_path):
    """Missing extensions, pages, references or invalid headings fail the gate."""
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-b",
            "html",
            "-W",
            "--keep-going",
            "-E",
            "-a",
            str(root / "docs"),
            str(tmp_path / "html"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / "html/index.html").is_file()
    assert (tmp_path / "html/content/about/citation.html").is_file()
