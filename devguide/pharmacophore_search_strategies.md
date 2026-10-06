# Pharmacophore search and alignment strategy survey

Primary-source review, 2026-10-03. Consumer work is tracked in
[#26](https://github.com/uibcdf/pharmacophoremt/issues/26); the earlier
[clique/RDP review](clique_consensus_review.md) and its legacy counterexamples
remain relevant. Sources below describe published methods, not an assertion that
the latest commercial release exposes every algorithm unchanged. Published
speedups are not transferred to PHMT datasets or hardware.

## What is being optimized?

Separate common-pattern discovery, pairwise alignment and indexed library search.
They have different inputs and completion guarantees. Also separate minimum RMSD,
maximum Gaussian overlap and maximum number of features satisfying positional and
directional tolerances. These objectives can prefer different placements; the
[G3PS paper](https://doi.org/10.3390/molecules26237201) explicitly motivates its
matched-feature objective by this distinction. PHMT should preserve named strategies
and their criteria rather than choose a universal solver in advance.

## Alternatives and useful mechanisms

| Published strategy and primary source | Efficiency mechanism / problem | PHMT decision |
| --- | --- | --- |
| Martin, Bures, Danaher, DeLazzer, Lico and Pavlik (1993), [DISCO](https://doi.org/10.1007/BF00141577) | Clique-based common pharmacophore mapping over molecular conformations. | Keep association mapping as a baseline, with proper fitting and post-fit validation. Current maximal mappings are a bounded PHMT family, not full DISCO. |
| Zhu and Agrafiotis (2007), [RDP](https://doi.org/10.1021/ci7000583) | Recursively partition invariant distance descriptions and eliminate unsupported lists; assignment to multiple boxes protects boundary matches. | Worth a future exact prefilter comparison. First specify safe tolerance coverage and validate boundaries against an independent exhaustive oracle. |
| Podolyan and Karypis (2009), [frequent clique mining](https://pmc.ncbi.nlm.nih.gov/articles/PMC2631088/) | Mine labeled feature/distance graphs; multi-conformer methods reuse information between a molecule's conformers. Support counts molecules having at least one embedding. | Strong candidate for prepared conformer consensus. Keep discretization, conformer embeddings and molecule support explicit. It differs from maximal association mappings and aligned site cliques. |
| Wolber, Dornhofer and Langer (2006), [LigandScout rigid overlay](https://doi.org/10.1007/s10822-006-9078-7) | Distance/density characteristics guide feature pairing and reduce combinatorial pairing work. | Consider an environment-signature assignment baseline; verify its original full method before claiming replication. Cheap descriptors should rank proposals or use a proved safe rejection condition. |
| Permann, Seidel and Langer (2021), [G3PS](https://doi.org/10.3390/molecules26237201) | Greedy three-point search targets matched-feature count under feature tolerances rather than only RMSD/overlap. | Adapted seed ranking (#28) and independently usable greedy refinement (#29) are delivered with declared limits and policy counterexamples. Translation rescue and exclusion correction remain future stages; this is not full G3PS. |
| Schneidman-Duhovny, Dror, Inbar, Nussinov and Wolfson (2008), [PharmaGist deterministic flexible alignment](https://doi.org/10.1089/cmb.2007.0130) | Multiple flexible alignment identifies shared pharmacophoric patterns and alternatives. | Later compare multiple pivots and prepared conformer choices; first preserve placement evidence and avoid treating a single pivot as global multiple alignment. |
| Koes and Camacho (2011), [Pharmer](https://pmc.ncbi.nlm.nih.gov/articles/PMC3124593/) | Feature triplet indexing, KDB-tree spatial queries and Bloom fingerprints reduce work for database pharmacophore search, followed by alignment. | Good direction for repeatedly screening large prepared inventories. Account for index construction, storage and tolerance-safe candidates separately from pair alignment. |
| Koes (2018), [Pharmit backend](https://pmc.ncbi.nlm.nih.gov/articles/PMC8049614/) | Start with a rare query triangle using histograms, join compatible indexed triangles, then globally align. Database partitions and pipeline stages supply practical parallelism. | First evaluate rare/selective typed-seed ordering; then indexing/partitioning if representative repeated queries justify them. Query ordering alone does not reproduce Pharmit. |
| Taminau, Thijs and De Winter (2008), [Pharao](https://www.silicos-it.be/assets/papers/hdw-pharao-paper.pdf) | Prune feasible feature combinations by invariant distances, optimize Gaussian feature-volume overlap from several starts, and prune smaller subsets by overlap upper bounds. | A distinct continuous Feature + Shape strategy. Retain its overlap objective and compare coverage separately; do not translate an overlap bound into a coverage bound without proof. |

The original two baselines are `association_cliques` and `triplet_seeds` in
[the rigid consensus workflow](rigid_consensus_workflow.md). Both use the same
MolSysMT fitting boundary and the same post-fit absolute geometry criteria.
Association-clique fits can fail when valid smaller submappings exist; triplet
seeds can give a different placement from fitting a larger mapping. Agreement is
required on the declared rigid-motion controls, not on every continuous problem.
The default is currently the explicit maximal association family; it is not a
measured universal performance winner.

The [modular comparison](rigid_strategy_comparison.md), tracked in #27, now
contains a frozen warped-square counterexample: the full mapping's least-RMSD
fit gives zero matches at the requested tolerance, while triplet placements
give three. RMSD is compared over the same four feature pairs. Both finite
families finish according to their declared contracts; they return different
coverage and alternative counts. The public placement tool can accept another
proposal strategy without reconstructing extraction, fitting or verification.

## Inspectable external comparison candidates

The current [CDPKit alignment cookbook](https://cdpkit.org/master/cdpl_python_cookbook/pharm/processing/ph4_align.html)
exposes multiple output placements, an exhaustive-search option, orientation
handling and distinct positional matching modes. Its example strips exclusions
before pharmacophore-to-pharmacophore alignment. Therefore a comparison must
declare these flags and evaluate exclusions separately; accepting only a default
top pose would conflate output filtering with search completeness. This is useful
external reference behavior, not evidence that PHMT matches its underlying method.

[PyPharao's official repository](https://github.com/silicos-it/PyPharao) offers an
inspectable Gaussian-alignment implementation and identifies the original Pharao
paper as its citation. It uses RDKit-based feature perception. A future comparison
should first align equivalent supplied feature inventories and objectives, then
separately assess end-to-end recognition differences. Any molecular conversion,
preparation or geometry adapter in our ecosystem must go through MolSysMT. Neither
CDPKit nor PyPharao is added as a dependency or credited as executed in this slice.

## Implementation and comparison order

[#28's ranked-seed contract](ranked_seed_workflow.md) now implements independently
reusable neighborhood comparison and multiple-guess ranking from G3PS section
2.2.1, with declared uniform-tolerance/padding adaptations. Its explicit finite
selection can miss a known match. [#29's public refinement](rigid_refinement_workflow.md)
now exposes both angular policies, shared pair evaluation and best-state retention.
Controlled cases favor each policy in different circumstances. Both remain
available; an unfavorable bounded comparison is documented, not grounds for
removing another scientific option. Translation rescue and exclusion corrections
remain future stages; this does not implement full G3PS.

1. Deliver and test the two rigid baselines with shared fixtures and transparent
   proposal/fit/layout counts, including rejected fits and exhausted budgets.
2. Add counterexamples where minimizing RMSD misses a larger tolerance-valid
   matching. Review G3PS as an independently versioned strategy and compare both
   the scientific result and compute cost, including optional feature semantics.
3. Profile prepared multi-conformer workloads. Compare frequent-clique mining
   with safe RDP filtering; preserve molecule support rather than conformer counts.
4. Evaluate typed triangle signatures/selective ordering, then an invariant index
   for repeated screening. Keep recall against an unfiltered reference, including
   exact boundaries, reflected and nearly degenerate cases. Ordering is harmless
   when exhaustive; early stopping changes the guarantee and must be declared.
5. Compare Gaussian overlap as a separate objective, using existing Feature + Shape
   representations. Any generic point-set molecular fitting or shape geometry
   needed by sibling users belongs to MolSysMT or another identified owner.

No ranking of speed is accepted before controlled measurement. For each case,
retain immutable input provenance, feature definitions, preparation/state/frame
choices, units, tolerances, output-equivalence policy, source revisions, dependency
versions, CPU/thread settings, wall time, peak memory and warmup/repetition policy.
Record candidate products, graph nodes/edges, cliques, fits, rejected alignments,
layouts and output hypotheses. Report failed/incomplete cases independently of
scientific negatives. Include index build/load cost for indexed strategies and
both unique molecules and conformer counts for ensembles.

Small analytical controls provide geometry and accounting evidence. Biological
pilot/retrospective comparisons need independent controls, declared split/leakage
rules and verified preparation. The ERalpha gate remains provider preparation
work; this survey does not remove it. Publication packaging is the separate
[#20 decision](https://github.com/uibcdf/pharmacophoremt/issues/20).

## Acceleration and reusable ownership

Pharmit's backend illustrates that practical parallelism can depend on data layout:
its authors describe independent database partitions and pipelined search stages,
and report abandoning a shared-tree concurrent design in their tested setting.
This informs PHMT's design options; it is not proof of the best partition for PHMT.

Keep scientific method, compute backend and execution plan separate. Profile first;
move measured PHMT pharmacophoric graph/candidate bottlenecks to Rust while keeping
reference equivalence controls. MolSysMT supplies molecular fitting/transformation
and their accelerated backends. Distributed source batches, deterministic output
ordering, bounded membership arrays and batched GPU computations can be considered
when their costs are measured. No Rust/GPU/distributed PHMT implementation is claimed.

Offline research links are distinct from Ackredit runtime attribution. Only reached
implemented criteria/solvers/software are credited in a run. Register additional
published methods when their precise adapted implementation and attribution context
have been reviewed; a design survey does not earn runtime credit.
