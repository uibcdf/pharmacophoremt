# Compose exclusion spheres with a pharmacophoric query

`get_excluded_volume_sites()` is an independent builder from cached heavy-atom
geometry. MolSysMT supplies molecular coordinates, selections and elements;
PharmacophoreMT chooses Feature + Shape constraints. The caller explicitly picks
the radius and guarantees that exclusions and positive sites share a frame.

The first example is analytical geometry, not an optimized receptor complex.
A uniform exclusion radius is a modeling choice, not a physical atomic radius
or a pairwise van der Waals overlap model.

## Extract geometry, build sites and evaluate

```python
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import (
    from_ligand, get_features, get_excluded_volume_sites,
)
from pharmacophoremt.screening import PoseEvaluator

ligand = msm.convert(msm.convert('smiles:CCC', to_form='rdkit.Mol'),
                     to_form='molsysmt.MolSys')
ligand.structures.append(coordinates=puw.quantity(
    [[[0,0,0], [.15,0,0], [.30,0,0]]], 'nm'))
receptor = msm.convert(msm.convert('smiles:[He]', to_form='rdkit.Mol'),
                       to_form='molsysmt.MolSys')
receptor.structures.append(coordinates=puw.quantity([[[0,0,0]]], 'nm'))
inventory = get_features(receptor, features=['included volume'])
excluded = get_excluded_volume_sites(inventory, radius='0.10 nm')
query = from_ligand(ligand, features=['hydrophobicity'], radius='0.5 nm')
for site in excluded['interaction_sites']:
    query.add_interaction_site(site)
evaluator = PoseEvaluator(query)
results = {}
for displacement in (0.09, 0.10, 0.11):
    candidate = msm.structure.translate(
        ligand, translation=puw.quantity([[[displacement,0,0]]], 'nm'), in_place=False)
    results[displacement] = evaluator.evaluate(candidate)
assert all(result['fit_value'] == 1 for result in results.values())
assert results[0.09]['status'] == 'not_matched'
assert results[0.10]['status'] == results[0.11]['status'] == 'matched'
```

Heavy-atom centers **strictly inside** an exclusion veto the candidate. A center
on the boundary is permitted. Exclusions have zero positive-fit weight; this is
why the penetrated pose has fit 1 yet fails. Essential/optional flags do not
soften the exclusion veto. A query needs positive sites as well as exclusions.

Inventories must contain singleton `included volume` records; chemical/grouped,
oriented and duplicate records are rejected. Empty declared feature lists return
no exclusions, without proving that the molecular source has no heavy atoms.
Uniform scalar radii require explicit units. Source identities and common frame
remain caller declarations; no imaging or reference-ligand pruning occurs.

## Reuse the inventory and retain construction credits

```python
import json
import ackredit

with ackredit.session('cached exclusion construction'), phmt.attribution(True):
    with ackredit.capture('construction from existing geometry') as capture:
        rebuilt = get_excluded_volume_sites(inventory, radius='1 angstrom')
assert rebuilt['report']['n_sites'] == 1
assert rebuilt['attribution']['status'] == 'captured'
assert not any(
    use['context'].get('software') == 'molsysmt'
    for use in rebuilt['attribution']['references']['uses']
)
saved = json.dumps({
    'report': rebuilt['report'], 'attribution': capture.attribution.to_dict(),
}, allow_nan=False)
bibliography = ackredit.Attribution.from_dict(
    json.loads(saved)['attribution']
).report(format='bibtex')
assert bibliography
```

Cached construction reads no molecular data. Its credits cover executed host,
array and unit software; earlier inventory attribution is retained in the source
report, without crediting another extraction. No named third-party exclusion
algorithm or physical-radius table is claimed. Real chemistry methods reached by
other workflow stages retain their own citations.

Site geometry/metadata and the detached report are independently owned. Add the
report and portable attribution to query metadata or save them beside native
query JSON. Report site indices are local to the returned list; after composition
global query indices differ. Clash atom indices refer to the evaluated candidate,
while site metadata retains the original receptor atom indices.

## Continue with observed receptor geometry

From this source checkout, the observed 1QKU continuation composes the previous
[EST preparation](observed_est_hydrogens.md) with the
[receptor geometric scope](observed_receptor_coverage.md):

```python
from tempfile import TemporaryDirectory
from devtools.prepare_eralpha_ligand import credit_inputs
from devtools.validate_eralpha_exclusions import workflow, valid
from devtools.validate_eralpha_template import portable

with ackredit.session('observed receptor exclusion controls'), phmt.attribution(True):
    with ackredit.capture('ligand preparation and receptor geometry') as capture:
        with TemporaryDirectory() as directory:
            observed = portable(workflow(directory))
        credit_inputs()
assert valid(observed)
assert observed['construction']['report']['n_sites'] == 153
assert observed['outcomes']['reference']['status'] == 'matched'
assert observed['outcomes']['collision']['status'] == 'not_matched'
assert observed['outcomes']['collision']['fit_value'] == 1
assert observed['query_metadata_preserved']
assert observed['source_unchanged'] and observed['ligand_unchanged']
assert len([i for i in capture.attribution.to_dict()['items'] if i['type']=='dataset']) == 3
```

The 19 whole residues within 0.5 nm of observed EST supply 153 heavy-atom centers.
At the explicitly chosen 0.1 nm exclusion radius the unchanged reference passes.
A controlled ligand translation superposes O3 onto GLU353 OE2; the candidate
retains all five positive matches but is vetoed by one exclusion. The broad
0.4 nm positive-site radius isolates this effect and is an analytical control.
It does not replace the earlier 0.02 nm recovery hypothesis.

At 0.35 nm exclusion radius, the unchanged reference is vetoed by 12 atom/site
clashes. This shows sensitivity to radius choice; neither choice is a validated
physical cutoff. Both remain available. Native query JSON retains metadata and
the reference/collision outcomes. Receptor chemistry remains unprepared and no
interaction detector runs. Generated ligand H are local geometry, not observed
or receptor-optimized orientations. These controls establish no affinity or
biological enrichment.

Run the complete evidence driver:

```bash
python -m devtools.validate_eralpha_exclusions --output /tmp/est-exclusions.json
```

The tool is tracked in [#32](https://github.com/uibcdf/pharmacophoremt/issues/32),
the observed case in [#22](https://github.com/uibcdf/pharmacophoremt/issues/22).
Molecular chemical preparation remains with
[MolSysMT #298](https://github.com/uibcdf/molsysmt/issues/298).
