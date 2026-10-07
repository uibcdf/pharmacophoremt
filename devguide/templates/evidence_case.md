# Case title

Copy this template into `docs/content/validation/<case>.md`, replace the prompts,
and link it from the collection index. Follow `devguide/validation_collection.md`.
Use links to canonical data, contracts and outputs instead of copying them.

## Identity and claim

- Case ID, owning issue, accountable maintainer and dated review.
- Evidence class: analytical, scientific validation, retrospective screening,
  vertical pilot or computational benchmark. Name a narrower control scope.
- Scientific question, tested claim and explicit untested boundaries.
- Original measurement date/run ID, producer identity, full result and summary
  links/checksums. Distinguish historical evidence from current execution.

## Inputs and preparation

- Dataset origin/URLs, acquisition date, citations and redistribution/license
  policy source. List immutable files/manifests and hashes; preserve originals.
- Molecular/ligand counts and selection, chemical/protonation/stereo states,
  hydrogens, bonds, coordinates/frames and explicit measurement units.
- Public MolSysMT preparation operations, backend/options, transformations,
  readiness evidence and input-immutability controls.
- Independent reference/oracle, declared tolerances, positive/negative cases,
  failed preparation/calculation records and what is assumed.

## Execution and environment

- Link executable driver/recipe/notebook and provide its exact command.
- Python/provider versions, supported environment/bootstrap route, producer Git
  identity, dirty overlay/source hashes, native extension identity and artifact
  hashes when applicable. A requirements list alone is not executed evidence.
- Method, backend, execution plan, selected features/states, parameters/units,
  deterministic ordering or random seeds, finite budgets and completion scope.
- Named scientific/regression guards; separate cheap archive checks from
  reexecution. State what must trigger a new run and who reviews it.

## Scientific results

- Measured results with independent expected values and declared tolerances.
- Original and evaluated ligand-level counts, repeats/conformers, valid zero
  scores, failed/missing outcomes and inclusion/denominator policy.
- For activity-based evaluation: endpoint/labels, training/test split,
  molecular/series overlap and leakage controls, class balance, uncertainty and
  failed-input sensitivity. Mark not applicable with a reason otherwise.
- For search: hypotheses returned, coverage, budgets, incompleteness and misses.
  Empty results must remain separate from calculation failures and inactivity.
- Portable actual Ackredit payload/item/use links, input-data versus resource
  citations, reached method/software versions and separately reviewed literature.
- What these observations establish and what remains unqualified.

## Computational performance, when measured

- Equivalent scientific outputs/oracle and the explicit comparison gate.
- Input/workload sizes, hardware/OS, thread/process/GPU settings and backend.
- Initialization/compilation/warmups, timing boundary, repetitions and all samples.
- Memory definition/scope, units, uncertainty/variation and interfering workloads.
- Failed or incomplete workloads and different search coverage/alternatives.
- Mark not measured for count-only or scientific controls; do not infer runtime
  superiority from fewer fits or memory efficiency from lifetime RSS alone.

## Maintenance and publication

- Owning issue/maintainer, review/update trigger and current blocker issues.
- New measurements append a distinct run identity; corrections preserve original
  evidence and explain their effect. Never replace an original archived output.
- Links to shared pilot receipts and provider handoffs where relevant.
- Required hosted/installed/public qualification stays independent of this case.
