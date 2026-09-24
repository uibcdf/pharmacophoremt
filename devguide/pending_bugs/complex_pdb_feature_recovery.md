---
summary: Recover chemical features from PDB complex during pharmacophore extraction.
issue: uibcdf/pharmacophoremt#5
status: active
opened: 2026-09-24
closed:
severity: high
verification: reproduced
area: [complex-modeling, chemical-features]
guard: tests/test_validation_eralpha.py::test_eralpha_pharmacophore_extraction
normative:
blocked_by: []
supersedes: []
---

# Recover chemical features from a PDB complex

## What

The ERalpha benchmark initially returned no interaction sites. MolSysMT's
direct RDKit conversion left the ligand with 47 bonds of unspecified order,
and the receptor pocket contained no detectable aromatic or hydrophobic
features. A malformed negative-charge SMARTS also used Unicode minus signs.

## How

The test converts `tests/data/eralpha_complex.pdb` to a MolSysMT object,
selects a 44-atom ligand and a 609-atom receptor pocket, and calls the
complex-based modeler. RDKit can infer the ligand bond orders from the
existing connectivity and coordinates. Converting the selected pocket
through MolSysMT PDB text lets RDKit apply standard protein residue
chemistry while preserving the selected atoms and coordinates. The
negative-charge SMARTS uses ASCII signs.

## Why

An empty pharmacophore, or one missing aromatic and hydrophobic features,
misstates the modeled complex. The defect also blocks the local policy
migration in `uibcdf/pharmacophoremt#3`.

## What is measured and what is assumed

Before the fix, the benchmark failed at `ph.n_interaction_sites > 0`.
Direct conversion gave zero protein features; PDB-text conversion yielded
31 donor, 45 acceptor, three aromatic-ring, and 48 hydrophobic pocket
matches. Ligand bond-order inference recovered an aromatic ring. The
existing test now passes all three scientific assertions, and the full
local suite passes 23 tests under pytest-receptor.

## What was refuted

Adding explicit hydrogens alone did not restore protein aromaticity.
Using the selected PDB text for the ligand restored some hydrophobic
matches but did not identify its aromatic ring; bond-order inference
was still required.

## Scope and exclusions

The conversion change is limited to complex-based modeling. Other
modeling methods retain their own input paths. The benchmark checks
features in one complex; it is not validation of every molecular class
or parameter threshold.

## Acceptance criteria

The ERalpha benchmark yields at least one site including aromatic-ring
and hydrophobic features, and the full test suite remains green. CI
and the MolSysSuite policy workflow pass on the published commit.

## Dependencies and risks

A ligand with incomplete atoms or unusual formal charge may need an
authoritative bond-order template. Inference errors should surface
instead of silently generating a chemically incomplete model.
