# Model with traceable prepared CCD ligands

Run this recipe from the source checkout in the compatible development environment.
The retained fixtures are the official [CCD ideal SDFs](https://www.rcsb.org/docs/programmatic-access/file-download-services)
for [estradiol (EST)](https://www.rcsb.org/ligand/EST) and
[diethylstilbestrol (DES)](https://www.rcsb.org/ligand/DES). Their ideal coordinates
are reference geometry; this recipe does not validate experimental binding poses,
affinity or conformer energies.

MolSysMT reads the explicit chemistry/hydrogens, interprets source stereo and
performs the declared RDKit sanitizing roundtrip for aromatic metadata. The
fixture loader checks source bytes and retains an audit. Original SD properties
remain in the unmodified SDFs. No atoms, hydrogens or conformations are generated.

```python
from devtools.prepared_ccd_ligands import prepare_case, motion_frames, credit_source

prepared = {name: prepare_case(name) for name in ('EST', 'DES')}
assert prepared['EST']['report']['prepared_counts']['n_atoms'] == 44
assert prepared['DES']['report']['prepared_counts']['n_atoms'] == 40
for item in prepared.values():
    audit = item['report']
    assert audit['source_atom_ids'] == audit['prepared_atom_ids']
    assert audit['source_bytes_unchanged'] and audit['source_state_unchanged']
    assert audit['coordinate_rmsd_nm'] < 1e-12
```

Build a selected-feature inventory, propose one ranked noncollinear seed and
refine it with the independent public tool. Frame zero is the ideal reference;
frame one is a rotated/translated copy of the same conformation. The source
remains unchanged. A bounded application Ackredit session records the input and
every executed stage, including preparation before the refinement call.

```python
import ackredit
import pharmacophoremt as phmt
from pharmacophoremt.modeler import get_features
from pharmacophoremt.screening import (
    get_rigid_feature_correspondences,
    refine_rigid_feature_correspondences,
    evaluate_feature_correspondence,
)

features = ['hb donor', 'hb acceptor', 'aromatic ring']
with ackredit.session('CCD self recovery'), phmt.attribution():
    item = prepare_case('EST')
    credit_source('EST')
    frames = motion_frames(item['molecular_system'])
    target = get_features(frames, structure_index=0, features=features)
    source = get_features(frames, structure_index=1, features=features)
    seeds = get_rigid_feature_correspondences(
        target, source, correspondence_strategy='ranked_triplet_seeds',
        n_seeds=1, distance_tolerance='.02 nm',
    )
    refined = refine_rigid_feature_correspondences(
        frames, target, seeds['correspondences'], features=features,
        feature_inventory=source, structure_index=1, orientation_policy='final',
        min_matches=5, distance_tolerance='.02 nm', direction_tolerance='20 degrees',
    )
    placement = refined['placements'][0]
    geometry = evaluate_feature_correspondence(
        target, placement['inventory'], placement['matches']['matches'],
        distance_tolerance='.02 nm', direction_tolerance='20 degrees',
    )
    assert geometry['all_pairs_valid']
    assert refined['report']['n_fits'] == 3
    self_references = ackredit.get_attribution().to_dict()
```

Both angular policies recover all five selected EST features and all six DES
features in these self controls. Atomic hydrophobic participants are recognized
in the preparation audit but excluded from this selected-feature search.

Now build a reference-anchored consensus between the two prepared ligands. Here
the hypothesis includes acceptors and aromatic rings, with three shared sites
required. Changing selected families changes the scientific question.

```python
from pharmacophoremt.modeler import from_rigid_ligands
from pharmacophoremt.validation import summarize_rigid_consensus

with ackredit.session('CCD cross-ligand consensus'), phmt.attribution():
    pair = {name: prepare_case(name) for name in ('EST', 'DES')}
    for name in pair:
        credit_source(name)
    consensus = from_rigid_ligands(
        [{'ligand_id': name, 'molecular_system': item['molecular_system']}
         for name, item in pair.items()],
        features=['hb acceptor', 'aromatic ring'],
        correspondence_strategy='ranked_triplet_seeds', n_seeds=4,
        refinement_strategy='greedy', orientation_policy='each_step',
        min_matches=3, min_sites=3, distance_tolerance='.20 nm',
        direction_tolerance='30 degrees', max_fits=100,
    )
    summary = summarize_rigid_consensus(consensus['report'])
    assert summary['n_models'] == 1 and summary['max_joint_sites'] == 3
    assert summary['n_fits'] == 2
    references = ackredit.get_attribution().to_dict()
```

Render the saved whole-workflow bibliography after leaving its session. Input
data references and their CCD description remain separate from G3PS, provider
fitting and executed software. Individual function captures have smaller scope
than this application-owned session.

```python
bibliography = ackredit.Attribution.from_dict(references).report(format='bibtex')
assert '10.1093/bioinformatics/btu789' in bibliography
assert '10.3390/molecules26237201' in bibliography
assert any(item['type'] == 'dataset' for item in references['items'])
```

For the same selected seed limit and .20 nm distance tolerance, including donors
with a 30-degree angular tolerance yields no common model under either policy.
Relaxing that angle to 90 degrees yields four/final or two/each_step alternatives,
with four joint sites. These observations do not establish activity, distinct
binding modes or a superior strategy. Removing donors or relaxing constraints
defines another hypothesis; an empty bounded search does not prove inactivity.

The source contract `devguide/prepared_ccd_validation.md` records preparation,
frame screening, counts, parameters and evidence limits. Reproduce all controls
with `python -m devtools.validate_prepared_ccd_ligands --output /tmp/ccd-validation.json`.
That driver compares scientific fields with and without tracking and retains full
citations; it takes no timing measurements. The experimental ERalpha preparation
gate remains open in the [input-audit recipe](eralpha_input_audit.ipynb).
