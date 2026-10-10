# Carry a prepared hypothesis through curation, saving and screening

This source-checkout recipe uses the public frozen CCD EST fixture. Its ideal
coordinates provide workflow controls, not an experimental binding pose or
activity labels. MolSysMT owns molecular preparation and translations;
PharmacophoreMT owns the declared query and its constraints.

## Construct and curate independently

```python
from devtools.prepared_ccd_ligands import prepare_case
from pharmacophoremt.modeler import (
    from_feature_inventory, extract_pharmacophore, edit_pharmacophore,
    get_interaction_site_indices,
)

prepared = prepare_case('EST', features=['hydrophobicity', 'aromatic ring'])
source = prepared['molecular_system']
original = from_feature_inventory(prepared['inventory'], radius='.02 nm')
rings = get_interaction_site_indices(original, feature_names='aromatic ring')
hydrophobic = get_interaction_site_indices(original, feature_names='hydrophobicity')
assert len(rings) == 1 and len(hydrophobic) == 9
selected = extract_pharmacophore(original, site_indices=rings + hydrophobic)
optional = edit_pharmacophore(selected, site_indices=range(1, 10), essential=False)
narrow = edit_pharmacophore(optional, site_indices=0, weight=3)
wide = edit_pharmacophore(narrow, site_indices=0, radius='.1 nm')
assert wide.score is None and narrow.interaction_sites[0].essential
```

The ring is mandatory and contributes weight three; nine hydrophobic sites are
optional with weight one. The alternative changes only ring radius. These choices
must precede evaluation and are retained in curation history. They are not learned
from activity labels. No hydrogen-bond direction operations are requested.

## Persist the query, then screen declared placements

```python
import molsysmt as msm
from pathlib import Path
from tempfile import TemporaryDirectory
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.io import to_sdf, load_sdf
from pharmacophoremt.screening import VirtualScreening

near = msm.structure.translate(source, translation='[0,0,.05] nm', in_place=False)
far = msm.structure.translate(source, translation='[0,0,2] nm', in_place=False)
unprepared = msm.convert(
    msm.convert('smiles:CCC', to_form='rdkit.Mol'), to_form='molsysmt.MolSys')
with TemporaryDirectory() as directory:
    path = Path(directory) / 'hypothesis.sdf'
    with puw.context(standard_units=['pm', 'fs', 'degrees']):
        to_sdf(wide, path)
    with puw.context(standard_units=['angstrom', 'ps', 'radians']):
        restored = load_sdf(path)
        screen = VirtualScreening(restored, screening_method='placed', min_fit_value=.2)
        hits = screen.run([near, source, far, unprepared, source], on_error='record')
assert [hit['input_index'] for hit in hits] == [1, 4, 0]
assert [row['status'] for row in screen.evaluations] == [
    'matched', 'matched', 'not_matched', 'failed', 'matched']
assert [row['fit_value'] for row in screen.evaluations] == [.25, 1., 0., None, 1.]
assert hits[0]['mol'] is source and hits[1]['mol'] is source
```

The small displacement leaves only the wide aromatic constraint matched, giving
coverage `3/(3+9)`. The original pose scores one. The far placement scores zero;
the unprepared molecule fails and has no score. Tied hits retain input order.
Repeating the original reference tests ties, not independent molecular support.
Placed screening performs no alignment: the far placement could be recoverable
under a separately chosen rigid-search method.

This SDF stores virtual pharmacophore sites with the versioned native model
payload. Exporting molecular hits is a separate MolSysMT workflow. Use
`screen.to_dataframe()`/`to_csv()` for ranked scalar hits and `evaluations` for
the complete input/failure denominator.

## Inspect the complete qualification

```bash
python -m devtools.prepared_workflow --output /tmp/prepared-workflow.json
python -m pytest -q tests/test_prepared_workflow.py
```

The opt-in driver checks narrow/wide hypotheses and an independent steric veto,
all three codecs, fresh readers, two unit policies, source immutability and actual
attribution on/off. The [validation case](../validation/prepared_workflow.md)
links original outputs and limits. This demonstrates a prepared chain available
while MolSysMT #375 remains pending; it does not establish biological prediction.
