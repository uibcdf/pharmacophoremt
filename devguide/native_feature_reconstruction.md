# Native feature reconstruction

Owners LMMV/dprada; PHMT#193; 2026-11-11 UTC. This is a development-source
increment toward 0.6.0, after immutable source tag 0.5.0. No new tag or public
package is selected by this contract.

## Selected compatibility route

`screening.reuse_feature_inventories(view, required_families, *,
expected_generation, payload_profile, work_keys=None)` borrows the existing public
`FeatureAssetView`. The required `payload_profile="snapshot-study-v1"` explicitly
admits originals with schema `pharmacophoremt.feature-snapshot-study@1` and profile
`native-classical-single-frame@1`. Other schemas/profiles refuse. This is a named
compatibility decoder, not automatic promotion of study classes, stores or writers.
Runtime imports no `phmt_test_support`; historical original bytes stay unchanged.
A future public writer/native payload requires its own versioned format decision.

The admitted profile preserves the original limits: full parent atom axis of
1–256 atoms, frame/state 0, classical_atomic_formal@1, at most 64 features and
2 MiB per original payload. The stored caller-verified-artifact/unchanged-source
precondition and selected-case producer scope remain explicit original declarations.
They do not authenticate a molecule, its present state or an extraction method.

## Admission and lifetime

- ArgDigest checks the real public signature, view type, required family names,
  literal unique keys, exact expected SHA-256 and explicit profile selector.
  There is no unit-like key parsing or public digestion bypass.
- Each call rechecks the pinned generation, selected extraction completion and
  family evaluation through the public view. No inspection dictionary or mutable
  validation flag admits scientific reuse. Incomplete and unobserved families
  refuse; evaluated-empty families remain valid with their zero counts.
- At most 64 selected occurrences and 8 MiB of original bytes, counting repeated
  occurrences separately, are admitted per eager call. Check the full selection
  before decoding quantities. Larger selections require explicit batches from
  public metadata pages. These bounds do not establish scale or throughput.
- Parse canonical finite JSON, verify its original payload digest, and compare
  parent, producer, effective request and coverage against the pinned archive.
  Canonical byte comparison distinguishes booleans from integer frame/count values.
  Recount every family, validate all participant/geometry maps and preserve every
  captured feature, including families beyond the requested coverage check.
- Decode each feature center/direction/normal/charge afresh using public
  `QuantityRecord.from_dict(...).to_quantity(field=..., unit=...,
  dimensionality=...)`. Centers require nm/length; directions and normals require
  dimensionless vectors; charges require elementary-charge units, finite scalar
  values and their declared sign. The existing native inventory/orientation owner
  checks geometry. No new quantity codec or molecular fallback is introduced.
- Recognition and attribution remain detached original JSON provenance. They
  are not interpreted as native quantities or used to authenticate source maps.
  No new extraction credit, bibliographic enrichment or producer relabelling occurs.
- Return the complete native inventories, original work/source/occurrence keys,
  global ordinals and extraction metadata in manifest order. Each call owns fresh
  decoded objects. Return no partial batch on failure. The caller owns closing
  the view; returned data survives its closure.

An empty explicit selection returns no inventories and claims no quantity
validation. A complete selected subset may come from an incomplete manifest;
the report retains whole-manifest completeness separately. Query admission,
matching, source authentication and saved-run resumption remain independent.

## Support ownership and qualified lower bound

PyUnitWizard >=0.28.1 is the selected published capability floor for this new
quantity-record route, not a claim that its provisional interchange is stable.
The original public `pyunitwizard-0.28.1-py_0.tar.bz2`, SHA-256
`d4654faf93ed4181bf331f7d382379e78f02784f71f678ad19d0ac43d8062cc6`, has
[provider publication evidence](https://github.com/uibcdf/pyunitwizard/blob/2ab37a525ce99728ad8aee846b4a4f7acc4f1b65/devguide/evidence/release_0.28.1_2026-10-05.json).
Consumer controls run against its actual extracted payload, not a simulated
version or a shared-prefix downgrade. Metadata, the prospective Conda recipe and
generated ordinary environments carry the same floor. Existing controlled source
pins remain unchanged; pinned 2ab37a5 follows 0.28.1 with documentation-only commits.
That exact consumer qualification is separate from a full new public installation.

DepDigest gates explicit scientific dependency activation. ArgDigest owns public
argument admission; SMonitor owns catalog/capture/rendering. PHMT-E308 reports
generation mismatch; E309 missing family evaluation; E310 original metadata/layout
disagreement; E311 quantity/native-geometry failure; E312 absent quantity-record
capability; E313 the declared batch budget. Existing reader/format categories
remain intact. Native/provider causes are retained; raw originals are not attached
to diagnostics. Application capture policy remains authoritative.

## Acceptance and later work

The [receiving receipt](evidence/native_feature_reconstruction_20261111.json)
receives source 1604a6d and its exact owned wheel: 271 selected cases each,
114 real public-lower-bound reader/native cases, both scientifically cold readers,
the guide under nm/pm in both contexts and strict full docs. The
[#193 archive](archive/native_feature_reconstruction.md) owns the completed bounded
slice and its failed first attempts. The quantities/provider interface remains
provisional; no supported public-artifact matrix or new tag is inferred.

Receive original source and exact-owned installed contexts, actual lower-bound
provider bytes, nm/pm policies, empty/incomplete/literal selections, wrong sealed
quantities/geometry/maps, real diagnostics and no-new-credit/reference evidence.
Execute the user guide using the same operations as expert composition. Keep
failed initial control assumptions and every actual run identity.

Public writing/recovery, MolSysMT#624 collections, current molecular-source
authentication, persisted lookup, performance/scale, biological and representative
human usability remain separate. #192 owns interruption-test isolation; full
exact-head and public/platform delivery remain #9/#10/#23-owned. #148/#165 stay
stopped. This contract supplies no general collection or production index.
