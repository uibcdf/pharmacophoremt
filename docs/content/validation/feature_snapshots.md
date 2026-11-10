# Native feature snapshot controls

This analytical case, owned by LMMV/dprada under
[issue180](https://github.com/uibcdf/pharmacophoremt/issues/180), checks whether a
bounded snapshot preserves native feature geometry, original participants,
requested coverage and provenance. It is an unshipped research prototype.
The [supported manual reuse guide](../user/prepared_feature_reuse.md) remains the
user-facing route. No public snapshot API or production index is introduced.

## Inputs and independent expectations

The project supplies three original synthetic inputs, with no external dataset
or activity labels: three separated ions, isotopic water and a planar benzene
ring. All molecular construction, aromaticity annotation and native H5MSM
write/read use public MolSysMT. The
[declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/feature_snapshot/declaration.json)
and [parent manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/feature_snapshot/parents.json)
retain coordinates in nm, chemical state0/frame0, ordered atoms, formal charges,
bonds, preparation, redistribution origin and exact artifact hashes.

| Request | Expected native evidence |
| --- | --- |
| Positive/negative charge and aromatic ring on three ions | Three signed charge features at their declared atom centers; aromatic family evaluated empty |
| Aromatic ring on three ions | Zero features with explicit completed requested-family coverage |
| Donors and aromatic ring on water | Two donors sharing the oxygen center, with distinct hydrogen participants and orthogonal unit directions; aromatic family evaluated empty |
| Aromatic ring on six carbons | One six-atom ring, zero centroid and an unoriented normal along the z axis |

The geometry tolerance is 1e-12 nm, with 1e-12 for direction/normal components.
The original three native artifacts roundtrip with zero coordinate error.
These controls establish geometry and accounting, not biological prediction.

## Executed results

The [2026-11-10 receipt and full original archive](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/feature_snapshot_prototype_20261110.json)
record 32 passing guards in each of two contexts: source and exact owned
`0.4.0+218.g5515e93`. Four requests under nm/pm application policies produce eight
complete rows per context. Original feature counts are 3/0/2/1. Scientific values,
participant maps and public correspondence checks agree; actual producer labels,
recognition records and attribution remain as originally captured.

Two independent fresh readers each inspect all 16 original snapshots with
PHMT's main namespace, MolSysMT, NumPy, SciPy, RDKit, PyUnitWizard and Ackredit
imports blocked. No scientific module or import attempt is observed. Structural
inspection verifies schema, canonical bytes, integrity, counts and maps; it
neither reconstructs quantities nor authenticates the claimed molecular origin.
Explicit reconstruction separately validates known quantity fields through
PyUnitWizard, then the native inventory validator. Warm reading/reconstruction
also leaves the enclosing attribution unchanged. Each complete workflow retains
eight actual references and 12 uses; the archive preserves full nested records.

The guards cover corrupted/unknown/oversized data, invalid maps/coverage,
field/unit mismatches, nonfinite geometry, literal unit-like source names,
repeated source occurrences, later source mutation and detached outputs.
Controlled feature failure propagates as failure; partial output cannot become a
successful empty snapshot. Existing driver destinations refuse before scientific
imports. The original failed preparation and verifier attempts remain archived.

## Reproduce and maintain

The [unshipped driver](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/qualify_feature_snapshots.py)
and [focused guards](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/test_feature_snapshot_prototype.py)
consume the same fixed artifacts. The
[receiving contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/feature_snapshot_prototype.md)
records the environment, resource limits and original failures. Prepare a
compatible admitted environment and apply the shared-workstation limits before
running these opt-in commands; choose unused output destinations and supply the
SHA-256 of your own frozen execution context:

```bash
python -m pytest --receptor=llm tests/test_feature_snapshot_prototype.py
python -m devtools.qualify_feature_snapshots \
  --output snapshot-result.json --snapshots snapshot-files \
  --admission-sha256 YOUR_FROZEN_CONTEXT_SHA256
```

The received run uses Python3.14, one CPU/backend thread and the unchanged
original native binary. It verifies 214 wheel payloads, 159 runtime bodies,
4,594 provider Python files and 11 case files. Exact source/owned version labels
and dirty overlays are retained, rather than inferred from a version string.
Changes to capture, decoding, preparation, provider boundaries or independent
expectations require a new run identity. Cheap archive reading verifies saved
bytes without repeating molecular calculations.

The [24 design-case mapping](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/examples/feature_snapshot_prototype_coverage.json)
marks three covered within this bounded profile, 14 partial and seven deferred.
Generic collections/lifetimes remain owned by
[MolSysMT624](https://github.com/uibcdf/molsysmt/issues/624). Automatic compatibility,
query/index/plan decisions, atomic refresh, public API promotion and human
usability remain open. Timing and memory efficiency are not measured. Exact-head,
installed-platform, public-package and release gates retain separate evidence;
resource-stopped measurements148/165 are not retried here.
