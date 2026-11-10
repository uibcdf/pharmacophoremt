# Six-family native retrieval controls

This analytical case, owned by LMMV/dprada under
[issue182](https://github.com/uibcdf/pharmacophoremt/issues/182), expands
[snapshot ingestion](snapshot_retrieval.md) to all six classical families and
complete three/four-point queries. The composition remains unshipped. Its
[original receipt and archives](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/typed_retrieval_20261110.json)
retain successful, failed and interrupted evidence separately.

## Inputs and preparation

Four project-created disconnected-fragment parents provide independent chemical
and geometric witnesses. No external compound database or activity labels are
used; these geometries are analytical controls, not optimized conformers.

| Parent | Declared native evidence |
| --- | --- |
| Isotopic water plus Na/Cl | Two donor occurrences share an oxygen center but retain different hydrogen participants/directions, plus positive/negative centers: four features |
| Benzene plus ammonium/chloride | One six-atom aromatic normal and two signed charge centers: three features |
| Propane/carbonyl/Na | Central propane carbon, carbonyl acceptor and positive center: three features |
| Two propane fragments/carbonyl/Na | Two distinct hydrophobic centers, acceptor and positive center: four noncoplanar features |

The hydrophobic witness uses the provider's declared central-carbon rule;
terminal methyl is not assumed to match. Public MolSysMT owns construction,
ring-only aromaticity annotation and native H5MSM write/read. Ordered atoms,
charges, bonds, one frame/state and coordinates verify; all four native artifacts
roundtrip with zero coordinate error. There is no local molecular parser, repair,
hydrogen addition or conformer generation.

The [prospective declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/typed_retrieval/declaration.json),
[parent manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/typed_retrieval/parents.json)
and [original snapshot manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/typed_retrieval/originals.json)
retain hashes, explicit units, maps and preparation. Actual capture runs under
nm/pm application policies from source and unchanged owned218: 16 new byte strings
plus four old empty/short originals. Each context has eleven work occurrences,
including a repeated donor capture. Original positions 1/3/4/5/6/7/8/9/10 are indexed;
short positions 0/2 remain visible and are evaluated by the full-query reference.
Caller origin trust remains an explicit precondition, not source authentication.

## Complete queries and numerical boundaries

Twelve mathematical query families include shared donor occurrences, aromatic
normal reversal, three-in-four/full-four cardinality, a reflected four-point
distance proposal, translation, near collinearity, clear negatives and three
binary64 neighbors around an anchor coordinate of 5.25 angstrom at radius 0.125 angstrom.
Widths remain 0.125/0.5/1 angstrom. Centers are explicitly converted through public
PyUnitWizard; original directions, normals, charges and provenance are retained.

The original case helper admitted four labels and always requested three
matches. Two original red controls expose those limits: D/R rejection and a
three-pair result for a four-point query. The expanded helper requires the full
query size and explicit donor/aromatic query geometry. Its new live asset profile
is `classical-three-four-point-snapshot-study@2`; old asset identities are not
silently retained. The original native snapshot wire format stays unchanged.

The independent rational oracle checks full typed injective mappings against the
exact physical pair-distance inequality at 2r. Away from the numerical boundary,
99 cases per policy require equality with public native proposals. The separate
33 boundary observations per policy preserve both answers, including disagreements.
The native outward-rounded candidate band can retain uncertain proposals beyond
the exact pair-distance threshold. Neither oracle is final pose/activity acceptance.

## Executed results — 2026-11-10 UTC

Both source and exact-owned218 pass 60 selected guards: 19 new and 41 existing controls.
Each completes 72 query/width/unit-policy rows, 198 away-from-boundary rational checks
and 66 boundary observations. All native full-query mappings survive conservative
retrieval and agree across source/owned and nm/pm policies. Each context makes
264 exhaustive and 182 retrieved native calls, 446 in total, plus 20 supplied-pair
evaluations. Each width asset stores 42 pair entries. These are workload counts,
not timing, storage-cost or memory-efficiency measurements.

There are three rational/native differences per policy: the exact boundary at
original 7 and the successor boundary at originals 3/7. All are recorded as candidate-
band observations. The archive preserves original snapshots, public conversion,
freshly reconstructed operands/hex and independent rational readback; no physical
oracle equality is manufactured. Exact-bin-only misses are retained separately.

The three donor work occurrences each retain two four-feature proposals, with
all positions valid and one direction-valid mapping. Different hydrogen
participants are preserved. Both aromatic normal signs pass their supplied
mapping. Reflection remains a distance proposal; proper fitting is not qualified
here. Pending donor originals 6/10 and unsearched work remain unknown in a prefix.

No molecular operation is observed during tests or frozen-feature retrieval.
Original reading/reconstruction creates no original-workflow credit. Each new
complete retrieval session retains eight actual references/twelve uses, while
capture has eight references/eleven uses. Old references remain original data.
Two fresh readers each inspect all 20 snapshots with scientific imports blocked,
verify 125 public support payloads and refuse four existing output paths.

## Resource interruption and preserved ordinary answers

An ordinary-source comparison stopped on the conservative global-swap alarm,
with own observed RSS below 170 MB and about 56 GB available. The partial JSON retains
20 complete rows; its unsaved original session attribution remains unknown.
The installed ordinary run had already completed before a precautionary stop
request; no process matched that request. After three stability observations,
a separately declared suffix receives only four pending source rows with nine
new native calls. Original partial bytes/status remain unchanged. All 24 ordinary
scientific rows per context agree with the earlier #181 answers; the source result
is an explicit 20+4 composite, not an uninterrupted workflow or restored old credit.

[Issue183](https://github.com/uibcdf/pharmacophoremt/issues/183) owns partial driver
attribution retention. Its gap is not an Ackredit or native scientific defect.
No resource limit was raised; no failed old workload or #148/#165 route was retried.

## Reproduce and maintain

The [driver](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/qualify_typed_retrieval.py),
[guard](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/test_typed_retrieval_domain.py)
and [receiving contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/typed_retrieval_domain.md)
link the exact environment, frozen code/inputs, original red/static/resource
failures and receiving commands. Admit a compatible environment and shared-machine
resources, supply your own frozen-context SHA-256 and choose an unused output:

```bash
python -m pytest --receptor=llm tests/test_typed_retrieval_domain.py \
  tests/test_snapshot_retrieval_ingestion.py tests/test_retrieval_control_oracles.py
python -m devtools.qualify_typed_retrieval --output typed-result.json \
  --snapshot-context source --admission-sha256 YOUR_FROZEN_CONTEXT_SHA256
```

The received route uses Python 3.14, one CPU/backend thread and the unchanged
original native binary. All 214 wheel payloads/159runtime bodies/4594provider Python
files and 60 green fixture files verify. Capture/tests/retrieval load 148/144/146 PHMT
module origins respectively. Exact original producer labels and dirty overlays
remain in the archive. Changed features, binding, query/cardinality, numerical or
provider assumptions need a distinct run identity and scientific review.

This bounded result does not promote a public API/index, generic molecular
collection, arbitrary-scale recall, equivalent cost, biological performance,
human usability or supported installed-platform/release delivery. Next address
partial checkpointing under #183 before admitting longer equivalent-cost experiments.
MolSysMT#624 and the resource-stopped #148/#165 measurements retain separate ownership.

## Checkpoint follow-up — 2026-11-10 UTC

[Issue183 receiving](retrieval_checkpoints.md) now preserves observed session credit
with each scientific progress checkpoint in both opt-in drivers. Separate new
complete experiments preserve original scientific projections and bibliography;
controlled interruption retains the last committed partial. The older interrupted
session and its missing attribution remain unchanged. Equivalent-cost workload
and admission design is the next gate before production-index selection.
