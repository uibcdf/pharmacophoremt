# Native observations for an interface hypothesis

This analytical case supplies the small H0/H1 inputs offered to BindingMT#112
from PharmacophoreMT development. Owners: LMMV/dprada; consumer tracking:
[PharmacophoreMT#108](https://github.com/uibcdf/pharmacophoremt/issues/108).
It checks native selection, evidence reuse and constraint decisions; it does
not demonstrate an implemented BindingMT interface or biological binding.

## Inputs and independent expectations

The [frozen inputs and content map](https://github.com/uibcdf/pharmacophoremt/tree/main/tests/data/binding_interface_handoff)
are newly authored, publishable synthetic controls under this repository's
license. Four disconnected ions have explicit formal charges, one structure,
reference state0, identity local/source axes and no PBC. In nm, A=Cl− is at
(0,0,0), B=Na+ at(.2,0,0), C=Na+ at(0,.25,0), D=Cl− at(0,.45,0).
The binding question groups A+B against C; D remains contextual.

Native MolSysMT ionic detection at0.31/0.35nm must yield A–B, A–C and C–D.
Strict selection of AB versus C keeps only A–C and its original occurrence in
each named analysis. The two labels have different cutoffs but describe the
same configuration. An evaluated0.01nm analysis is empty and retains coverage.

The observed-C hypothesis must contain one essential positive-charge sphere,
weight1, radius0.02nm, with both labelled contributions. This is observed-ligand
modeling. The source still includes the full chemical context during construction.
The separate alternative moves C by0.05nm; it is not merged or averaged.

| Control on C | Expected fit | Expected decision |
| --- | --- | --- |
| Primary on original; alternative on its own source | 1 | matched |
| Primary on alternative; alternative on original | 0 | not_matched |
| Additional absent essential site, weight0 | 1 | not_matched |
| Exclusion at C | 1 | not_matched |
| Explicit keep of the two repeated constraints | 0.5 | not_matched |

The extra controls refuse conflicting geometry, contradictory states/maps,
unevaluated coverage and a cut compound charge participant. Missing/corrupt
assets fail rather than becoming valid empty evidence. These answers follow
from the declared geometry and constraints, independently of stored outputs.

## Execution and receiving

The [executable driver](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/qualify_binding_interface_handoff.py)
uses public owner tools. Full named analyses and structures are persisted through
MolSysMT H5MSM1.0; hypotheses use native PharmacophoreMT JSON. The manifest binds
files and source/analysis/site links for this trusted test case; it is not a new
interaction codec or BindingMT schema.

```bash
python -m devtools.qualify_binding_interface_handoff --read-directory tests/data/binding_interface_handoff --length-unit nm
python -m devtools.qualify_binding_interface_handoff --read-directory tests/data/binding_interface_handoff --length-unit pm
python -m pytest tests/test_binding_interface_handoff.py -q
```

Use the declared development route and shared-workstation limits: one allowed
CPU/backend thread, low CPU/I/O priority, finite wall/CPU limits and the bounded
512MiB DATA envelope after checking available memory/pressure. Fresh generation
requires a new `--output-directory`; delivered inputs remain frozen.

The [measured receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/binding_interface_native_handoff_20261112.json)
retains source/import/native identities, actual outputs and attribution, initial
test-controller failures, unit policies, commands and process resource outcomes.
The [contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/binding_interface_native_handoff.md)
and guard above own maintenance. Rerun after relevant adapter, composition,
constraint, persistence or provider changes; append a distinct measurement.

Saved reading with molecular detection/recognition blocked must preserve
metadata and essential/weight/exclusion semantics without new originating credit.
Evaluation and explicit reconstruction are separate scientific operations.
When reconstruction executes with a later PHMT version, its new root/component
producer declarations identify that version; reading the stored model keeps the
original producer. The [producer-oracle correction](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/native_handoff_producer_oracle.md)
checks both declarations explicitly and retains exact comparison of every other
metadata/site/contribution field, original reference and frozen input byte.
Native attribution records software actually used; no literature-derived method
or external dataset is claimed for these authored controls.

## Limits

These are source-only receiving controls in the recorded Python3.14 workspace,
not a fresh installed/public or supported-platform gate. Matching each source to
its own model is consistency evidence. There are no activity labels, experimental
structures, predictive splits or affinity claims. No search, performance comparison,
arbitrary remapping, ensemble, PBC or other interaction-family qualification is
established. Whole-process resource measurements serve execution safety only.

BindingMT still owns and must execute its actual I0/H/I1 admission, construction
and persistence. The supplied files do not certify shared-schema acceptance,
consumer adoption or cross-component interoperability.
