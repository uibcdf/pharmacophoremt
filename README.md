# PharmacophoreMT

[![MolSysSuite: Scientific Component](https://img.shields.io/badge/MolSysSuite-scientific%20component-0b7285?labelColor=24292f)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#scientific-component)
[![MolSysSuite policy](https://github.com/uibcdf/pharmacophoremt/actions/workflows/molsyssuite-policy.yml/badge.svg?branch=main)](https://github.com/uibcdf/pharmacophoremt/actions/workflows/molsyssuite-policy.yml)
[![Python 3.11 | 3.12 | 3.13](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md)
[![License](https://img.shields.io/github/license/uibcdf/pharmacophoremt)](https://github.com/uibcdf/pharmacophoremt/blob/main/LICENSE)
[![Codecov](https://codecov.io/gh/uibcdf/pharmacophoremt/branch/main/graph/badge.svg)](https://app.codecov.io/gh/uibcdf/pharmacophoremt)

Coverage: PharmacophoreMT Python tests, uploaded from Linux/Python 3.13 on eligible full CI runs; weekly and conditional nightly recovery retain the existing cadence. The badge reflects the last uploaded report, which may lag later direct or skip-CI commits; it does not certify a full matrix or scientific correctness.

The development source supports Python **3.11–3.14** (`>=3.11,<3.15`). Release
**[0.4.0](https://github.com/uibcdf/pharmacophoremt/releases/tag/0.4.0)** is public
on the official Conda channel, with eight installed Linux/macOS arm64 × Python
3.11–3.14 cells passing. Exact artifact evidence and central admission are tracked
in [#23](https://github.com/uibcdf/pharmacophoremt/issues/23) and
[MolSysSuite #131](https://github.com/uibcdf/molsyssuite/issues/131); the Python
badge retains the centrally admitted range pending that disposition.

A Pharmacophore MultiToolkit designed to simplify and streamline the detection,
generation, analysis, comparison, and application of pharmacophore models in
drug-design strategies.

Install the qualified public molecular-provider context with:

```bash
conda create -n pharmacophoremt --strict-channel-priority -c uibcdf -c conda-forge pharmacophoremt=0.4.0 molsysmt=0.23.0
```

See [installation and qualification scope](docs/content/about/installation.md).
