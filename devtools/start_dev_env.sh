#!/usr/bin/env bash
# Explicit creation only; activate and install the editable clone separately.
# Usage: bash devtools/start_dev_env.sh --manager mamba --name pharmacophoremt-dev
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python "${script_dir}/conda_environment.py" create \
  devtools/conda-envs/development_env.yaml --python-minor 3.14 "$@"
