# Live molecular references and independent pharmacophore variants

Source/API receiving under [#60](https://github.com/uibcdf/pharmacophoremt/issues/60),
2026-11-04, owner LMMV/dprada. This review qualifies existing operations; no
runtime implementation or dependency floor changes. [Receipt](evidence/live_reference_ownership_20261104_summary.json)
records exact source/test/provider identity and limits.

## Ownership choices

| Operation / state | Owned independently | Intentionally retained / responsibility |
| --- | --- | --- |
| `query.copy()` / `modeler.copy_pharmacophore(query)` | Native sites, quantities, feature lists and nested metadata; original score and bibliography preserved | Same live molecular_system reference and positional ref_mol/ref_struct. No molecular copy, inspection or new scientific calculation |
| Extraction / independent curation | Selected/edited native data, detached source snapshot and local site map | Live molecular source remains intentional; edited/extracted score invalidated and original retained in history |
| Explicit `msm.copy(source)` / `source.copy(deep=True)` | Molecular domains, controlled edits and named analysis handles according to MolSysMT's supported source contract | General molecular implementation, chemistry, coordinates, ownership and invalidation belong to MolSysMT |
| Complex facade | Native query/result from declared cached observations; previous results remain historical objects | Source and supplied analyses are caller-owned live references; source must stay unchanged while observations are reused |
| Structure facade | Query sites from cached inventory and explicit projections; failed builds clear current result | Cached inventory/frame/source identity is a caller declaration, not authenticated by local molecular inspection |
| Ligand facade | Native result/report for an explicit prepared consensus | Prepared source records remain references; failed builds clear both result and report |
| Legacy `Pharmacophore.merge` | Not qualified by this review | Confirmed metadata loss and measured shared sites are separate #77; do not generalize curation-copy results to every library method |

Model indices and ref_mol/ref_struct are positional declarations in the original
source context, not persistent molecular IDs or a copy operation. Saved native
files do not reconstruct the live molecular source. A pure pharmacophore copy
must preserve original attribution rather than claim another detection/fit run.

## Edits and cached evidence

A controlled MolSysMT edit of an independently copied source invalidates the
current named analyses only on that edited owner. The original molecular system
and its analyses remain intact. Repeating a controlled edit on the original
still leaves the variant independent. Retained old analysis handles remain
historical results; their coverage is not rewritten into a new calculation.

A live molecular reference does not cause cached pharmacophore sites to follow
source coordinates automatically. After an edit, cached models/reports and scores
still describe their earlier calculation. Do not interpret their current linked
source as certified original geometry. Recompute required observations/inventories
through MolSysMT and rebuild the hypothesis explicitly for the new prepared source.
Rebinding a molecular pointer alone does not regenerate geometry or provenance.

Builder fields may retain earlier analysis objects supplied by the caller. The
provider's current owner registry invalidation does not authenticate an external
cached dictionary or erase saved models. No PHMT observer, local geometry stamp,
source fingerprint or molecular invalidation engine is introduced. Raw table/
array writes remain outside the provider's controlled edit guarantee and require
its documented explicit invalidation. Cross-source/frame declarations must not
be inferred from matching shapes or counts.

A refused coordinate edit preserves the molecular copy's coordinates and named
analyses. A resource extension whose copy hook refuses is propagated by the
public molecular copy operation without transferring/damaging the original
workflow. PHMT's own copy retains that live resource reference without trying
to clone the molecule. Existing failed builder/curation controls verify no
partially published current results or mutations.

## Provider receiving and evidence

The earlier #60 notice referred to an incomplete complete-system copy API.
MolSysMT #121 is now closed; its maintained native-copy contract describes
implemented independent resident copying. That changes the provider status,
not the scientific meaning of PHMT's intentional references.

**Executed provider:** source 0faf1584d05ac47ddcebfc20d9c9978b7f4f230e in the
controlled inherited Linux/Python 3.14.7 prefix. The separate current sibling
checkout 71fbe4f46d3c70e4e973c8025f01752a8c9b1084/native-copy guide was inspected
read-only, not executed as that scientific provider. Public ArgDigest 0.17.0 is
extracted into PYTHONPATH; other scientific dependencies are inherited. No shared
prefix, sibling source or support metadata is modified.

[10 new integration controls](../tests/test_live_reference_ownership.py) use a
prepared analytical disconnected participant fixture (not experimental biology),
public molecular copies/edits, real named analyses and actual Ackredit capture.
They qualify default eager public/native copy routes under nm and pm policies:
full observation/source/occurrence/coverage/provenance payload retention, atom
selection/coordinate equality, bidirectional independent controlled edits and
owner-local invalidation, retained historical analysis/query values, failed
resource copy/coordinate edit and pure-copy/no-new-credit behavior.

The selected scope passes **199 controls** in 119.67 s, including existing
curation, complex/ligand/structure facade and contract controls. An initial test
attempt has eight comparison failures/two passes: two aromatic profiles retain
NaN intersection distances and plain dictionary equality treats those as unequal.
A probe confirms exact NumPy comparison passes with the same NaN positions.
The corrected guard preserves those unavailable measurements, never imputing zero.
Original attempts and one standalone helper-import correction remain in the
receipt. Both attempt source/native/test/metadata identity comparisons stay stable.

This is bounded source consumer qualification. No clean installed/public-closure,
all-platform/minor, full-suite or predictive claim; no copy speed or arbitrary
extension/table-cell/deferred-copy promise. Wider client workflows remain
[MolSysMT #408](https://github.com/uibcdf/molsysmt/issues/408); central coordination
is [MolSysSuite #122](https://github.com/uibcdf/molsyssuite/issues/122).
The review closes #60's existing-reference/eager-copy scope. Audit item 5's legacy
merge finding remains open #77, with composition/source policy to be settled there.
