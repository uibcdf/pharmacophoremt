# Cached prepared ERα receptor and contact control

## Identity and claim

Case `cached-prepared-eralpha-receptor@1`, owned by
[PharmacophoreMT #52](https://github.com/uibcdf/pharmacophoremt/issues/52),
maintainers LMMV/dprada; review date 2026-10-10. Evidence class: analytical
classical-workflow controls on a historically prepared real fragment. The claim
concerns explicit projection geometry, exclusion vetoes, retained native contacts,
source maps, saved models and failed rebuild semantics.

Translated PHE404 is a synthetic methodological candidate, not an independent
ligand, generated conformer, experimental binding pose or activity label. Contact
reconstruction does not qualify freshly detected or environmentally refined
interactions. No biological or performance claim applies.

## Inputs and preparation

The [prepared-fragment recipe](../cookbook/prepared_eralpha_interface.md) retains
original deposited 1QKU acquisition/licensing references and explicit chemical
assumptions: receptor residues 304–550, excluded incomplete residues, HIE states,
charged termini, inspected ARG correspondence and generated local hydrogens.
This stage reads the unchanged archived H5MSM, without repeating preparation or
detection. Its 4,047 atoms/4,088 bonds include 1,995 observed heavy atoms and 2,052
local H. Full-receptor, environmental H and peptide stereochemical acceptance
remain outside the historical preparation claim.

The [original summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/eralpha_interface_py314_summary.json)
identifies the prepared artifact by compressed/uncompressed SHA-256 and byte counts.
The loaded native bytes have SHA-256
`a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`.
Original data/atom maps remain in the
[fragment manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/eralpha_interface/manifest.json).
A reusable offline archive-byte reader verifies identity; MolSysMT decodes the
molecular format and supplies all selections, recognition, planes and movement.

PHE404 ring atoms are `[796,797,798,799,800,801]`; heavy atoms 791–801. All selected
atoms, including nine H, retain complete-system indices. EST selects 4003–4046.
Frame zero/reference chemical state is explicit. Separate ±z ring hypotheses at
0.35 nm with radius 0.02 nm use caller-declared vectors and explicit copied cached
ring axes. Exclusion radii 0.01/0.40 nm are independent query choices, not physical
radii. A positive PHE404 candidate uses public `[0,0,.35] nm` translation; the
observed EST negative uses `[2,0,0] nm` displacement of a copy.

## Execution and independent controls

The [recipe](../cookbook/prepared_receptor_workflow.md) composes public tools.
The [maintained contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/prepared_receptor_workflow.md)
describes independent atom, mean-center, plane, distance and veto expectations.

```bash
python -m devtools.prepared_workflow --case receptor --output /tmp/prepared-receptor.json
python -m pytest tests/test_prepared_receptor_workflow.py tests/test_receptor_projections.py tests/test_complex_based_facade.py --receptor=llm
```

Use normal editable `molsyssuite@uibcdf_3.14`, without Requires-Python/PYTHONPATH
bypass. Retain current producer source/input/loaded-extension identity alongside
historical preparation hashes/date, the original head/dirty developer/test overlay,
full guards and actual attribution. Query evaluation uses one-degree angular
tolerance. Cross-unit/independent geometry comparisons use 1e-12 nm/dimensionless.
All source coordinates, full chemical-state/history and cached analyses are
compared before/after; literal unknown native NaNs remain in finite JSON text.

Four query variants write/read through JSON/YAML/versioned PHMT virtual-site SDF
under pm/fs/degrees then Å/ps/radians. Fresh processes read twelve saved models
without new calculation uses. These codecs represent pharmacophores; native
molecular I/O continues through MolSysMT.

## Results and interpretation

Seven new scientific guards pass in **122.44 s on Python 3.14.7**. The broader
initial selection passed 133 unchanged controls (66 receptor projections, 31
complex facade, 36 previous prepared placed/search/consensus); seven new cases
initially failed at setup due to the client expecting the host exception family
for a provider out-of-range frame. Corrected handling retains that provider error
and adds explicit invalidated-frame-zero coverage checks. Only the affected seven
guards were rerun; they all pass. Original initial failure logs/client/guard remain
in the evidence, without claiming that initial selection passed completely.
Both public recipe blocks and the reviewed installed-development preflight pass.

The [new original summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/prepared_receptor_workflow_py314_summary.json)
links the full original gzip output by compressed/uncompressed SHA-256 and byte
counts. Its producer head is `a64e369eae1bbd331b7cfd2f17371ce38b73d284`, with
an explicitly uncommitted developer/test overlay retained as executed bytes.
Runtime scientific source remains unchanged. All 31 prior JSON gzip archives and
the native prepared input retain their original bytes. Both host tracking modes
pass with identical scientific fields and unchanged producer Python/input hashes.

The positive projection and exclusion-veto control have the same positive coverage, while the broadened veto changes final
status. The opposite hypothesis and original candidate test distinct geometric
negatives. Independent original-coordinate means/plane axes and atom-to-atom
bounds protect these expectations rather than relying on self-placement alone.

Observed native families retain twelve hydrophobic contacts and zero H-bond/pi-pi
contacts. Deposited participant identities and direct distance arithmetic check
the hydrophobic evidence. Source reconstruction retains six sites and the
evaluated-empty labels. Empty/exclusion-only hypotheses cannot be positive queries;
uncached/unevaluated frame failures must clear both facade results.

Host-on capture retains twelve items/36 uses, including the actually consumed
prepared artifact dataset. Host-off retains three items/three uses from independently
configured provider operations. Fresh processes read all twelve saved models and register zero new uses.
Historical preparation/detection attribution is kept as cached provenance, not
new execution credit. The strict isolated rendering of these two new pages uses
Sphinx 9.1/Python 3.13, without claiming a scientific gate on that interpreter.

No labels, splits, enrichment denominator, prospective binding acceptance or
speed/memory comparison are measured. Optional attribution must name the derived
prepared artifact actually loaded, without claiming historical preparation or
contact detection was executed again.

## Maintenance and independent gates

Rerun after input/native loading, source maps, cached observations, projection/
exclusion decisions, geometry, persistence or failure contracts change. Append
new identities, preserve old outputs and keep current provider hashes separate
from historical preparation provenance. MolSysMT #375/#323/#350/#367 and required
hosted/installed/public delivery #23 remain separate gates. No sibling source or
runtime molecular implementation is added here.
