# Build consensus from prepared aligned ligands

Use `modeler.from_aligned_ligands()` when your prepared ligands already share
a common coordinate frame. The current method anchors the model in the chemical
features of one declared reference ligand, finds one-to-one correspondences in
the other ligands and aggregates sufficiently supported sites.

This is a development API. Provider revisions and distribution limits are the
same as the other native cookbook recipes. The example is an analytical control,
not a biological validation or a performance benchmark.

## Executable example

The fixtures below represent two slightly different placements of propane in
one frame and a sodium ion with no hydrophobic feature. Coordinates and chemistry
are supplied through MolSysMT; replace these fixtures with your prepared inputs.

```python
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw

def prepared(smiles, coordinates):
    source = msm.convert(
        msm.convert('smiles:' + smiles, to_form='rdkit.Mol'),
        to_form='molsysmt.MolSys',
    )
    source.structures.append(coordinates=puw.quantity([coordinates], 'nm'))
    return source

first = prepared('CCC', [[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]])
second = msm.structure.translate(
    first, translation=puw.quantity([[[0.04, 0, 0]]], 'nm'), in_place=False,
)
negative = prepared('[Na+]', [[2, 0, 0]])

with phmt.attribution():
    query = phmt.modeler.from_aligned_ligands(
        [
            {'ligand_id': 'reference', 'molecular_system': first},
            {'ligand_id': 'second', 'molecular_system': second},
            {'ligand_id': 'negative', 'molecular_system': negative},
        ],
        features=['hydrophobicity'], min_support=2,
        distance_tolerance='0.10 nm', radius='0.06 nm',
        name='Aligned hydrophobic consensus',
    )

assert query.n_interaction_sites == 1
site = query.interaction_sites[0]
assert site.metadata['support_count'] == 2
assert site.metadata['support_fraction'] == 2 / 3
assert abs(float(puw.get_value(site.center, to_unit='nm')[0]) - 0.17) < 1e-12
assert abs(float(puw.get_value(
    puw.QuantityRecord.from_dict(site.metadata['position_rmsd']).to_quantity(),
    to_unit='nm')) - 0.02) < 1e-12

evaluator = phmt.screening.PoseEvaluator(query)
assert evaluator.evaluate(first)['status'] == 'matched'
assert evaluator.evaluate(second)['status'] == 'matched'
assert evaluator.evaluate(negative)['status'] == 'not_matched'
```

Every input has a unique declared `ligand_id`. An input record may additionally
declare its own MolSysMT `selection`, `structure_index` and `chemical_state`;
the defaults are `'all'`, `0` and `'reference'`. Input coordinates are neither
aligned nor altered. A single ligand supplies one prepared frame; do not count
its conformers as separate ligands. Dataset duplicate/chemical-equivalence
curation remains an explicit input responsibility.

## Matching, aggregation and interpretation

`reference_index` selects the source that anchors the model. Each reference
feature defines one possible consensus site. Other ligands contribute at most
one compatible occurrence to that site; an occurrence cannot fill two sites.
Matching maximizes the number of valid typed correspondences, then minimizes
total center distance. This avoids a nearest-first greedy choice that can lose
valid matches. Equal optima retain a deterministic input-order choice.

`distance_tolerance` bounds the reference/candidate center distance during
matching and the member deviation from the final mean during aggregation.
`direction_tolerance` bounds directed donor-H vectors or unoriented aromatic
axes relative to the reference. A reversed donor vector differs; reversed
aromatic normals describe the same axis. Directions are retained from the
reference member and recorded as such; no angular averaging is implied.

Centers are unweighted means of **pharmacophoric feature centers**. Metadata
retains each supporting ligand, inventory/feature/atom indices, frame, declared
chemical state, member geometry, support fraction, positional RMSD and maximum
position/orientation deviation. Ligands with no matching features still count
in the support denominator. Unsupported or geometrically inconsistent groups
are recorded in `query.metadata['consensus']['rejected_groups']`.

Emitted `radius` is an independent model choice. A smaller curated radius may
reject a ligand that contributed to the correspondence group; support is not a
promise of final query acceptance or affinity. Sites start essential with unit
weight. Curate these choices before constructing an evaluator. Frequency alone
does not establish a binding requirement.

## Reuse the intermediate tools

`get_aligned_feature_matches()` works directly on two native `get_features()`
inventories. `get_consensus_sites()` can aggregate explicit correspondence groups
from a different discovery method, without requiring molecular input or choosing
the emitted shape radii. A group lists `[inventory_index, feature_index]` pairs.

```python
inventories = [phmt.modeler.get_features(source, features=['hydrophobicity'])
               for source in (first, second, negative)]
matches = phmt.modeler.get_aligned_feature_matches(
    inventories[0], inventories[1], distance_tolerance='0.10 nm',
)
assert matches['matches'] == [[0, 0]] and matches['complete']
consensus = phmt.modeler.get_consensus_sites(
    inventories, [[[0, 0], [1, 0]]],
    ligand_ids=['reference', 'second', 'negative'], min_support=2,
    distance_tolerance='0.10 nm',
)
assert consensus['sites'][0]['support_count'] == 2
```

The aggregation tool returns complete evaluated-empty evidence when no group
qualifies. Model construction raises if there is no usable site. The assignment
matrix is bounded by `max_matrix_entries`, including dummy columns: exceeding
the bound raises PHMT-E106 before allocation, and is not reported as a negative.

This reference-anchored method does not discover patterns absent from the chosen
reference, enumerate alternative equal assignments or optimize a joint
multi-ligand mapping after aggregation. Use the separate
[aligned-clique recipe](aligned_cliques.md) for reference-independent maximal
site discovery and alternative jointly supported hypotheses. Native JSON/YAML preserves its metadata,
and [optional attribution](attribution.md) records reached software/method
references without crediting those future methods as executed.
