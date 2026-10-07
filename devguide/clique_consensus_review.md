# Distance partitioning and clique consensus: review and proposed contracts

**2026-10-07 completion of #18:** The public legacy builder is retired.
`LigandBasedModeler` requires an explicit prepared native `rigid` or
`aligned_cliques` method; see [the migration contract](ligand_based_workflow.md).
Its class/list syntax is preserved, while site minima, joint support, hypothesis
order and full reports follow those native contracts. The original review below
remains historical evidence. Its executable audit now uses two frozen historical
helpers in `devtools/legacy_clique_helpers.py`, copied from the recorded original
source revision/hash without a molecular or public build API. The native methods'
independent oracles and transition guards replace the defective route; no repaired
RDP, legacy equivalence or biological acceptance is claimed.

Reviewed 2026-10-02. The legacy audit belongs to
[issue #18](https://github.com/uibcdf/pharmacophoremt/issues/18).
This is a review and implementation strategy, not a validated new consensus
implementation or a performance benchmark. Feature + Shape remains the model
representation; a graph is a method's intermediate representation.

The first native reference-anchored method is now implemented locally under
[issue #21](https://github.com/uibcdf/pharmacophoremt/issues/21); see the
[aligned-consensus contract](aligned_consensus_workflow.md). It supplies reusable
fixed-frame matching and explicit correspondence-group aggregation. It does not
repair the audited legacy hybrid or claim exhaustive graph-pattern discovery.

The next native aligned method is now implemented locally under
[issue #24](https://github.com/uibcdf/pharmacophoremt/issues/24); see
[aligned clique consensus](aligned_clique_consensus_workflow.md). It discovers
maximal compatible site cliques without a reference anchor, then packages them
with disjoint occurrences and joint ligand support. NetworkX performs generic
clique enumeration, with executed implementation references captured through
Ackredit. This is a declared bounded family of packages of maximal site cliques;
it does not establish RDP/DISCO parity, unaligned discovery or biological validation.

## What the current implementation actually computes

`modeler/ligand_based.py` enumerates fixed-size feature subsets, groups them by
sorted feature names, recursively bins their distance vectors, flattens surviving
boxes and links candidates whose distance-vector RMSD is at most 0.15 nm.
It enumerates maximal cliques with NetworkX and emits the coordinates of one
candidate, scoring the variation of distance vectors within its clique.
It does not compute the documented aligned consensus centers.

The executable bounded audit is `devtools/audit_legacy_cliques.py`. It uses the
actual legacy helper methods with synthetic arrays, without constructing or
modifying a molecular system. In the controlled development environment it gives:

| Counterexample | Measured result | Consequence |
| --- | --- | --- |
| Distances 0.10 and 0.20 nm, two ligands | Pair RMSD 0.10 nm; zero surviving boxes | The partition filter rejects a pair accepted by the subsequent predicate |
| Distances 0.001 and 0.002 nm, two ligands | Four flattened entries, two original identities | Overlapping boxes duplicate candidates |
| B:0.04, A:0.10, A:0.20, B:0.26 nm | One maximal clique supported only by A | Minimum distinct-ligand support per box does not enforce support per clique |
| Reorder the same labeled four-point pattern | Ordered distance vectors differ | Sorting names without transforming correspondences does not canonicalize geometry |
| Reflect a noncoplanar four-point pattern | Distance vectors remain identical | Distances alone cannot distinguish handedness |

Additional source findings: candidates from the same ligand can share an edge;
clique enumeration is materialized without a budget; candidate identities and
equivalent hypotheses are not deduplicated; support/alignments are not retained;
the seed choice determines the output coordinate frame. Direct RDKit recognition,
coordinate access and automatic conformer generation still need migration to
MolSysMT-supported operations. These findings do not establish a defect in the
published RDP method: this local hybrid must be judged against its own predicates.

## Primary literature and distinct graph problems

**Recursive distance partitioning.** Zhu and Agrafiotis (2007),
[10.1021/ci7000583](https://pubmed.ncbi.nlm.nih.gov/17547387/), partition feature
lists in distance space, allow assignment to multiple boxes and prune recursively.
Their boundary-coverage guarantee is a property to reproduce under explicit
matching assumptions, not something provided by any arbitrary overlap width.
Our filter must conservatively retain every candidate accepted by the final
criterion, including the declared metric and tolerance.

**Clique-based mapping / DISCO.** Martin, Bures, Danaher, DeLazzer, Lico and Pavlik
(1993), [10.1007/BF00141577](https://pubmed.ncbi.nlm.nih.gov/8097240/), use clique
detection to find superpositions including conformations of the input molecules,
with point-type and chirality requirements. This motivates a compatibility graph
with explicit correspondence and conformation constraints, followed by geometric
verification. A clique of our whole candidate subsets is not automatically the
same construction as an association graph of individual point correspondences.

**Frequent labeled cliques.** Podolyan and Karypis (2009),
[10.1021/ci8002478](https://pmc.ncbi.nlm.nih.gov/articles/PMC2631088/), mine cliques
whose vertex labels identify feature types and whose edge labels encode binned
distances. Support is counted by molecule, with at least one supporting conformer,
not by total conformer occurrences. Their second algorithm exploits similarities
between a molecule's conformers. This is a promising separate method for many
prepared conformers and multiple binding patterns. Exhaustiveness in the paper's
discrete representation must not be presented as exhaustiveness over continuous
conformational space or over arbitrary Feature + Shape geometries.

**Maximal versus maximum/weighted cliques.**
[NetworkX's maximal-clique solver](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.find_cliques.html)
implements Bron–Kerbosch with the Tomita adaptation; output order is arbitrary
and output size can be exponential. Bron–Kerbosch (1973):
[10.1145/362342.362367](https://doi.org/10.1145/362342.362367);
Tomita, Tanaka and Takahashi (2006):
[10.1016/j.tcs.2006.06.015](https://doi.org/10.1016/j.tcs.2006.06.015).
A maximal clique cannot be extended; it need not be largest or scientifically
best. [Maximum-weight clique search](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.max_weight_clique.html)
uses branching with upper bounds and a different objective. Consider it when
weights have an explicit scientific meaning, and consider bounded ranked
alternatives when several modes matter. These are engineering candidates, not
claims that a single optimum captures the relevant binding mechanisms. NetworkX's
current weighted solver requires integer node weights; do not silently quantize
continuous potency or geometric objectives.

**Useful alternatives outside clique mining.**
[PharmaGist's multiple flexible alignment](https://pmc.ncbi.nlm.nih.gov/articles/PMC2699263/)
(Schneidman-Duhovny et al., 2008; 10.1089/cmb.2007.0130) provides a pivot/alignment
comparison, with geometric hashing and multiple-alignment stages.
[3D pharmacophore signatures](https://pmc.ncbi.nlm.nih.gov/articles/PMC6321403/)
(Kutlushina et al., 2018; 10.3390/molecules23123094) use complete labeled graphs,
signatures and VF2 subgraph matching; this is not maximal-clique enumeration.
These approaches can inform indexing, canonicalization and benchmark baselines
without forcing every approach through a clique solver.

## Recommended first implementation and subsequent comparison

First build a small native consensus workflow over **prepared, already aligned
ligands**, using `get_features()` and the native recognition definition. Preserve
source ligand/frame/feature identities and return an editable Feature + Shape
hypothesis with per-site support, dispersion and provenance. Make essential-site,
weight and shape choices explicit; frequency alone does not establish causality.
Use this small workflow as the reference against which graph-based discovery is
tested. Unaligned inputs must subsequently use provider-supported alignment.

For the first clique discovery method, keep distance partitioning as an optional
conservative prefilter. Separate candidate generation, compatibility construction,
search, geometric verification, consensus aggregation and ranking. Require:

- Type-preserving correspondences, including permutations among repeated types;
  one occurrence cannot fill multiple sites. A canonical signature retains the
  mapping back to original features, frames and chemical states.
- Distinct-ligand support. A candidate-subset compatibility graph has no edges
  between candidates from the same ligand. Association-graph methods need their
  own injective point mapping and consistent-conformer constraints instead.
- Proper rigid fitting through MolSysMT, followed by residual, direction/normal,
  chirality and exclusion checks. Pairwise compatibility alone is insufficient
  proof that all candidates satisfy one common alignment and shape criterion.
- Consensus centers and angular statistics in the verified common frame. Treat
  aromatic normals as axes and donor vectors as directed; do not average raw
  coordinates or signs from unrelated frames. Preserve alternative mappings/modes.
- Separate distance-bin widths, compatibility tolerances, final fitting tolerance
  and emitted shape radii. Record each value and the definition that interprets it.
- Streaming output, deterministic ranking/deduplication, explicit support and
  objective, and budgets for candidates, graph size, search and returned models.
  Budget exhaustion yields incomplete evidence, not a scientific negative.

Then compare frequent-clique mining with the compatibility method on repeated
features, outliers, multiple conformers, reflections, boundary perturbations and
independent decoys. Measure recall against a bounded exhaustive oracle, distinct
ligand coverage, geometric validity, memory and runtime before selecting a default.
Published speedups on other datasets do not establish a speedup here.

## Owning reusable operations

| Operation | Owner and consumer boundary |
| --- | --- |
| Molecular reading, selection, chemistry, feature participants, conformers/states and transformations | MolSysMT; PHMT calls documented public tools and reports missing capabilities there |
| Distances between molecular positions, proper rigid fitting, molecular geometric descriptors | MolSysMT; use or extend independently useful tools there rather than copying molecular kernels |
| Generic maximal/weighted-clique solvers or graph isomorphism | Existing graph providers, initially NetworkX; do not add pharmacophoric policy to MolSysMT or duplicate a generic solver |
| Pharmacophoric signatures, correspondence compatibility, ligand support and hypothesis aggregation/ranking | PharmacophoreMT, as separately reusable tools with unit-bearing contracts and tests |
| Angular statistics on molecular geometry | Inspect MolSysMT's public coverage first; propose a provider tool if it is independently useful; choice of pharmacophore geometry remains PHMT policy |
| Bibliographic capture, work identity and bibliography rendering | Ackredit; PHMT declares reached criteria, software versions and result provenance |
| Shared packaging/CI/distributed-execution policy | MolSysSuite; owning scientific kernels keep their provider boundary |

No provider gap has yet been demonstrated by a real native consensus consumer;
do not create a speculative dependency or duplicate a prospective capability.
If a gap blocks that consumer, open a provider issue with linked local evidence.
Packed candidate/edge arrays and explicit completion metadata should allow a
profiled CPU/Rust backend and later batch, distributed or GPU execution without
changing the scientific method. Parallel scheduling must preserve support,
deterministic result identity and completion semantics.

## Attribution boundary

The publications above are design references. They are not currently credited as
executed native algorithms. Instrument a method only when its implemented branch
is reached, distinguishing scientific criterion, referenced implementation,
executed software/version and software-description papers. The native integration
is documented in [the attribution cookbook](../docs/content/cookbook/attribution.md)
and owned by [issue #19](https://github.com/uibcdf/pharmacophoremt/issues/19).
