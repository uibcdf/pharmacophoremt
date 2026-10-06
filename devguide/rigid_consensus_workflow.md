# Prepared rigid unaligned consensus

Local implementation, tracked by [#26](https://github.com/uibcdf/pharmacophoremt/issues/26).
This completes the first rigid unaligned ligand workflow using existing native
feature extraction, MolSysMT alignment, aligned matching and clique aggregation.
It does not qualify legacy modelers or biological pilots.

## Public reusable operations and ownership

`screening.get_rigid_feature_correspondences(reference_inventory, feature_inventory)`
operates on classical feature inventories with explicit units and original
occurrence indices. It performs no molecular access. PHMT owns chemical feature
compatibility and the pharmacophoric correspondence graph; NetworkX owns generic
maximal-clique enumeration. Consumers can use proposals outside consensus.

`screening.align_to_pharmacophore()` remains the existing fitting boundary. Its
native Structures anchor cloud, public least-RMSD fit, coordinates, copy and set
operations are all supplied by MolSysMT. PHMT does not extract provider-private
rotations, implement a local molecular solver or generate conformers/hydrogens.
The fit report records source and target centers, fitted selected atom coordinates,
source atom indices, state/frame context and the actual provider/version/options.
No new molecular provider capability is required for this slice.

`modeler.from_rigid_ligands()` owns the pivot, placement alternatives and consensus
decisions and calls the public `screening.get_rigid_feature_placements()` tool for
explicitly chosen mappings. Cached query construction is available independently
as `modeler.from_feature_inventory()`; completed report reading is available as
`validation.summarize_rigid_consensus()`. See [the modular comparison contract](rigid_strategy_comparison.md).
Each input is a prepared ligand_id/molecular_system record with optional
selection, structure_index and chemical_state. All inputs are read and validated
through MolSysMT-supported get_features before placement. The caller declares one
prepared frame per ligand and a non-periodic coordinate interpretation.

## Finite proposal families and ranked selection

The default `association_cliques` graph has one node `(reference feature index,
candidate feature index)` for every equal-kind pair. Edges require distinct indices
on both sides and internal distance differences no larger than `2 * distance_tolerance`.
This follows from the triangle inequality: if each of two fitted point pairs is
within tolerance, their internal distances can differ by at most twice tolerance.
This necessary condition is conservative and cannot establish a proper rigid fit.

Every inclusion-maximal clique with at least min_matches pairs and non-collinear
centers in both frames becomes a proposal. Enumeration counts unsupported and
degenerate cliques against the bound too. This is an association graph, distinct
from the aligned graph whose nodes represent one ligand's individual feature
occurrences. It is not a complete implementation of DISCO or frequent clique mining.
In particular, a smaller valid mapping contained in a maximal clique rejected after
fitting is outside this proposal family; no fallback silently changes the method.

`triplet_seeds` reuses get_correspondences on a query built from the pivot inventory,
with every site's radius equal to distance_tolerance. All non-collinear typed,
injective triplets passing the same invariant distance condition are proposed.
min_matches is the post-fit full-inventory requirement, not triplet size. This is
the existing bounded PHMT triplet method, not G3PS or Pharmer. It can recover
placements different from maximal-clique fits because their fitting objectives
use different anchor subsets. Neither family solves continuous tolerance
feasibility or guarantees the best globally matched-feature count.

`ranked_triplet_seeds` ranks that same triplet family using the public typed
neighborhood comparison and correspondence-ranking tools. See the
[ranked-seed contract](ranked_seed_workflow.md) for its G3PS section 2.2.1 adaptation.
`n_seeds=None` retains all triplets; a positive integer makes an explicit scientific
selection and records omissions. This can miss a valid fit and is separate from
resource exhaustion. The original default remains association_cliques.

Refinement is selected independently with refinement_strategy='greedy' and the
public [refinement contract](rigid_refinement_workflow.md). Both final and each_step
angular policies remain available. The default None retains one fit per proposal.
Greedy refinement may attempt multiple fits per proposal; minimum matching is
final acceptance and each seed contributes at most one best valid placement.
Both policies validate final matching fully. Growth anchors and final assignments
remain separate evidence; the final policy permits angularly invalid anchors.

## Fit, verify, combine

For every proposal, fit the source to the pivot through MolSysMT, extract its
features again and verify that kind/atom membership retains the occurrence index
domain. Every original proposal pair must now satisfy the positional tolerance
and donor-direction or unoriented aromatic-normal tolerance. Then reuse
get_aligned_feature_matches to obtain an injective maximum-cardinality, minimum-
distance pivot matching and require at least min_matches pairs.

An RMSD value alone cannot pass this test. Noncoplanar reflections may pass all
invariant distances yet fail the proper fit and absolute geometry check. Small
partial patterns can still be shared by reflected molecules; this is not a
molecule-wide chirality detector.

Keep all accepted placements, even if different proposals produce identical
geometry. There is no coverage-1 early stop and no implicit pose deduplication.
This preserves evidence and makes the finite proposal family reproducible;
geometric clustering with a declared equivalence rule is future work.

The pivot contributes its unchanged frame. A source with no accepted direct pivot
placement is `unplaced`; retain its original nonempty inventory in source evidence,
but supply an empty feature contribution to every aligned layout. It continues to
count in the input ligand denominator. An unplaced status neither means chemical
absence nor proves that the source cannot align to another ligand or another pivot.

Enumerate the Cartesian product of accepted placements and call
get_aligned_consensus_hypotheses separately for each layout. The pivot selects the
coordinate frame and direct fitting opportunities; it does not restrict discovery
to its own features. Existing aligned cliques enforce pairwise positions and
orientations, disjoint occurrence usage and common-ligand support across all sites
of a hypothesis. Joint support can exclude the pivot. Different layouts remain
separate alternatives; their IDs encode the declared occurrence domain, not
chemical identity independent of reindexing.

## Bounds and scientific completion

- max_graph_nodes applies separately to each association graph and each aligned
  layout graph; the two node types have different meanings.
- max_cliques counts all maximal cliques in each relevant enumeration, not only
  returned supported proposals/sites.
- max_trials bounds raw triplet candidate products per nonpivot source.
- max_fits bounds total molecular fits, checking each source's scheduled mappings
  before fitting that batch. The standalone placement tool checks its mapping
  count before fitting, independently of the consumer's global budget.
  With refinement, every initial/trial fit counts and each provider call checks
  the remaining global allowance before executing.
- max_layouts is checked on the full placement product before layout discovery.
- max_matrix_entries bounds each post-fit assignment matrix including dummy columns,
  and each distance/pair/padded-neighbor matrix in the ranked proposal family.
- max_combinations bounds attempted consensus extensions per layout.

An exceeded bound raises PHMT-E107 (or PHMT-E106 for assignment matrices).
Partial enumeration is never returned as an evaluated-empty consensus. Provider
failures also propagate without an alternate local molecular solver. Bounds on
graph size, products or enumerated outputs do not promise a wall-time deadline or
an internal NetworkX search-step budget.

`complete=True` means this pivot and this declared finite proposal/hypothesis family
were evaluated without exhausting resources. It does not imply exhaustive flexible,
continuous or multiple-pivot alignment. Empty models is a valid completed result
within that scope. Model sites begin essential with weight 1; support is not affinity.

## Evidence and optional attribution

The detached report retains criteria, source inventories, accepted/rejected fit
evidence, correspondence counts, layouts and aligned hypothesis evidence. Each
model retains its selected placement/layout, original source/frame/state records,
site evidence and input support accounting, and survives native JSON persistence.

With attribution explicitly enabled, the composed operation uses the existing
single calculation capture. Bron--Kerbosch/Tomita are credited when their NetworkX
branch is reached, Crouse when SciPy assignment executes, and Kabsch when the
MolSysMT least-RMSD fit succeeds. The Kabsch criterion is attached to the provider's
documented method with its observed software version; no private backend algorithm
is inferred. Standalone triplet proposals do not credit unexecuted clique solvers.
Ranked proposals credit the adapted G3PS seed stage when reached, explicitly
excluding refinement, translation rescue and exclusion correction. Other
unimplemented alternatives in [the strategy survey](pharmacophore_search_strategies.md)
remain design citations and are not added to run bibliographies.

## Executed controls

`tests/test_rigid_consensus.py` covers proper rigid-motion recovery by both methods,
noncoplanar reflection and distortion controls, an independent injective permutation
oracle for a small association graph, six symmetric mapping alternatives, missing
feature/unplaced support accounting, source immutability, selection/frame/unit/pivot
behavior, all principal resource gates, provider failure propagation, real Ackredit
branch capture and native JSON retention. Fixtures have analytical coordinates and
declared chemistry; they are not experimentally validated pharmacophore cases.

See the [executable cookbook](../docs/content/cookbook/rigid_consensus.md).
