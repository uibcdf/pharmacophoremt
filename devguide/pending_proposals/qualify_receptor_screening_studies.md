---
summary: Qualify a reproducible receptor-to-screening workflow on ERalpha and a second receptor.
issue: uibcdf/pharmacophoremt#103
status: partial
opened: 2026-11-06
closed:
verification: measured
area: [science, receptor, validation]
guard:
normative: devguide/validation_collection.md
blocked_by: []
supersedes: []
---

# Reproducible receptor-based screening studies

## What

The maintainer accepted this longer-term objective on 2026-11-06: construct explicit receptor-based pharmacophore hypotheses and test reproducibly whether they help select ligands. A third party should be able to reproduce two bounded studies and understand preparation sensitivity, useful behavior and failures.

## Stages and ownership

1. Consolidate current APIs, examples and real dependency/install contracts under #95/#9/#10/#23. Proposed 0.5.0 is not required to include both new studies.
2. Qualify the complete prepared-receptor, explicit-hypothesis, saved-model and ligand-evaluation workflow using current native operations and disclosed experimental profiles.
3. Extend the ERalpha evidence into a declared receptor-based retrospective study and qualify a scientifically informative second receptor. Review source data, provenance/redistribution and preparation feasibility before selecting that receptor.

MolSysMT owns molecular forms/formats, inspection, preparation, atom/state maps, transformations and reusable molecular geometry/calculations. PharmacophoreMT owns pharmacophore hypotheses, constraints, comparison, matching/ranking and study orchestration. Use the registered support libraries at their reviewed boundaries; optional pocket/docking needs belong to TopoMT/DockingMT when needed. Review provider code/contracts and report any missing general operation in its owning repository with consuming evidence; no consumer molecular fallback or unauthorized sibling implementation.

## What is measured and what remains

Existing analytical, preparation, pose, cached-generation and activity records retain their own original identities and limits. Their review is the first task; this proposal does not claim either complete new study has executed. #102 repairs two source-test envelope comparisons; it does not add scientific validation. #95's public MolSysMT delivery remains separate from controlled-source scientific work. Missing original-method texts remain #66; do not substitute invented methods.

## Initial review — 2026-11-06

The [initial evidence review](../receptor_validation_evidence_review.md) distinguishes the cellular agonist ligand-reference cohort from receptor geometric controls and #66's unqualified binding-source pool. No fresh study, molecular run or holdout is claimed. The next protocol must declare receptor construction and data eligibility before evaluation; it cannot silently replace #66's frozen ligand-query method.

## Prepared-input audit and first-study admission — 2026-11-06

The [read-only preparation/provider audit](../receptor_preparation_admission_audit.md) and [stage-A study protocol](../receptor_study1_admission_protocol.md) now separate actual source readiness/CIP/direction observations from biological eligibility. #104 removes a historical direct-CIF traversal with nine passing controls. New PHMT#105 owns consuming already delivered aromatic-N directions; measured carboxylate and H-refinement needs are handed to MolSysMT#375/#323. No new activity cohort, model/score or completed study is claimed.

## First work package

Inventory current ERalpha receptor-generation and screening evidence and distinguish analytical/preparation/pose controls from activity-based validation. Identify reusable frozen data, actual model construction and evaluated cohorts, preparation assumptions, leakage risks and existing comparisons. Produce the first bounded study protocol before selecting/tuning hypotheses or choosing the second target. Map concrete needs to already consumed MolSysMT capabilities, provider delivery or precise owning requests.

## Acceptance criteria

Freeze scientific questions, receptor/preparation assumptions, chemical states, input identities, activity/negative-label definitions, selection/splits, leakage controls and comparison methods before evaluation. Declare direction/weight/radius/exclusion choices and keep construction/tuning separate from evaluation. Retain failures and original/evaluated cohort counts. Report measured performance, preparation sensitivity and appropriate uncertainty, including negative/inconclusive results. No favorable result is manufactured or required to hide a method limitation.

Both bounded studies must be reproducible from frozen inputs/plans and identified compatible environments, with saved-model replay, actual attribution and original measured outputs in the existing validation collection. This supplies evidence toward an agreed classical 1.0 scope; it does not reserve a version/date, authorize publication or require the addon/dynamics/AI. Intermediate 0.x releases may continue through 0.10, 0.11 and later. Shared-host work remains serial and bounded, leaving RAM/CPUs to others.

## Native aromatic-N source receiving — 2026-11-06

#105 is resolved by the [explicit profile](../public_cached_aromatic_n_generation.md),
with250 unique passing selected controls and actual MolSysMT cache/model/witness
receiving. The older profiles remain compatible, and molecular work stays in
MolSysMT. The two models/eight primary/two recovered analytical evaluations are
not a binding study. Next admit original assay methods and cohort/exposure rules,
resolve preparation/state/family decisions with their providers, and review the
second receptor's data/feasibility; keep both full studies and #103 open.

## Second-target source/method receiving — 2026-11-06

#106 and its [bounded review](../receptor_study2_source_review.md) receive40
assay descriptions/39 distinct IDs and original BRD4 method material, preserving
all source/exposure/access limits. BRD4 BD1 is prioritized for further admission;
no experimental source, second target, cohort, receptor preparation or score is
accepted. HSP90 target associations alone do not qualify human binding: several
original protocols use rabbit-lysate luciferase refolding. Next resolve the
named original-method/construct/concentration questions and predeclare later
source/capacity/class/rights/exclusion rules. #66 remains separate; both studies
and the full parent objective stay incomplete. No molecular fallback is added.
