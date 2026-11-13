# Cached inspection and comparison argument contracts

Owners LMMV/dprada; PHMT #204 under #6, selected 2026-11-12 local date.

## Contract and compatibility

`Pharmacophore.get_distance_matrix`, `to_dataframe` and `similarity` append
keyword-only `skip_digestion=False` and use definition-owned closed ArgDigest
contracts in the existing cached curation registry. Reuse consistent-model and
explicit-length/finite-three-coordinate validators; do not build another binder,
Domain or geometry engine. `tolerance_nm` is a finite nonnegative real scalar in
fixed nm, with booleans, strings, arrays, NaN/infinity and unrepresentable values
refused. This preserves the public numeric unit convention.

Scientific native checks remain active for deliberate bypass. All three methods
check native model consistency. Distance validates every center for models with
two or more sites, retaining the existing zero matrices for empty/singleton
models. No cylinder center is invented. Similarity validates both models, the
threshold and every present center; missing centers remain unmatched. Table
inspection keeps missing centers/radii and original quantity/feature-list cells.
Its new empty result has the same five columns as a nonempty result; replacing
cells is independent but mutating their contained objects edits the original.

The existing greedy similarity numerical loop is unchanged. It consumes nearest
unused same-feature counterparts in stored order and counts every input site in
the denominator. The label is corrected to ordered, greedy Dice-style score;
no symmetry, maximum matching, alignment, orientation/radius/weight/essential/
exclusion or biological interpretation is claimed. The independently owned
[#205 proposal](pending_proposals/symmetric_model_comparison.md) retains the
observed 0.5 versus 1.0 counterexample and future compatibility decision.

The distance matrix's existing internal `get(..., skip_digestion=True)` remains:
the caller now checks its model and centers and constructs only canonical fixed
flags/defaults. Native checks are not skipped. Other public calls retain their
own boundaries; no outer flag is blindly propagated and no speed claim follows.

## Receiving

Use `tests/test_cached_inspection_controls.py` and existing point, native-model,
curation/merge, contract and persistence controls. Independently check 3-4-5
distances, fixed-nm threshold meaning, feature alternatives/capacity, empty/
single/centerless models, actual table object ownership, no molecular access,
source custody, inherited contracts and native readback under nm/pm. Compare
lengths in explicit nm with declared numerical tolerances, keeping provenance
exact. Preserve the original 57 preimplementation failures and probe outputs.

Run source then an exact committed private wheel, actual SDK-staged support,
authenticated public Pytest Receptor 1.2.2 and public ArgDigest 0.17.1/PUW 0.28.1
receiving. Keep inherited dependency/prefix limitations explicit. Use one CPU/
backend thread, nice19/idleIO and finite per-process DATA/CPU/wall limits after
memory/swap/PSI checks, preserving 20% physical RAM plus 1.5GiB margin. No shared
resources are reserved. No native/provider/prefix/schema/dependency changes,
new remote CI dispatch, tag/publication or stopped #148/#165 work.

This receives three public boundaries, not complete #6 adoption or full supported
source/installed/public/platform, scientific-method or scale qualification.

## Source receiving — 2026-11-12 local date

The [source receipt](evidence/cached_inspection_controls_source_20261112.json)
passes 234 selected cases (65 new/169 existing), six public nm/pm guide blocks
and 13 quality operations, including strict docs and27 distribution tests.
All existing function bodies compare exactly after excluding only the declared
native guard prefix and DataFrame column keyword. Original57 red failures/probe
outputs remain. The bounded inventory observes150 callables/39 controls/123
plans. No new optional availability or attribution boundary is introduced;
existing Pandas/PyUnitWizard dependency ownership and pure cached inspection
behavior remain. Exact-owned/public-provider receiving follows committed freeze.
