# Prepared construction-to-screening control

## Identity and claim

Case `prepared-workflow-est@1`, owned by
[PharmacophoreMT #49](https://github.com/uibcdf/pharmacophoremt/issues/49),
accountable maintainers LMMV/dprada; review date 2026-10-10.
Evidence class: analytical controls on public prepared real chemical data.
The question is whether explicit cached curation constraints and provenance
survive persistence and control the complete placed-screening batch as declared.
Ideal geometry is not biological validation, an observed bound pose or an
activity-based retrospective dataset.

## Inputs and preparation

Reuse the frozen [CCD EST/DES input provenance](prepared_ccd.md), selecting EST
only, its untouched SDF and [manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/prepared_ccd/manifest.json).
EST SHA-256 is `9b3fe86469dd81554830f01ea11daa6d58fe329a887e6b36f0a42481eb18980f`.
The manifest retains original source URLs and acquisition record; the existing
case documents public redistribution provenance. No new dataset is downloaded.

The public MolSysMT fixture recipe preserves 44 source atoms, 47 bonds, 24
explicit hydrogens and one ideal-coordinate frame while declaring aromaticity
through its supported RDKit conversion route. CTAB stereo interpretation retains
the original qualification limits; no pH optimization or environmental H
refinement is implied. Source atom identity, elements, state and coordinate
immutability are checked. Only nine hydrophobic participants and one aromatic
ring are requested. No molecular donor/acceptor direction engine is invoked.

Public MolSysMT translations produce 0.05 nm and 2 nm z displacements.
The batch has five entries: three prepared placements of one molecule, one
explicit unprepared propane and a repeated original source reference.
All prepared placements use frame zero/reference chemical state. Repetition is
a stable-tie control. No training/test split, activity labels, metrics or chemical
diversity claim applies to this analytical batch.

## Execution and environment

The [executable recipe](../cookbook/prepared_workflow.md) composes separate public
steps. The [maintained contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/prepared_end_to_end_workflow.md)
declares three hypotheses, independent pair-distance/weight/CTAB controls,
one-degree aromatic tolerance, minimum coverage 0.2, failure accounting and
the exact scoped commands. Source-checkout execution uses the normal editable
`molsyssuite@uibcdf_3.14` installation; no path/version bypass is needed.

```bash
python -m devtools.prepared_workflow --output /tmp/prepared-workflow.json
python -m pytest -q tests/test_prepared_workflow.py
```

The driver retains before/after producer Python hashes, loaded MolSysMT extension
hashes, source head/dirty overlay, driver/guard/helper/input hashes, original
preparation observations, complete models, encoded artifacts and full native
screening records. A changed provider defines a new measurement, not a rewrite
of old evidence. No runtime or memory benchmark is performed.

## Scientific results and maintenance

The [2026-10-10 summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/prepared_workflow_py314_summary.json)
links the original checksum-qualified full archive. Both host-attribution modes
pass all nine variant/codec controls and yield identical scientific fields.
The focused scientific selection passes 15 tests on Python 3.14.7 in 26.20 s,
including both original default-feature preparation cases. The original source
head is `74bf6c628930613b61b4f62645c17f1bb6b985d2` with a declared uncommitted
developer-tool/test overlay; the archive retains its executed source bytes.
Runtime scientific source is unchanged. All 28 earlier gzip archives retain
their original bytes.

The maintained contract specifies independent expected answers. The narrow
query rejects the 0.05 nm displacement, the wider ring query accepts it at
coverage 0.25, and a zero-weight optional exclusion vetoes exact self placement
at coverage one. A far displacement is a valid negative; failed preparation
retains `fit_value=None`. JSON/YAML/versioned PHMT SDF preserve constraints,
source mappings and curation history exactly; geometry uses absolute tolerance
`1e-12` nm or dimensionless units across application policies. Fresh-process
readers retain saved evidence and register no new uses.

Actual application-owned Ackredit evidence is retained for executed branches
and public input data; reading saved results does not claim another calculation.
Host tracking disabled retains four items/six uses from independently configured
provider operations; host tracking enabled retains 14 items/24 uses, including
one actual EST input dataset. Disabling host tracking does not disable every
provider's own attribution configuration. Both fresh readers register zero uses.
No private pilot evidence is published or implied by this control. Larger
discovery projects retain their independent readiness and scientific acceptance.

Maintainers rerun after changes to selected participants, preparation, curation,
codecs or screening contracts. Append new measurement identities and preserve
original output bytes. MolSysMT #375 remains required for #41's donor-vector
migration elsewhere, and #323 remains the environmental H-refinement scope.
Required hosted/installed/public qualification remains #23.
