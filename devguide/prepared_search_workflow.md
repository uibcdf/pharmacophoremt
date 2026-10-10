# Prepared query continuation through rigid and frame search

Owned by [#50](https://github.com/uibcdf/pharmacophoremt/issues/50), continuing
the [placed analytical case](prepared_end_to_end_workflow.md) under #49.
All scientific operations already exist: cached curation and codecs belong
to PharmacophoreMT, molecular recognition/access/transformations/fitting to
MolSysMT. Only fixed-case orchestration, evidence selection, guards and guidance
are added. No provider implementation is duplicated.

## Declare a method-compatible hypothesis

The prior query contains one essential aromatic site and nine optional hydrophobic
sites. It remains valid for placed evaluation and is explicitly refused by
`rigid_triplet_fit@1`. Through `edit_pharmacophore`, make cached hydrophobic sites
one/five essential as well. In the frozen ring-first model they correspond to
source atoms zero/eight. The essential indices are `[0,1,5]`; their centers form
an independently checked non-collinear triangle. The aromatic weight remains
three and every hydrophobic weight one. All radii remain 0.02 nm.

These are explicit alternative hypothesis constraints, not automatic biological
site discovery or learned activity weights. The original query and complete
curation history remain in the saved model. Frame zero is the original prepared
CCD conformation. Frame one is the same conformation rotated 90 degrees about z
then translated by `[2,1,3] nm`, using public MolSysMT operations.

## Independent answers

| Control | Expected evidence |
| --- | --- |
| Placed evaluation of moved frame | Valid negative, coverage zero |
| Rigid search of moved frame, budget 10000 | Valid full-coverage hit with provider fit and source frame one |
| Original system selected to ring atoms only | Complete selected-participant negative, coverage 8/12, essential atom-eight site missing |
| Moved frame, one-product budget | Unscored search-budget failure, not a negative |
| Both frames, budget 10000 | Complete resolved hit; first requested frame wins the full-coverage tie |
| Both frames, budget one | Original frame establishes valid maximum; moved frame failure remains visible and ensemble incomplete |
| Rigid facade batch `[prepared, unprepared, prepared]`, frame one | Stable tied input hits zero/two, failed input one unscored, original source references retained |

The ring selection is `[0,1,2,4,5,10]`. Recognition operates on this selection in
the complete original molecular system; no molecular fragment is reconstructed.
The independent maximum selected atom distance cannot reach the required
ring-to-atom-eight distance within 0.04 nm pair slack. One budgeted raw product
reuses a candidate and is pruned. Identity placement still proves maximum
coverage for frame zero despite truncated proposal enumeration.

`ensemble.score_resolved=True` and `ensemble.complete=False` can both be true:
a valid matched pose with coverage one proves the maximum even when another
frame fails. All requested frames are attempted, every failure retains its
diagnostic and source frame, and failed searches receive no score. This does not
optimize RMSD among tied full-coverage placements or establish continuous
exhaustive search. Complete negatives apply to this discrete triplet method.

## Source preservation, persistence and provenance

The three saved codecs are JSON, YAML and versioned virtual-site PHMT SDF.
Writes use pm/fs/degrees; reads and calculations use Å/ps/radians. Evidence and
constraint fields remain exact; geometric comparisons declare absolute tolerance
`1e-12` nm or dimensionless units. Public alignment replay preserves frame zero,
recovers all 44 frame-one atoms against the original geometry and retains declared
chemical state. Original source and both prepared frames remain byte-equivalent
as numeric coordinate/state payloads before/after evaluation.

```bash
python -m devtools.prepared_workflow --case search --output /tmp/prepared-search.json
python -m pytest -q tests/test_prepared_search_workflow.py tests/test_prepared_workflow.py
```

The existing evidence driver now accepts explicit `--case search`; its default
placed case and reader names retain their contract. Both application-owned
host-attribution modes execute. New source/input/native-extension identities and
complete outputs have a distinct archive; earlier outputs retain their original
bytes and producer facts. Fresh readers load all three saved queries with no new
calculation credits. Ackredit is an explicit driver prerequisite; optional runtime
integration semantics remain unchanged.

The [recipe](../docs/content/cookbook/prepared_search_workflow.md) exposes public
steps; the [case](../docs/content/validation/prepared_search_workflow.md) links
original evidence. Maintainers LMMV/dprada rerun after changed preparation, anchor
membership/order, methods, tolerances, codecs or failure policy. These are ideal
prepared workflow controls, not biological/activity or timing/memory evidence.
MolSysMT #375/#219/#323 and #23 delivery gates remain independent.
