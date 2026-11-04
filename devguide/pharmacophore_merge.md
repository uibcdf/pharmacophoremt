# Pharmacophore.merge compatibility and ownership

[#77](https://github.com/uibcdf/pharmacophoremt/issues/77), reviewed 2026-11-04;
owner LMMV/dprada. `left.merge(right)` now delegates once to the existing public
`compose_pharmacophores({"self": left, "other": right}, duplicate_policy="keep",
name=left.name)` and retains left.description. No second composition engine,
molecular copy, inspection, preparation, recognition or alignment is introduced.

## Result and compatibility decision

| Concern | Current explicit contract | Former behavior / migration |
| --- | --- | --- |
| Site order and duplicate occurrences | All left sites, then all right sites; no deduplication, averaging or added weights | Existing order and no-dedup behavior retained |
| Ownership | Each output occurrence/site/shape and nested metadata is independent, including self-merge and repeated/shared inputs | Former mutable site aliases are intentionally replaced; edit sources explicitly when source mutation is intended |
| Name and description | First input's name and description | Retained |
| Model metadata | Existing composer root with components labelled self and other; each component retains its original metadata, name, description, score and references | Old implementation returned {}; its docstring promised first-root metadata. Access that preserved content through metadata.components[0].metadata, not by flattening conflicting root keys |
| Site metadata and observations | Existing composer contribution snapshots and component-scoped observations; local relation/occurrence indices remain traceable | First/second sources stay unchanged; merging is not new molecular detection |
| Score and ref_mol | Output None; input values retained in component provenance | Old output defaults retained; input scores are not a joint score |
| ref_struct | One common known frame if present, otherwise None | Former output always None; conflicting known frame indices now raise before returning |
| Molecular source | First live molecular_system reference; no source cloning/inspection | Retained reference policy from #60. Equal frame indices do not authenticate a shared source/origin |
| Empty/self/chained input | Empty components remain in provenance; all-empty result stays empty; self/repeated sites remain independent constraints; nested histories retained | No synthetic site, collapse or inferred consensus |
| Invalid components / failures | Existing public composer admission and failures; inputs unchanged and no partial result returned | Unchecked attribute failures and silent frame disagreement are replaced with public diagnostics |

Both models must be declared in one coordinate frame by the caller. A matching
numeric frame index is insufficient proof of common axes, molecular identity,
chemical state or preparation. Align/prepare molecular systems through MolSysMT
before producing the hypotheses. For explicit component names or supported
native same-participant reuse, call compose_pharmacophores directly.

This is a joint collection of constraints. It does not compute consensus,
frequency/essentiality, similarity, spatial clusters or pose alignment. Repeated
constraints may compete under one-to-one matching; keeping them is an explicit
scientific choice. Different-complex consensus remains a separate method/study,
not a side effect of merge. All-empty results cannot be used as a pose query.

## Provenance, persistence and attribution

Metadata namespace migration is explicit: original first-root metadata is retained
under the self component, and second metadata under other. Nested compositions
retain the previous metadata tree; source site maps are component-local. Reserved
composer fields do not overwrite the original component snapshots. Mutable input
objects are not modified in success or the guarded refusal paths.

Native JSON/YAML preserve the resulting composer metadata/constraints under
pharmacophoremt.native@1. Direction/length handling remains the existing owning
shape/PyUnitWizard contract. Optional attribution follows the existing composer
boundary: composition is recorded when enabled; cached original citations remain
provenance and molecular detectors/fits are not re-executed by merge. No new
reference, provider dependency or molecular routine is added. Live molecular
objects themselves are not serialized/copied.

## Evidence and limits

[Receipt](evidence/pharmacophore_merge_20261104_summary.json) retains exact accepted
source/test overlays on base 528872f516bb617741f547046f43ae5697e6fa1c and every
attempt. Original-production guards fail 23 cases and pass two; these failures
cover both the confirmed metadata defect and the intentional new ownership/frame
contract, not 23 separate pre-existing scientific defects. The initial Ruff
semicolon report is corrected by formatting before that execution. A patch call
with an incorrect path made no file change and was corrected before testing.

**202 broad compatibility controls pass** (154.19 s), followed by **28 final
merge guards** after adding chained provenance/deep-copy refusal and clarifying
the composer docstring. Both runs retain exact overlays and stable identities.
Final focused source receiving covers independent six-shape data, metadata/scores/
references, duplicates/self/empty/chained input, frame admission, deep-copy refusal,
public delegation, molecular-operation prohibition, non-default units and native
persistence, plus existing composition/curation/copy/schema contracts. Full counts
and all identity results are in the receipt. This is Linux/Python 3.14.7 source
receiving with extracted public ArgDigest 0.17.0 and inherited scientific
dependencies, not full-suite, clean installed/public/all-platform, predictive or
performance qualification. SDF container migration #74/MolSysMT #215 and broader
API/scientific gates remain separate.
