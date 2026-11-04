---
summary: Expose G3PS neighborhood and ranked-guess stages as reusable native tools.
issue: uibcdf/pharmacophoremt#28
status: resolved
opened: 2026-10-03
closed: 2026-11-03
verification: measured
area: [screening, modeling, validation, attribution]
guard: tests/test_ranked_seeds.py
normative: devguide/ranked_seed_workflow.md
blocked_by: []
supersedes: []
---

# G3PS stage-one tools

## Resolution — 2026-11-03

Reviewed and incorporated as the named ranked-seed source/API method. The
[new receipt](../evidence/ranked_seed_acceptance_20261103_summary.json) records
clean receiving head **9731e054b9eb56b5b9a121dd889af214773b0643**. All **82 fresh
controls** pass in 23.11 s without failures/errors/skips: 22 ranked-seed and 60
correspondence-geometry controls. Independent bounded assignment oracles, units/
motion/permutations, empty/unequal axes, masks, saved-report rejection, deterministic
ranking/duplicates, detached ownership, allocation preflight, consumer calls and
actual citation reuse retain their guards. No new full suite is claimed.

Fresh host-off/on capsules preserve the full 16-seed family. Ranked-all and plain
triplets perform 16 fits and retain the same eight accepted mappings/site geometries
(with 1e-12 nm numerical comparison); neither family is geometrically deduplicated.
Selecting one seed omits 15, performs one fit and returns a completed empty result,
missing the known four-feature solution. The selected report retains its omissions
and selection_exhaustive=False. Computation exhaustion remains different: both
16-entry neighborhood work under limit 15 and triplet enumeration under limit one
raise PHMT-E107/complete=False without a query. An empty comparison completes with
no assignment or G3PS credit. Cached saved comparison ranking remains reusable.

Twelve pose checks and two JSON/YAML round trips per tracking profile pass under
changed unit policies. Original reflected poses remain partial nonmatches at fit
.75; public MolSysMT placement replay and references match at one. Source atom
identity/state/coordinates remain unchanged under like-unit-policy comparisons;
off/on science agrees. Actual capture is 0 items/0 uses host-off and 14/77 host-on. Only
representative first models are retained in the capsule, alongside full reports,
all accepted seed geometries, evaluations and original references. No full-return
or distinct-physical-binding-mode claim is inferred from the eight alternatives.

All four original cookbook blocks execute (14 items/70 uses); saved-summary rereading adds
no credit. Strict isolated rendering passes with two neighboring link-target stubs.
The published page exactly matches that staged render: a prose-only correction
links already available refinement, and every executed Python block is unchanged.
The primary section 2.2.1 was freshly checked through
[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8658842/); this remains a declared
PHMT stage-one adaptation, not full G3PS. Earlier DOI/MDPI access failures retain
their dated identities. No new molecular rescue solver is introduced.

After owned tests/capsules/docs finish, the unchanged original comparison runs
seven frozen cases/two explicitly named strategies in 14 sequential isolated
workers. Ranked calls explicitly select n_seeds=1. Each has one warmup, three
measured calls and separate actual attribution. All 14 controls match their
expectations and summaries remain stable: eight completed, five completed-empty
and one expected PHMT-E107 failure. The failed baseline retains no completed
attribution payload. The ranked budget case legitimately schedules one selected
fit and completes under max_fits=1. All 42 samples, warmups, actual references,
source/input/provider/native hashes and thread settings remain archived.

Worker source/native identities match each other and controller snapshots; all
four source/native/helper/test/input/metadata comparisons remain stable. CPU/
parallel=False/one-thread policy is observed. The supported 300 s worker wall
allowance does not change scientific budgets. No owned test/build/benchmark load
overlaps timing; machine-wide exclusivity is not claimed. Whole-worker high-water
RSS after measurements is 302.3–507.1 MiB including setup/warmups,
not incremental call allocation. Times describe different selected alternatives/
coverage, including the real false negative. No equivalent-recall speedup, default
seed limit or universal ranking follows. Ranked-all calls are not timed.

All molecular construction/recognition/coordinates/fitting/copy/set/transformation
remain public MolSysMT operations. PHMT owns cached pharmacophoric neighborhoods
and selection; SciPy owns generic assignment. No runtime/test/fixture/scientific-
definition/provider/prefix/sibling change is needed. Only documentation/evidence
and the recipe prose correction change. Defaults are unchanged.

This resolves #28 source/API and the declared analytical comparison, not biology,
energetics, continuous/global optimality, clean installed/public/platform/hosted
qualification (#23/#10/#9; workspace #82). #29 refinement is already resolved;
translation/exclusion rescue retains separate scientific/provider ownership.
Next #15 prepared rigid pose-search acceptance independently checks proposal
completion, valid maximum-coverage early stops, failed-search accounting and
retrospective composition. #41 public/floor/installed receiving and legacy
retirement remain partial (review 2026-11-11); #60/#66 retain their scopes.
Addon/new release defer. Owned root /tmp/phmt28-acceptance-20261103-guahqzj6/,
LMMV/dprada, review 2026-11-17; no local process remains after closeout. Original
report text below is preserved; its pending-review/future-stage statements are
historical and superseded by this dated acceptance.

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
