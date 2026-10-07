"""Delegate explicit create requests to the qualified shared operator."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from conda_environment import main  # noqa: E402 — local owner tool path

if __name__ == "__main__":
    sys.argv[1:1] = ["create"]
    raise SystemExit(main())
