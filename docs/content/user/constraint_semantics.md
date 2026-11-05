# Interpret pharmacophore constraints

A native Point or Sphere site with several features accepts **any one** of
them. For example, `["positive charge", "negative charge"]` allows either
charge kind within that site's positional tolerance. It remains one site with
one assignment and one weight. Requiring separate sites expresses separate
constraints, and every essential site must match, even when its weight is zero.

Assignments consume recognized feature records. One record cannot satisfy two
sites, but different chemical roles can share atoms. An oxygen's donor and
acceptor records are distinct, as are two donor–H pairs sharing a donor atom.
This method allows those records to fill separate sites; a geometric match
does not establish that simultaneous receptor contacts are physically feasible.

Directed sites require a donor-H feature. Aromatic disks require an aromatic-ring
feature and compare center distance and the unoriented plane normal. Excluded
volumes are separate spheres: a selected heavy-atom center strictly inside one
vetoes the pose. These shapes cannot combine arbitrary feature alternatives.

Inclusive positive-site distance comparisons allow a relative margin of eight
float64 epsilons to preserve equality through ordinary unit-conversion roundoff.
Results expose it as `position_comparison_relative_slack`; it does not replace
the declared radius or Point tolerance. Exclusion boundaries remain strict.
The [receptor sensitivity controls](../validation/receptor_sensitivity.md)
illustrate these separate roles.

`fit_value` is the fraction of matched non-exclusion weight. Essential sites,
exclusions and the chosen minimum coverage also determine `status`; high
coverage alone does not imply an accepted pose. Results record
`site_feature_logic="any_of"` and `assignment_unit="typed_feature_record"`
alongside the one-to-one and essential-site criteria. Coverage does not estimate
affinity, binding probability or confidence.

Queries from recognized ligand features, observed contacts and explicit receptor
projections begin with essential sites of weight one. These are editable
hypothesis choices, not measurements of binding importance. Multiple contacts
for the same typed participant retain multiple observations without increasing
its weight automatically. Reference features, detector observations and caller
projections keep their distinct provenance.

Use [model curation](../cookbook/pharmacophore_curation.md) to change weights,
essential flags or radii with a recorded reason and source-model snapshot.
JSON/YAML retain those choices and their history. Direct attribute edits do not
automatically record a reason. Choose these decisions before constructing the
evaluator, which snapshots the query. Compare scientific alternatives explicitly;
the software does not infer which constraints cause binding.

Follow the [reference-ligand recipe](../cookbook/reference_ligand.md) or the
[observed-complex recipe](../cookbook/complex_based_modeler.md) for the input
workflow. Molecular preparation, chemical recognition, selections, coordinates
and transformations are provided by MolSysMT.
