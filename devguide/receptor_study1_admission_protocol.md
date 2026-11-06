# Receptor-based ERalpha study1: admission and design protocol

Owner LMMV/dprada, [#103](https://github.com/uibcdf/pharmacophoremt/issues/103), revision1, 2026-11-06. **Status: admission stage only.** No eligible primary assay/cohort, primary receptor preparation, complete construction method or numerical experiment is frozen or evaluated by this document. It specifies the next decisions and stop conditions before affected activity/structure/score stages; it does not redefine the goal as completing a protocol.

## Scientific question and endpoints

Test whether explicitly declared receptor-derived pharmacophore hypotheses help discriminate stronger binders from experimentally weak or negative compounds in a human ERalpha assay relative to fixed simple comparison methods. Primary source eligibility targets ligand-competition/binding with original methods and defined species/isoform/construct. Cellular agonism, crystallographic pose recovery, contact geometry and affinity prediction remain different questions. The second receptor remains unselected pending an independent data/feasibility review.

The old ligand-reference agonist cohort is already exposed development material, not a fresh binding holdout. Preserve #62/#63/#64 outputs and #66's fixed ligand-query protocol. Reusing its source/endpoint/exposure safeguards does not silently replace its method with this receptor study. Any shared future cohort/comparison needs a separate dated declaration before the affected stage, preserving all original plans.

## StageA: preparation and capability admission

Use the [read-only audit](receptor_preparation_admission_audit.md) as receiving evidence, not biological acceptance. The archived1QKU fragment remains a development/control input. A biological source must be chosen and justified against the admitted assay construct and source quality before scoring; it is not selected for a favorable pharmacophore answer. The current fragment's state, termini, stereo and local H choices do not become biological truth by reuse.

| Required decision | Current authoritative evidence | Next action / owner |
| --- | --- | --- |
| Source/construct/assembly and pocket region | Deposited source and original fragment are traceable; no assay-matched complete receptor preparation is admitted | Review experimental source and assay methods, choose source/assembly and declare pocket/feature-selection policy. MolSysMT performs molecular inspection/selection/assembly; optional TopoMT is used only for an actual cavity/pocket method |
| Chemical states, H and stereochemistry | Explicit HIE/termini/local H in the control; readiness gaps and read-only CIP diagnostics are retained | Declare and justify state assumptions and accepted unresolved fields. Use supported MolSysMT preparation/assessment; never fill chemistry or reinterpret unknowns locally |
| H geometry and environment | Old near-contact diagnosis does not establish suitable H orientations | Receive a supported #323 composition/operation or qualified prepared input with explicit provenance and freezing/model/budget evidence. No PHMT optimizer or endpoint-coordinate restoration |
| Required acceptor-family directions | Native HIS524 model3 exists; GLU353 carboxylate directions are unsupported in the received profile | PHMT#105 now qualifies explicit source receiving of existing aromatic-N geometry (analytical witnesses only). MolSysMT#375 decides the carboxylate model/composition. Do not claim complete receptor coverage by silently dropping an essential unsupported family |
| Molecular identity, co-crystal/reference exclusion and series overlap | External IDs and source hashes alone do not prove molecular/series independence | Review/receive supported MolSysMT#447 annotation/correspondence composition under explicit state/stereo/isotope/normalization policies; preserve unresolved inputs/exposure records. PHMT owns split interpretation, not molecular descriptors |
| Geometry/steric quality assumptions | Readiness coverage and radii alone are not a plausibility certificate | Declare needed assessments and their applicability. General molecular assessments remain provider-owned (including #555); unsupported checks stay unassessed, with any study limitation explicit |

A provider may identify an existing supported composition. Proposals do not require a particular function name/backend. Keep source inspection, executed receiving and public delivery separate; do not edit sibling code under consumer authorization. These are first-study decisions, not new automatic proposed0.5.0 release gates or a demand to close every broader provider issue.

## StageB: data/source admission before new evaluation

Review #66's retained source-method handoff before making new data requests. Its earlier capacity stops and original-text access limits remain; no new method text, activity table or cohort is acquired here. Species/construct, experimental format, tracer/concentration/buffer, endpoint calculation, label thresholds and negative interpretation need original evidence. Do not substitute unspecified records or convenient generated decoys for measured weak/negative compounds.

Freeze a dated eligible source pool, original source occurrence IDs, exposure exclusions, molecular grouping and class-capacity rules before the corresponding activity selection. Keep construction/development and evaluation partitions separate, including co-crystal/reference identities and chemical-series overlap under the actual available provider policy. Unresolved aliases cannot be collapsed into a molecule or certified as unseen. Record all failed sources/inputs and stop if the declared source fails; do not choose another pool by AUC or visible favorable class balance.

## StageC: freeze the runnable method before scores

The construction contract must identify receptor region/state/structure, admitted donor/acceptor/aromatic families, exact explicit profile, distances, radii, directions, essentiality/weights, exclusions and deterministic alternatives. Define how alternatives become an evaluated method, with any selection or aggregation decided before holdout outcomes. Keep incomplete generation distinct from an exhausted negative. A position-only or ligand/complex-derived comparator may be declared as a comparator; it cannot silently replace the requested receptor method.

Reuse native PHMT generation, saved-model replay, matching and search. Molecular recognition/directions/coordinates, fitting and transformations remain MolSysMT-owned; docking/poses belong to DockingMT when actually required. Freeze ligand preparation/conformer input policy and source correspondence, all finite generation/search/conformer budgets and termination meanings. No default or copied example tolerance is a calibrated physical uncertainty; 1e-12nm identity checks are numerical controls.

Declare fixed ligand-reference/consensus or other simple comparisons with immutable query/method identities and the same eligible inputs/preparation/evaluation accounting. Existing seeded_hit@1 is a defined binary fitted-seed criterion, not affinity or generic continuous pose coverage; any changed scoring definition requires its own contract and controls before use. Do not tune query radii or methods on already observed evaluation outcomes.

Before execution, record the exact producer/environment/native bytes, input hashes, method/configuration, random seeds where used, scoring/metric definitions, tie handling, original/evaluated group counts, prespecified uncertainty and failure-sensitivity analysis. Use existing PHMT metrics/results and appropriate established statistical tools. Do not infer independent sampling from repeated conformers, hypotheses, states or unresolved molecular aliases.

## Execution and success conditions

StageA/B/C fields still unresolved must remain visibly pending; a runnable frozen plan must supply them before evaluation. Preserve failed preparation/calculation as unscored; a valid completed negative can have score0, while absent pose fit values keep their distinct meaning. Report all declared methods, denominators, search completion, preparation sensitivity, ties and uncertainty, including negative or inconclusive findings. No favorable result is manufactured to satisfy the goal.

A third party must reproduce the bounded study from frozen inputs/plans and compatible identified providers, replay its saved hypotheses and understand limits. Retain original receipts and actual attribution in the existing validation collection. Repeat that qualification on a second justified receptor; neither study is complete now. Supported source/installed/public delivery and the real release-candidate decision remain independent gates.

Shared-host scientific phases remain serial and bounded, with processors/RAM available to others. Choose feasible workloads from resource evidence before launching them; the previous whole-suite1GiB OOM is not permission to exhaust shared RAM. No new package, tag, Release, addon or unsupported biological claim is authorized by this protocol.
