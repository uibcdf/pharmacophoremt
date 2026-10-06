# Native aligned-ligand consensus

Local implementation owned by
[issue #21](https://github.com/uibcdf/pharmacophoremt/issues/21), following the
[clique/literature review](clique_consensus_review.md). Method identifier:
`aligned_reference_consensus@1`, using `classical_atomic_formal@1` recognition.

## Public tool boundaries

- `get_aligned_feature_matches(reference_inventory, feature_inventory, ...)`
  performs typed, position/orientation-compatible injective assignment, maximizing
  cardinality before minimizing total center distance. Explicit empty inputs
  complete successfully. Dummy-inclusive matrix size is checked before allocation.
- `get_consensus_sites(feature_inventories, correspondence_groups, ligand_ids=...)`
  validates occurrence/identity mappings, aggregates explicit feature-center
  populations and returns supported sites plus rejected-group evidence.
- `from_aligned_ligands(ligands, ...)` calls both tools after obtaining each
  source's native inventory through public MolSysMT-supported `get_features()`.
  It builds editable Feature + Shape sites and attaches portable provenance.

These operations belong in PharmacophoreMT: their objects and rules concern
pharmacophoric correspondences and hypotheses. All molecular access, recognition,
selected frame/state geometry and transformations remain with MolSysMT.
The arithmetic mean and residuals aggregate pharmacophoric site populations,
not molecular coordinate arrays or a replacement molecular center provider.

Existing rigid-triplet correspondences propose alignments, not fixed-frame
full-inventory assignments; the new matching tool does not repurpose that contract.
SciPy supplies generic assignment. The existing public feature/pose tools and
native codecs are reused rather than introducing new chemistry or molecular forms.

## Scientific contract

One declared unique ligand identity contributes one prepared frame. Input records
carry independent selection/frame/state choices. A group has one common chemical
kind, at most one feature per ligand, and no reused occurrence in another group
of the same hypothesis. Ligands without features count in the support denominator.
Dataset chemical equivalence is not inferred from objects or atom counts.

Features in the selected reference anchor discovery. Matching uses absolute
centers in the declared common frame and handles directed donor vectors and
unoriented aromatic axes. Site centers are unweighted feature means. Retain the
first member's explicit orientation and verify deviations; do not add a generic
angular-mean implementation to the consumer. Searches of MolSysMT's current
public structural tools found no direct mean-orientation operation, but this
method requires no such provider capability and makes no averaging claim.

Final center/reference-orientation consistency is checked separately from
pairwise assignment, and rejected groups retain their members and reason.
Reference/candidate matching and mean-center acceptance currently share the
declared distance tolerance; the emitted model radius remains independent.
The first method does not reassign occurrences after a group is rejected.

Support is correspondence frequency, not affinity or a causal binding requirement.
Sites begin essential with weight 1; hypothesis curation remains explicit.
No score is fabricated from support. A smaller emitted radius can exclude a
supporting placement. Missing patterns, alternative mappings and joint global
optimization remain outside this reference-anchored method's completeness scope.

## Completion, provenance and attribution

The standalone matching/aggregation tools return complete evaluated-empty
results. No usable site makes model construction raise PHMT-E102. Exceeding
`max_matrix_entries` raises PHMT-E106 before assignment allocation; there is
no silent truncation, fallback solver or negative result. The matrix bound is
per comparison, not a guarantee on total molecular input/provenance memory.

Source inventories retain recognition, selected atom indices, frames/states and
native feature geometry. Sites retain member identities/indices/geometry and
unit-bearing dispersion. Native metadata uses QuantityRecord sealing and the
existing JSON/YAML model codec. Ackredit captures actual reached NumPy/PyUW/MSM
software and the SciPy assignment implementation/description; future clique
papers are not runtime declarations. The known cross-provider warning limitation
in MolSysMT #295 remains separate.

## Verification and limits

`tests/test_aligned_consensus.py` compares assignment against exhaustive injection
enumeration with a fixed-seed bounded fixture, checks a greedy counterexample,
reordered types, analytical centroids/support/dispersion, rejected/empty groups,
opposed donor vectors and equivalent normal signs, duplicate identities/occurrences,
invalid geometry/units and assignment budget. Real molecular controls use public
MolSysMT tools, preserve source coordinates, exercise independent frames/selections,
aromatic planes, nondefault unit policy, Ackredit and native JSON persistence.

Controlled source providers remain the documented MolSysMT
`4d490427e38c5836be82472348fdf61934442bda`, PyUnitWizard
`2ffe1885675f47c76af03c08e51bc889a5e99a05` and Ackredit
`584328de6efc07cee3a5ddf3ecda2d2e08cc72b4`, with existing suite dependencies.
This is analytical local evidence, not biological pilot validation, performance
benchmarking, stable installation or hosted supported-matrix coverage.

The [cookbook recipe](../docs/content/cookbook/aligned_consensus.md) demonstrates
construction/evaluation and reuse of the intermediate tools. The separate
[aligned-clique method](aligned_clique_consensus_workflow.md) now reuses aggregation
for reference-independent discovery and alternative jointly supported hypotheses.
Unaligned discovery,
complete native complex consensus, aggregate angular statistics and a replacement
for legacy RDP/clique modeling remain subsequent work. Generic molecular/angular
provider gaps require linked consumer evidence, not copied kernels.
