# Validation and benchmark collection

Decision: 2026-10-07, owned by
[PharmacophoreMT #20](https://github.com/uibcdf/pharmacophoremt/issues/20).
The first publication surface is a **Validation and benchmarks** section in the
existing library documentation. It reads and links the existing evidence
collection; no separate website or second result store is introduced.

## Options reviewed

| Option | Discovery and versions | Execution and maintenance | Decision |
| --- | --- | --- | --- |
| Library documentation | Beside public methods and recipes; reviewed in the same source history | Reuses Sphinx and current developer/scientific commands | Adopt now |
| Independent website | Separate navigation and deployment/version identities | Requires another maintenance and review route; does not solve evidence provenance | Defer until a concrete audience or interaction requires it |
| One collection with documentation and website views | Can serve both audiences from original results | Useful later if the second view consumes immutable original records | Keep compatible; add the view only when needed |

The cookbook teaches an operation. Case pages explain a declared scientific
question, independent controls, observed results and limits. They link the
same fixtures, commands and archives instead of copying executable notebooks,
reference outputs or whole preparation instructions. A future website must
consume this collection and preserve case/run identity.

## Source-of-truth layout

| Material | Owning location |
| --- | --- |
| Small frozen inputs and preparation manifests | `tests/data/<case>/` |
| Independently useful scientific operations | Owning `pharmacophoremt` module; molecular operations stay in MolSysMT |
| Local execution and case-specific expectations | Existing `devtools` driver and focused `tests` guard |
| Original measured outputs and reviewable projections | `devguide/evidence/`; new run identities never overwrite originals |
| Method/preparation contracts | Owning maintained developer document |
| User-facing case interpretation and collection navigation | `docs/content/validation/` |
| Recipe or notebook demonstrating an API | `docs/content/cookbook/`, linked from the case |
| Case contribution checklist | `devguide/templates/evidence_case.md` |

The collection index distinguishes these evidence classes:

1. **Analytical controls:** known geometric/ranking answers and independent
   oracles, including positive, negative, tied and deliberately failed inputs.
2. **Scientific validation:** declared real inputs and preparation/reference
   assumptions. Prepared ideal CCD geometry is a preparation/workflow control;
   it is not experimental or activity-based validation.
3. **Retrospective screening:** original/evaluated ligand counts, valid negative
   scores, recorded failures, activity labels and evaluated-subset metrics.
   Activity-based claims additionally need declared splits and leakage controls.
4. **Vertical pilots:** composition across tools with declared readiness,
   inputs, frames, blockers and independent end-to-end acceptance conditions.
5. **Computational benchmarks:** equivalent scientific workloads plus measured
   runtime/memory and variability. A count-only run belongs to another class.

One case can have multiple records, but a benchmark view cannot promote a
preparation control into biological evidence. Literature coverage, an algorithm
adaptation and an implemented complete method remain separate statements.

## Reproducibility and result history

Every case follows the template. It links original data URLs, acquisition dates,
redistribution terms, file hashes, chemical states, preparation and explicit
units. Record method/backend/plan, parameters, random seeds or deterministic
ordering, finite search budgets and exhausted versus incomplete search.
Results retain producer versions, source content hashes, dirty overlays and
native extension identity where relevant. An editable version string or Git
head alone does not reconstruct an uncommitted producer.

The command and compatible environment route are required. Historical source
hashes describe the original producer; a new run on changed providers is a new
measurement. Compare independent expected values and declared tolerances before
comparing counts or timing; never rewrite the old environment as current.
Store original full output, checksums and a linked summary. Corrections append
a dated explanation in the owning issue/page and preserve original claims.

Portable Ackredit payloads retain complete references and contextual uses for
the branches actually executed, including data versus resource descriptions.
Saved reading/rendering does not register usage or enrich citations. Reviewed
literature is labeled separately from captured execution. Absence or provider
failure must not manufacture attribution or erase completed scientific results.

Performance records additionally specify hardware/OS, threads/processes/GPU,
workload size, warmups, compilation/initialization, repeats, all timing samples,
memory scope and uncertainty. Whole-process peak RSS is not incremental call
allocation. Different returned alternatives or incomplete searches prevent an
unqualified speed comparison. Future Rust/GPU/distributed implementations must
pass the same scientific oracle and failure/coverage controls.

## Ownership, review and execution policy

PharmacophoreMT maintainers `LMMV` and `dprada` own this collection and its
publication decisions. Each new case names an accountable maintainer and an
owning issue; contributors propose cases there before adding queued reports.
The method owner reviews scientific assumptions and expectations. The data
contributor verifies provenance/redistribution and the publication reviewer
checks that claims match executed evidence. These are review responsibilities,
not new approval requirements for already authorized local development.

Lightweight local/CI controls check report indexes, archive integrity, fixed
inputs and the demonstrator's recorded counts/citation inventory using only the
standard library. `tests/test_evidence_archive.py` runs in the existing
independent reporting job, without launching molecular workflows. Existing
focused scientific guards remain in the component's scientific test selection.
This adds no new matrix, schedule or mandatory benchmark to ordinary pushes.

Larger drivers are opt-in: run the documented command after changes to its
scientific operations, preparation, expected outputs or provider boundaries,
before attaching a new result or claiming equivalence/performance. Finish other
tests/builds before timing; retain every repeat and failure. A changed answer
needs investigation and an owning issue, not an automatic baseline update.
Unchanged archived results remain dated evidence rather than validation of a
new head. Required source/installed/public qualification follows #9/#23 and
the existing suite policy independently of this collection.

Shared workflow evidence stays with `uibcdf/moli-vertical-pilots` and links its
immutable producer inputs/results. Cross-MOLI execution contracts belong in
`uibcdf/moli`; shared Python/CI/release/attribution policy belongs in
`uibcdf/molsyssuite`. Local case interpretation and PHMT expectations stay here.
This decision does not redefine their schemas or claim those pilots executed.

## Demonstrator and archive-reading contract

The [prepared CCD case](../docs/content/validation/prepared_ccd.md) links two
untouched EST/DES SDFs, their preparation manifest, existing driver, environment,
12 original count controls and complete actual Ackredit references. Its
recorded 2026-10-03 producer used an uncommitted source overlay; the archive
retains that fact and source hashes. Reading the original record is reproducible
from frozen bytes; exact reconstruction of that producer from its Git head
alone is not claimed. Rerunning current science uses the existing driver and
records a fresh environment/output.

`devtools.evidence_archive.read_archived_evidence(summary_path,
identity_key='full_evidence')` verifies compressed/uncompressed SHA-256,
optional byte counts and a sibling archive path, then returns the summary and
original JSON object. Historical `file` spelling and an explicit different
identity key are supported. It preserves unknown, failed and partial fields;
callers own scientific schema interpretation and acceptance. It uses no
scientific imports, executes no stored commands and mutates no files.

```bash
python -m devtools.evidence_archive devguide/evidence/prepared_ccd_py314_summary.json
python -m unittest discover -s tests -p test_evidence_archive.py
```

These commands verify the original archive, not the current scientific code or
installed distribution. The standalone tool is a local developer operation,
not a new supported runtime API or general molecular preparation service.
