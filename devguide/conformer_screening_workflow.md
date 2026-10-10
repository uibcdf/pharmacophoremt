# Screening prepared conformations

The #45 [screening facade transition](virtual_screening_workflow.md) now reuses
this tool through `VirtualScreening(screening_method='conformers')`. It adds a
ranked hit-list surface without changing this tool's ensemble/search contract.
Retrospective evaluation requires an explicit evaluator; legacy preparation is retired.

`screening.ConformerScreening`, tracked in `uibcdf/pharmacophoremt#17`, searches
prepared frames through the existing [rigid-search tools](rigid_search_workflow.md).
MolSysMT supplies frame indices, declared chemical states, coordinate access and
molecular alignment. PharmacophoreMT owns pharmacophoric interpretation and the
choice among checked poses. This workflow does not generate conformers or states.

## Input and result contract

One database entry is one molecular system with stable source atom identity and
prepared coordinate frames. `structure_indices='all'` searches all frames;
an explicit nonempty sequence of unique nonnegative indices preserves requested
order. MolSysMT validates frame bounds. `selection` applies to each frame through
MolSysMT. Empty selections and systems without coordinates are failures.

`chemical_state='reference'` uses the provider's declared reference state;
an integer selects that declared state for every frame. `'structure'` resolves
each frame's associated state independently. No states are inferred or enumerated,
and missing associations fail explicitly. Different atom inventories belong in
separate molecular systems. Default reference selection does not mean automatic
frame-associated selection.

All requested frames are attempted. The best valid hit ranks ahead of any
negative, then weighted coverage determines rank within each status. Exact ties
retain the first requested frame; RMSD does not break ties. Each conformer retains
`conformer_index` equal to its source `structure_index`, requested
`chemical_state`, resolved state index, recognition and search evidence. Successful
frames retain assignments, alignment and sealed `pose_coordinates` of shape
`(1, n_selected_atoms, 3)` ordered by `selected_atom_indices`. Alignment can be
`None` when the original placement wins; coordinates are still present.

The aggregate copies the best pose fields and names `best_conformer_index`.
`conformers` contains every requested frame in order. `ensemble` records requested,
evaluated and failed counts, completeness, score resolution and ranking policy.
In batches, `pose_id` and `input_index` identify the molecule by input position;
frame identity is local to that molecule. Generators and repeated objects retain
separate input identities. Results are detached and JSON portable; source systems
remain unchanged.

## Failed frames and retrospective metrics

`on_error='raise'` aborts on the first failure. Explicit `on_error='record'` retains
causes, diagnostic codes and stages, then continues through the remaining frames.
Source/frame-list errors are molecule-level failures in batch recording.

When any frame fails, a best observed pose with coverage below one leaves the
molecule's definitive score unresolved. The aggregate has `status='failed'`,
`fit_value=None`, `best_conformer_index=None` and `best_observed` for inspection.
If every frame fails, `best_observed=None`. Neither case becomes a scientific
negative or a partial score in ranking metrics.

A valid hit with coverage one proves maximal coverage even when other frames fail.
Its score remains usable, while `ensemble.complete=False` and the per-frame
failures remain visible. Unit coverage on an excluded or otherwise inadmissible
pose does not establish this exception. All successful requested frames with no
hit produce a complete negative for this discrete method.

`RetrospectiveValidator(..., evaluator=screen)` ranks one resolved result per
molecule and reports unresolved molecule failures. Its full evaluations retain
frame failures even for molecules with a proven maximum. Counts of failed
molecules and failed conformers therefore need not coincide.

## Executable example

The synthetic charged fragments below isolate three known anchors. They exercise
the API and physical units; they are not a biological benchmark.

```python
import json
import molsysmt as msm
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import ConformerScreening

source = msm.convert(
    msm.convert('smiles:[Na+].[K+].[Li+]', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity(
    [[[0, 0, 0], [1, 0, 0], [0, 1, 0]]], 'nm'))
query = from_ligand(source, features=['positive charge'], radius='0.02 nm')
source.structures.append(coordinates=msm.get(source, coordinates=True))
prepared = msm.structure.translate(
    source, structure_indices=[1],
    translation=puw.quantity([[[2, 1, 3]]], 'nm'), in_place=False,
)
screen = ConformerScreening(query)
result = screen.evaluate(prepared, structure_indices=[1, 0], chemical_state='structure')
assert result['status'] == 'matched' and result['fit_value'] == 1
assert result['best_conformer_index'] == 1
assert result['ensemble']['n_evaluated'] == 2
assert result['resolved_chemical_state_index'] == 0
coordinates = puw.QuantityRecord.from_dict(result['pose_coordinates']).to_quantity(
    unit='nm', dimensionality={'[L]': 1})
assert puw.get_value(coordinates).shape == (1, 3, 3)
json.dumps(result, allow_nan=False)
```

## Verification and limits

`tests/test_conformer_screening.py` supplies analytical real-provider controls.
Verification uses the existing published source pins, MolSysMT
`4d490427e38c5836be82472348fdf61934442bda` and PyUnitWizard
`2ffe1885675f47c76af03c08e51bc889a5e99a05`, with installed dependencies.
It does not establish clean-wheel, hosted-matrix or biological-pilot compatibility.
The rigid triplet method's essential-anchor requirements, finite budget and
discrete search limitations apply per frame. Runtime scales with requested frames
and candidate fits; the current fitting consumer copies the provider system for
each seed. Streaming, compact prepared representations, Rust, GPU and distributed
execution need measured follow-up work in the appropriate owner.
