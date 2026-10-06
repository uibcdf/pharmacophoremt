---
summary: Expose G3PS neighborhood and ranked-guess stages as reusable native tools.
issue: uibcdf/pharmacophoremt#28
status: active
opened: 2026-10-03
closed:
verification: measured
area: [screening, modeling, validation, attribution]
guard: tests/test_ranked_seeds.py
normative: devguide/ranked_seed_workflow.md
blocked_by: []
supersedes: []
---

# G3PS stage-one tools

## What

Implement the independently useful neighborhood-comparison and multiple-guess
ranking stage of the G3PS primary paper, then consume it through modular proposals,
MolSysMT placement and consensus.

## How

The [maintained contract](../ranked_seed_workflow.md) declares uniform tolerances,
unmatched-neighbor padding, finite-family/selection semantics, resource bounds and
ownership. Two public tools feed ranked_triplet_seeds, preserving the original
default and all-seed proposal family. Ackredit names only the reached adapted stage.

## Why

Expensive molecular fits can be prioritized using typed feature environments,
without tying this descriptor to consensus or rebuilding geometry. Heuristic
selection can miss valid mappings, so a reflected typed tetrahedron protects the
limit alongside the positive rigid-motion and independent assignment controls.

## What is measured and what is assumed

Primary paper sections 2.2.1–2.2.4 were inspected. All 22 new controls passed
on Python 3.14.7; the combined initial stage/attribution run passed 29 tests.
The complete suite passed 248 tests in 209.61 s with the installed environment
providers and no PYTHONPATH overrides. The only two warnings remain the intentional
optional-provider failure and legacy unit-stripping control. The new cookbook
executed four blocks; the isolated strict Sphinx build passed using the existing
3.13 documentation tools. Reporting/index checks, Ruff and whitespace checks pass.
All 14 sequential analytical comparison controls passed with one warmup, three
timed calls and separate actual attribution capture. Scientific outputs were stable
and source/extension hashes identical across workers. The retained evidence and
measured table are linked from the maintained contract. One selected seed reduces
fits and alternatives, and misses the guarded four-feature alignment. No whole-G3PS
replication or universal speed gain is assumed. The original method's translation
solver is unspecified.

The implementation and retained measurements are synchronized in
[the owning issue's evidence comment](https://github.com/uibcdf/pharmacophoremt/issues/28#issuecomment-5969056421).
The issue remains open pending review and incorporation of the working changes.

## Alternatives and refuted paths

Ordinary triplet fitting does not reproduce G3PS. Ranked seeds alone do not
implement greedy extension, translation rescue or exclusion-volume dodging.
Rejecting by a neighborhood score or clipping enumeration to satisfy a work
budget would change recall or misrepresent completion. Assignment is reused
from SciPy and all molecular operations remain with MolSysMT.

## Scope and exclusions

Public ranking-stage contracts, consumer composition, frozen analytical controls,
actual citations, opt-in comparison and executable recipe. Greedy refinement and
rescue need separate contracts, as do custom/per-feature tolerances and optional
site semantics. No biological, published-package, external-tool speed, Rust/GPU
or global optimality claim. Publication packaging remains #20.

## Acceptance criteria

Independent oracle and real-provider controls pass. All-seed proposals retain
the baseline family; selected and exhausted work remain distinct. Summaries
preserve omitted counts. Actual adapted-method/solver attribution survives reuse.
Recipe, report/index and full integration checks pass; comparisons retain stable
scientific outputs, source/input hashes and the false negative.
