# Explicit experimental cached-carbonyl generation

Contract declared 2026-11-05, owner LMMV/dprada,
[#94](https://github.com/uibcdf/pharmacophoremt/issues/94). This defines the source
API qualification target before implementation/evaluation. Delivery/results are
recorded separately. #92/#93's frozen scientific inputs, physical settings and
original results remain unchanged.

## Public choice and compatibility

Extend `modeler.from_receptor_features` with the explicitly chosen profile
`donor_aromatic_carbonyl_experimental`. Keep `donor_aromatic_faces`, its existing
arguments, method ID, enumeration, omissions and outputs compatible. No profile
is selected automatically, and `get_features` acceptors remain position-only.

The new profile additionally requires all four keyword arguments:

- `acceptor_directions`: native MolSysMT `molsysmt.hbond_site_directions@1`
  result, `method='ideal_local_geometry'`, `site_method='smarts_donor_acceptor'`,
  explicitly nonperiodic. Native unit-bearing origins are mandatory; saved
  QuantityRecord metadata is not silently decoded as scientific input.
- `acceptor_structure_position`: nonnegative integer position in the provider's
  ordered `evaluated_structure_indices`. It is mandatory even for one frame;
  repeated source indices must not silently choose the first occurrence.
- `acceptor_distances`: nonempty ordered list/tuple of positive scalar length
  quantities. Distances are hypothesis choices, separate from matching radii.
- `acceptor_target_orientation='towards_receptor'`: explicit PHMT rule that the
  ligand donor's D→H axis is -u for the selected provider direction u. No other
  rule is admitted initially. This is not a provider orbital/energetic inference.

These arguments default to None for old-call compatibility. The old profile
refuses non-None acceptor options rather than silently ignoring them. Existing
required donor/aromatic distance lists, positive radius, finite budget and optional
cached exclusions remain. Every scientific check applies with skip_digestion=True
and with zero budget, before constructing any hypothesis.

## Cached consistency and failures

The native chemical inventory must retain its original `hydrogen_bond` recognition
metadata. Match recognition method, resolved chemical-state index, original source
axis, selected atom set, donor/acceptor participants and recognition producer
versions against the direction result's `sites` metadata. Match integer state
selectors directly; reference means resolved state0, and structure-assigned
selection requires the captured resolved index. The explicitly chosen structure
position must refer to `feature_inventory.structure_index`.

Validate the versioned numeric code meanings, anchor/role/model/support tables,
CSR offsets, ordered sparse record/frame/local-direction correspondence, finite
unit directions, physical origins and their declared unit, and nonperiodic image
packing. Origins for a site's alternative directions share the same physical
point. Reject unknown schema/model/status, incoherent codes or malformed records;
do not infer missing fields, normalize an invalid vector or use another model.

Each inventory acceptor must have one anchor and exactly one provider acceptor
site. Duplicate acceptor anchors are invalid. Multifunctional donor/acceptor atoms
retain their separate typed roles. Curated feature subsets may leave provider
sites unused while retaining the original source selection/recognition evidence.
Source-support atoms may lie outside selection; they must lie in the declared
source universe. An admitted origin must match its cached feature center at
1e-12 nm; declared contexts/positions are not source-coordinate authentication.
No molecular system is accessed to verify or repair a cache.

Only acceptor role1/model2/status1 supplies two carbonyl alternatives at the chosen
position. Model0/status0 is `unsupported_acceptor_geometry`; model2/status2 is
`undefined_acceptor_geometry`. Known aromatic-N/nitrile models3/4 are
`outside_carbonyl_profile`, retaining their actual status in evidence. No omission
is a zero-fit pose score. A missing/mismatched recognized acceptor is invalid
cached context, rather than a valid unsupported record. Cached donor records
cannot supply an acceptor direction.

## Enumeration, exclusions and provenance

Combine unchanged donor/ring choices with carbonyl choices in original inventory
order. Acceptor choices are distance-major then provider local direction0/1.
Each admitted source feature occurs once in every hypothesis; alternative lobes
are separate complete hypotheses. The rightmost feature changes fastest. Keep
duplicate physical distance choices as distinct declared choices. Preserve the
lazy finite prefix, exact total/remaining/completion and empty-versus-truncated
semantics. Exclusions attach independently through the existing cache contract.

The new method ID is `cached_receptor_donor_aromatic_carbonyl@1`. Report parameters,
experimental scope, explicit orientation, selected structure position, omissions
and the original detached complete provider cache. Each model retains selected
provider record/site/local-direction indices, anchor/support, original state,
structure position/index, geometry, producer/model/recognition/reference evidence
and explicit PHMT decisions. Avoid copying the complete multiframe geometry into
every model: per-model selected evidence and the full report retain distinct
roles. Metadata, reports, input caches and models have independent ownership.

ArgDigest keeps the definition-owned signature contract and supplies nullable
argument digesters plus native cross-field scientific checks. SMonitor retains
PHMT-E102/ArgumentError; unexpected failures keep their original cause.
PyUnitWizard owns quantity validation/conversion and application policy authority.
This cached tool selects no optional molecular backend, so no new DepDigest
availability boundary is applicable. Optional Ackredit credits actual PHMT/unit/
numeric operations and preserves original provider credit without claiming new
molecular recognition/direction calculation.

## Qualification before delivery

Use typed synthetic caches for products, shared roles, multiple anchors, omissions,
known outside-profile models, invalid schemas/codes/units/context, empty and
zero/truncated budgets, lazy large products, metadata independence, source access
blocking, ArgDigest/diagnostics, native persistence and optional real/absent/failed
attribution. Synthetic caches are algebraic controls, not chemical evidence.

Replay #93's unchanged literal carbonyl/source/structure/unit/control matrix through
the new public generator: six blocks, 12 models, 72 primary/24 recovery evaluations,
plus four unsupported/undefined source queries with no scored poses. Retain all
old declarations/results and make a distinct measured identity. Reuse original
analytical candidate coordinates through public MolSysMT construction; compare
against the independent original-coordinate oracles and fixed fit arrays. No
new distance, tolerance, orientation, molecular preparation or physical choice is
tuned. Bounded public cookbook blocks must execute with real MolSysMT inputs.

This delivers explicit experimental source API support only after qualification.
One neutral-aldehyde receiving control does not qualify broader carbonyl chemistry,
nitrogen models, PBC, preparation/H refinement, physical accessibility, electronic/
energetic/biological validity, target breadth or performance. MolSysMT retains all
molecular representation/format/inspection/geometry responsibilities. Provider
floors/pins and installed/public #9/#23 gates remain separate; no release/addon.

## Source delivery — 2026-11-05

The declared API is now implemented in development source. **295 unique selected
controls have passing evidence across preserved runs**: 181 unchanged donor/
aromatic/exclusion/projection controls, 98 new public cached-carbonyl controls,
eight real-provider replay controls and eight frozen declaration guards. The
replay completes the unchanged 12 models/72 primary/24 recovery matrix and four
unsupported/undefined source queries. Three standalone cookbook blocks execute
with real MolSysMT input, two models and one JSON recovery, without pose scoring.

Original collection failure and four new guard-assumption failures remain in
the receipt. The guards needed an explicit attribution context and a floating
invalid-origin mutation; integer storage had truncated the intended .1 nm change.
Review also adds a regression for empty detached recognition lists while native
provider arrays retain their typed shape. No frozen scientific setting changes.
The independent original-coordinate replay and source/candidate/cache/unit
custody pass with stable source/native/helper/test/input/metadata identities.

[Original evidence](evidence/public_cached_carbonyl_20261105_summary.json) and
[public replay case](../docs/content/validation/public_carbonyl_generation.md)
retain exact source/commands and all attempts. This is explicitly experimental
source API qualification, not a public package or broad chemical-model result.
Next consolidate the proposed [0.5.0 candidate](release_0_5_0_readiness.md) under
#95 after exact-candidate checks; no tag/publication is performed here.
