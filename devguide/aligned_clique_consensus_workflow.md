# Native aligned clique consensus

Local implementation owned by [#24](https://github.com/uibcdf/pharmacophoremt/issues/24),
following the [clique review](clique_consensus_review.md) and the delivered
[reference-anchored method](aligned_consensus_workflow.md).
Method: `aligned_maximal_clique_consensus@1`; recognition: `classical_atomic_formal@1`.

## Reusable tools and ownership

`get_aligned_feature_cliques()` accepts native feature inventories and declared
unique ligand IDs. It builds a pharmacophoric compatibility graph and calls
NetworkX's generic `find_cliques()` implementation. The graph has one node per
feature occurrence, and edges only for different ligands with equal kinds,
compatible absolute centers and compatible orientations. No reference ligand
anchors discovery. A donor vector is directed; an aromatic plane normal is an
unoriented axis. Each clique therefore has at most one contribution per ligand.

`get_aligned_consensus_hypotheses()` reuses that tool and `get_consensus_sites()`.
It aggregates each maximal clique separately; overlapping alternatives do not
weaken the existing aggregation contract. Centers are unweighted feature means.
The first member ordered by ligand ID provides the recorded orientation, with
all member deviations checked. There is no molecular or angular averaging kernel
implemented here.

`from_aligned_ligand_cliques()` obtains each selected prepared frame/state through
public MolSysMT-supported `get_features()`, calls hypothesis discovery and creates
Feature + Shape models through the shared site constructor. It returns models
in deterministic hypothesis order and a detached scientific report. Every model
retains its selected sites, correspondence/source evidence and original attribution.

PharmacophoreMT owns compatibility of pharmacophoric occurrences, hypothesis
constraints and model construction. NetworkX owns generic graph enumeration.
MolSysMT owns molecular recognition, selection, chemistry, coordinates and
transformations. No new molecular preparation, hydrogen-generation or conformer
tool is implemented. The ERalpha preparation gap remains
uibcdf/molsysmt#298/uibcdf/molsysmt#300, tracked by local #22.

## Exact scope and alternative hypotheses

Discover all inclusion-maximal pairwise-compatible site cliques, including
different clique sizes. `min_support` is a count of unique declared ligands,
not features or conformers. Empty inventories count in every support denominator.
Chemical/dataset duplicate identification is the caller's responsibility.

The second tool enumerates inclusion-maximal feasible packages of the discovered
candidate sites. A package cannot reuse a feature occurrence, and the intersection
of all its site supporters must reach `min_support`. Pairwise intersections are
insufficient: three sites can each share two supporting ligands with the others
while sharing only one ligand across the whole package. `min_sites` filters the
resulting maximal packages. Alternative packages may reuse occurrences across
different hypotheses; each is an independent editable model, not a merged query.

Completeness applies to this declared family of packages of maximal site cliques.
The method does not enumerate every site subclique or claim all joint molecular
patterns, DISCO superpositions, published RDP equivalence or optimal affinity.
Restricting a larger site clique to a smaller supporting population could permit
other packages outside this first method's scope. That extension requires a
separate scientific definition and reference controls.

Groups/members are canonicalized by ligand ID and local feature index, and
hypotheses by their candidate-site indices. IDs such as `site_00000` and
`hypothesis_00000` are deterministic within that occurrence domain; they are not
chemical identities stable across feature reindexing or changed input definitions.
Reordering inventories with the same ligand IDs preserves canonical choices;
feature reindexing preserves physical patterns after correspondence remapping.

All sites begin essential with weight 1. Shared support is correspondence evidence,
not affinity or an automatic essential-site decision. The emitted `radius` is
independent of discovery tolerance and can reject a supporting placement. Curate
site requirements, weights and radii before biological use.

## Limits and completion

| Parameter | Default | What it bounds |
| --- | --- | --- |
| `max_graph_nodes` | 64 | All input feature occurrences, before graph construction |
| `max_cliques` | 1000 | Enumerated maximal cliques, including unsupported ones |
| `max_combinations` | 10000 | Attempted site-package extensions, including infeasible ones |

Graph size bounds pair construction and graph storage. NetworkX iterates cliques;
the consumer never materializes an unbounded clique list. Its output bound does
not provide an internal solver-step or wall-time guarantee. Package enumeration
is a task-specific deterministic traversal of occurrence/support constraints,
not a copied generic clique solver. Input recognition, provenance and model copies
are outside a total-memory guarantee; no speed benchmark is claimed.

Exceeding a bound raises catalog-backed `PHMT-E107` with stage, observed resource,
limit and `complete=False`. No partial model or negative result is returned.
Successful empty discovery has `complete=True`, no hypotheses and no usable
models. It remains distinguishable from unresolved computation.

## Executed references and portable evidence

NetworkX documents its nonrecursive maximal-clique implementation as based on
[Bron and Kerbosch (1973)](https://doi.org/10.1145/362342.362367), adapted by
[Tomita, Tanaka and Takahashi (2006)](https://doi.org/10.1016/j.tcs.2006.06.015).
The source for the implementation identity and bibliography is the
[provider documentation](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.find_cliques.html).

With optional attribution enabled, credit these as `reference_implementation`
only when the nonempty graph reaches `find_cliques`. Credit NetworkX's loaded
version as `executed_software` and its
[recommended description](https://networkx.org/documentation/stable/#citing)
as `software_description`; retain the actually reached numerical/molecular
providers. An evaluated nonmatching graph has execution evidence; an empty graph
does not credit an unexecuted clique algorithm. RDP, DISCO and frequent labeled
pharmacophore clique papers remain design references rather than runtime credits.

Use the existing deferred Ackredit capture and application session. Each derived
model carries a detached copy of the bibliography for the entire generation
calculation, even when another result already credited the same references.
The top-level result retains the same original producer and software versions.
Model JSON and fresh readers preserve these records without recording another
calculation. Provider absence/failure preserves the scientific outcome and
host-owned declarations, including under warnings-as-errors. No import hooks,
enrichment or automatic session replacement is enabled.

## Verification

`tests/test_aligned_cliques.py` uses independent subset oracles for feature cliques
and feasible packages, fixed-seed bounded cases, same-ligand/repeated-type controls,
unequal maximal sizes, absent-reference patterns, triple intersection failures,
orientation/units, reordering and strict resource boundaries. Molecular controls
exercise public MolSysMT recognition, selected frames, unchanged source coordinates,
multiple alternative models, screening and native JSON persistence. Real Ackredit
controls exercise repeated references, enclosing capture/session, original versions,
detached models, executed/empty branches, true absence, failures and fresh readers.

The [cookbook recipe](../docs/content/cookbook/aligned_cliques.md) executes the
prepared-ligand route and standalone inventories, inspects alternatives and renders
the bibliography. Dated test/build results and controlled provider revisions are
retained in the checkpoint/report. This is analytical local evidence; biological
validation, installation and hosted supported-matrix acceptance remain separate.
