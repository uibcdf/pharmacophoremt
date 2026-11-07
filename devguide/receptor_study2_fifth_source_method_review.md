# BRD4 fifth-source review: FP-derived Ki, material and tracer pending — 2026-11-06

Owners LMMV/dprada; [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent [#103](https://github.com/uibcdf/pharmacophoremt/issues/103). The
[dated method plan](evidence/brd4_fifth_source_method_plan_20261106.json)
nominates AID 2061300 / BindingDB_12872_1 / US12286435B2, the fifth isolated-BD1
lead in the complete descending-raw-SID/ascending-AID order. Prior stops and
the separately held AIDs 1797292/1797167 remain unchanged. No activity balance
or PHMT score selects this source.

The [receiving and review receipt](evidence/brd4_fifth_source_method_20261106_summary.json)
retains original identities, executable controllers, a historical wording
correction, bounded search failures and the separately declared PCT follow-up.
This is documentary feasibility evidence, not an admitted biological cohort.

## Complete receiving and unchanged metadata

Exactly three original method requests return HTTP 200: description, summary
and the US patent. AID 2061300 retains version 1/revision 2, BindingDB_12872_1,
195 SIDs/193 CIDs. Those are raw source counts, not independent chemical groups.

| Private original | Bytes | SHA-256 |
| --- | ---: | --- |
| PubChem description | 5,480 | `de7520007159b26acaa5e426d8c54565dd86de8ae1bc5a19a0411568c92d8ad3` |
| PubChem summary | 3,380 | `f9cfa2fac91f1a03a21fae987642c87f63f0da5952d611785a8f7ff11647df2c` |
| US12286435B2 HTML | 1,899,724 | `ec1355ed7c7cdfaa7e38557a81f4947acd76e83dcf441723331fed2d451217ca` |

Reusing the existing documentary parser yields a 616,451-byte US prose
projection, SHA-256
`fa085bff161bcf784bc55a1e8c95fa57b8a8d763ff3c3b9d4192c626c8e044e8`.
Fresh Name and Description canonical identities exactly match the original
capacity projection: 234 bytes / `84e4f5508b228ae335a2d50a95ea526a326a3c25125a70ea2507a2880e5b5e4c`
and 1,575 bytes / `6669bb5eb5eb1fa48ab9aaad6937a779ea466ed7f045c31b913077fd9016ba70`.
The old private census capsule is absent; its verified portable archive retains
these identities and the complete fixed lead order.

## Original endpoint and table unit

The [US original](https://patents.google.com/patent/US12286435B2/en) measures
fluorescence polarization during tracer displacement. It obtains an IC50 from
the concentration at the midpoint of the measured signal range, then uses its
reported equation to calculate inhibitor Ki. The Kd in that equation is
explicitly the protein–tracer dissociation constant. These are distinct
quantities; the review performs no conversion or independent assay validation.

Table 1 separates BRD4 BD1 and BRD4 BD2 columns and explicitly labels both
Ki in nM. Its 60-byte normalized header has SHA-256
`a1c2b61c1e03f554b263041b75c93c1f2d58fb36940d0ef2b324b82a3daad61b`.
Fresh metadata also names Ki in TIDs 4/5. This supports the intended BD1/FP/Ki
context, while individual-row correspondence with the BD1 column remains
unauthenticated. PubChem's standardized micromolar descriptor is a separate
curation statement; no individual activity payload is received.

The original method reports a protein concentration of 43.4 µM and an added 80 µL mixture
containing 37.5 nM protein/2.5 nM tracer. Keep their stated scopes: this review
does not derive final well concentrations or transfer them from BD2.

## Dated correction and incorporated PCT follow-up

Our historical capacity adjudication described a “KD title”. The identical
canonical source title actually preserves the literal `KO`. Correct our
characterization without rewriting that original adjudication or claiming a
PubChem metadata change. The US HTML also prints `30 mM` in its incubation
sentence; its cause and original PDF typography are not established here.

The received US cross-reference explicitly incorporates PCT/CN2020/073380
through a continuation-in-part relationship. A
[separate dated single-request plan](evidence/brd4_fifth_source_parent_method_plan_20261106.json)
then receives [WO2020156357A1](https://patents.google.com/patent/WO2020156357A1/en):
HTTP 200, 2,229,754 bytes, SHA-256
`2e2ab4d16800f6d303e299ffdf7869730bd7beafc7a8a023f835a872113b9fb2`.
Its private documentary projection is 907,192 bytes, SHA-256
`878e0f847a0995a7ff2e12ef04b7071b93223801ce249d85c8407be3843ee900`.

The PCT Chinese method and displayed English translation explicitly identify
Ki and state 30 min/30 minutes. Its equation is identical to the US equation
after whitespace normalization. These are positive source-specific observations;
the US `KO`/`30 mM` bytes remain intact. The review does not certify the whole
translation, diagnose PDF errors or infer equality of all compounds/tables from
incorporation of the PCT.

## Remaining material, tracer and curation authority

The reviewed US/PCT BD1 methods do not explicitly identify the actual species,
accession, expressed residue boundaries or tag. They also do not identify the
tracer or supply the numerical protein–tracer Kd required to reproduce the
reported Ki calculation. General BRD4/BD1 names do not fill these gaps.

A bounded three-call search includes a failed opening of the source-specific
BindingDB assay metadata page (`Cache miss`, no accepted body) and six search
queries. Indexed curator snippets annotate human BD1 residues 58–164 and,
separately, human BD2 residues 348–457. These are curator annotations; neither
the failed page nor snippets authenticate the material actually measured.
No molecular/sequence correspondence is attempted. Source-curation/license
version and compound-level interference/orthogonal confirmation remain separate
questions before later admission or individual-row redistribution.

This source stays pending at the original-method boundary. No dedicated
activities, class-frequency projection, class thresholds, cohort, receptor,
pharmacophore or score follows. Earlier sources are neither pooled nor relabeled,
and neither complete biological study under #103 has executed.

## Exposure, execution and next lead

Earlier #66/#106 exposure remains additive. Source navigation and search expose
chemical names, synthetic/NMR fragments, background potency statements and
individual Ki values; the private ledger retains the observed identifiers.
No chemical alias/structure/sequence interpretation, activity-class calculation,
blinded source selection or unseen-holdout claim follows. Source bodies,
tables, original navigation excerpts and exposure details remain private;
portable projections retain own facts and byte identities only.

Receiving runs serially on CPU 19 with 100% CPU quota, 512 MiB memory, zero swap,
32 tasks, nice 19, idle I/O and single backend threads. Actual observations are
in the receipt; both scopes report no memory-limit/OOM events. Short offline
projection/review phases use one CPU, low priority and a 512 MiB address-space
limit, without cgroup no-swap or performance claims. Shared Conda/providers
remain unchanged. Owned capsule: `build/phmt-brd4-fifth-method-20261106-34jmdso_`,
review by 2026-11-20 or relevant change.

The next untouched fixed-order lead is **AID 1798835 / US9957263B2**,
BindingDB_3084_1 version 3/revision 2, 184 SIDs/184 CIDs. It needs its own dated
method nomination and verification of the original BD1 K57–E168 column.
The held sources retain their own authority gaps; no external message is sent
and no future lead is accepted by this review.
