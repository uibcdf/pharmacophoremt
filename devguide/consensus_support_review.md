# Consensus support and controlled redundancy

Reviewed 2026-11-04 under [#80](https://github.com/uibcdf/pharmacophoremt/issues/80),
following the [native matching review](native_constraint_semantics.md).
Source base: `7ec284fafdf10a936ce93265caa80a5ae484ff43`.
This is a bounded interpretation/control review of audit 8–9/13. The existing
scientific definitions are retained; no new weighting or consensus algorithm
is introduced.

## Choose the scientific question

| Native method | Discovery / support condition | Geometry and emitted requirements | Main completeness boundary |
| --- | --- | --- | --- |
| `aligned_reference_consensus@1` | Features of one declared reference anchor discovery; each emitted site independently reaches `min_support` | Mean of members' feature centers, first member's orientation; sites begin essential, weight one | Pairwise reference matches and their consistent groups; no common-support requirement across all sites and no global reassignment after rejection |
| `aligned_maximal_clique_consensus@1` | Reference-free maximal site cliques; a package's **intersection** of site supporters reaches `min_support`, with no reused typed occurrence | Unweighted feature means, lexicographically first ligand member's orientation; each package is a separate essential/unit-weight model | Maximal feasible packages of maximal site cliques; not all subcliques or globally optimal molecular patterns |
| `pivot_rigid_clique_consensus@1` | Declared proposal family fits prepared frames to a pivot using MolSysMT; clique joint support applies within each accepted layout | Shared aligned-site constructor after provider-owned fitting; requirements begin essential, weight one | Declared pivot/proposals/layouts; every accepted proposal placement is retained, including geometrically equivalent alternatives |

The minimum support count and minimum number of emitted sites ask different
questions. A site's support is marginal; a hypothesis's joint support is the
intersection of its site members. The reference method can combine sites with
different supporter populations into one hypothesis. It is not erroneous for
that model to have fewer jointly supporting ligands than `min_support`.
Switching to joint filtering would change its declared scientific method.

Support is discovered correspondence, not guaranteed acceptance of emitted
geometry: radius is independent of discovery tolerance, orientation is an
explicit reference choice, and curated constraints may reject contributors.
No support fraction is a binding probability. All defaults remain editable.

## Analytical cross-method comparison

The fixed charge cohort uses real public MolSysMT conversion/recognition with
analytical coordinates. A has Na+ at 0 and Cl- at 0.3 nm, B has Na+ at 0, and C
has Cl- at 0.3 nm. These disconnected atom fixtures define a logical/geometric
control, not optimized conformers, experimental ligands or independent activities.

| Declared input | Positive site supporters | Negative site supporters |
| --- | --- | --- |
| A, B, C | A, B | A, C |

At support two, the reference method emits both sites as one hypothesis. Their
common supporter set is **A**, so evaluating A/B/C gives matched/not_matched/
not_matched with the chosen 0.02 nm radius. The clique method emits two separate
one-site hypotheses, supported by AB and AC respectively. Their matched inputs
are exactly AB and AC for this deliberately coincident fixture. This measured
difference reflects method choice, not solver disagreement.

At support three, neither original site qualifies. Reference construction raises
its established no-supported-site error; clique discovery completes with no
models. Repeating the known prepared B source as a second entry named B-repeat
makes the positive site attain support 3/4 in both methods. The positive site
still has weight one and is initially essential. A new string label does not
make a repeated molecular source independent evidence.

A separate two-source positive-site control places A at 0 and B at 0.06 nm.
The site mean is 0.03 nm. Repeating B moves it to **0.04 nm**, with count three
and unchanged site weight. This distinguishes input multiplicity in aggregation
from an explicit pharmacophore weight. It does not estimate chemical-series bias
or validate a data-balancing rule.

## Identity, occurrence and population

- A unique declared `ligand_id` contributes at most once to a site. Identical ID
  strings are refused by existing argument contracts. The library does not
  authenticate chemical uniqueness from labels, object identity or atom counts.
- An occurrence is `(inventory index, feature index)`. The same occurrence cannot
  appear in two sites of one hypothesis. Distinct typed roles may share atoms;
  a donor–H record and an acceptor record can both contain the donor heavy atom.
- Overlapping alternative hypotheses may reuse occurrences across models. Rigid
  placements and resulting model counts retain proposal multiplicity. Neither
  model count nor summed site support counts independent evidence.
- All declared inputs remain in support denominators, including empty feature
  inventories and, in rigid consensus, sources without a direct pivot placement.
  Absence of a correspondence is not a measured inactive label.
- Distinct conformers/states are prepared input choices, not automatic extra
  independent ligands. This interface takes one declared prepared frame per ID.

Chemical identity, source comparison, duplicate detection, conformer/state
preparation and general molecular grouping belong to MolSysMT. Experimental
endpoint eligibility, series balancing and data splits belong to the study
protocol. This review deliberately repeats a **known** source; it implements no
molecular equivalence test, scaffold classifier or automatic cohort reweighting.

## Evidence-to-constraint decisions

Each site retains member IDs, inventory/feature/atom/frame/state indices,
source geometry, support count/fraction and dispersion. Original source
inventories retain their molecular-provider recognition. Clique/rigid models
also retain the selected hypothesis and joint supporter IDs/count/fraction;
rigid models retain pivot, proposal family, placements/layout and finite budgets.
Reference models retain the per-site populations, not a fabricated joint
threshold. Native JSON/YAML preserve these differences and the initial
essential/unit-weight choices under changed unit policies.

The new shared-role control constructs four typed features at three centers
from `[2H]O.C=O.[Na+]`: a donor and acceptor share O atom 1. All three methods
retain unique feature occurrences, both roles, support two and weight one.
Molecular coordinates remain unchanged. The result is an analytical assertion
about pharmacophore representation; simultaneous physical receptor contacts
need a separate scientific argument.

Use existing [curation](pharmacophore_curation_workflow.md) for a recoverable change history.
Frequency does not automatically make a site essential or increase its weight.
Neither construction nor preserved provenance supplies a causal binding claim.

## Independent controls and limits

| Mechanism | Existing independent or analytical guard retained |
| --- | --- |
| Maximum-cardinality/minimum-distance assignment | `tests/test_aligned_consensus.py::test_assignment_matches_bounded_exhaustive_oracle_with_repeated_types` enumerates injections independently of SciPy |
| Maximal feature cliques | `tests/test_aligned_cliques.py::test_cliques_match_independent_subset_oracle` enumerates subsets independently of NetworkX/production helpers |
| Joint support and occurrence-disjoint packages | `tests/test_aligned_cliques.py::test_hypothesis_packages_match_bounded_subset_oracle` and the explicit triple-intersection control |
| Rigid correspondence | `tests/test_rigid_consensus.py::test_association_graph_matches_independent_injective_mapping_oracle` enumerates bounded injective permutations |
| Alignment objectives and frozen strategy expectations | `tests/test_rigid_strategy_comparison.py` distinguishes minimum RMSD from tolerance-valid coverage and preserves declared case outcomes |
| Equivalent proposal multiplicity and resource limits | Existing symmetric-mapping, empty/unplaced, budget, failure and report-summary controls in rigid/modular tests |
| Prepared distinct ligands and complete persisted maps | `tests/test_prepared_consensus_workflow.py` retains the existing frozen prepared molecular inputs and denominators |

The new [cross-method controls](../tests/test_consensus_support_review.py) add
uncovered comparisons and controlled multiplicity effects, not copies of these
oracles. The [receipt/full original evidence](evidence/consensus_support_review_20261104_summary.json)
retains all attempts, exact sources/inputs, native identities, commands, actual
results and model persistence outputs. Source qualification with controlled
scientific dependencies is separate from clean installed/public/all-platform,
full-suite, biological predictive or performance qualification.

Audit 8–9/13 remains partial: this does not show robustness to real chemical-series
imbalance, justify constraint importance or compare predictive model complexity.
Those depend on prespecified development eligibility/groups, independent labels,
MolSysMT-backed molecular preparation and a held-out evaluation design. #66's
original-method access gate remains. Next define a bounded development-only
sensitivity protocol for radius, matching tolerances and explicit constraint
ablations, starting with analytical controls and keeping final evaluation data
unused. Do not silently tune the reserved holdout or increase search opportunities
without recording them.

No molecular/runtime/provider/prefix/dependency or scientific-definition changes.
SDF ownership migration #74/MolSysMT #215, broader #6, installed/public/hosted
qualification, addon and new release retain their separate scope. Public release
remains 0.4.0.

## Executed checkpoint — 2026-11-04

126 selected cases pass in 160.40 s, including 28 new cross-method cases.
The original charge-cohort probe and the selected run each preserve complete
source/native/test/input/metadata identity. Existing independent oracles remain
unchanged. No runtime/helper/input/provider/dependency source changes.
This is the tested source scope, not a new full-suite/installed/public/hosted claim.

Owned capsule: `/tmp/phmt-consensus-review-20261104-vd1h3_79`, LMMV/dprada, review
2026-11-18. Keep original outputs for follow-up; borrowed scientific and public
ArgDigest prefixes are unchanged. No continuing local process is required.
