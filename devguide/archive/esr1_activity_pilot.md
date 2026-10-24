---
summary: Frozen ligand-reference ERα assay pilot with held-out experimental outcomes.
issue: uibcdf/pharmacophoremt#62
status: resolved
opened: 2026-10-23
closed: 2026-10-24
verification: measured
area: [validation, mvp]
guard: devtools/tests/test_esr1_activity_pilot.py::TestEsr1ActivityPilot::test_original_accounting_and_metrics_have_independent_oracles
normative: devguide/validation_collection.md
blocked_by: []
supersedes: []
---

# Frozen ligand-reference ERα activity pilot

## What and why

Resume the MVP after public 0.4.0 and documentation foundations. Existing
geometry/prepared controls do not measure discrimination of assay activity.
This bounded retrospective case uses prepared published 3D inputs and existing
native PharmacophoreMT tools. It does not wait for receptor H refinement.

## Declared experiment

The acquisition/split manifest is
`tests/data/esr1_activity_pilot/manifest.json`; the opt-in driver is
`phmt_test_support/esr1_activity_pilot.py`. Bath's CC BY-SA 4.0 ESR1ago table
supplies selected IDs and labels, independently checked against PubChem assay
743075. No docking score or imputed potency enters the experiment. The Bath
archive is not interchangeable with the original full LIT-PCBA population.

Before any scores, exclude every CID with contradictory substance outcomes:
2662, 5361202, 6128 and 17113. Preserve the eight original conflicting rows.
Order remaining unique CIDs by SHA-256 of `phmt-esr1ago-pilot-v1:<CID>`.
The first active, CID 9821849, is the sole reference; seven other actives and
24 inactives are held out. No replacement after acquisition/preparation/search
failure. CID disjointness does not establish chemical-series independence.

Each source is a single computed PubChem 3D conformer, with supplied chemical
state and explicit hydrogens; it is not an experimental bound conformation.
Public MolSysMT reads SDF and performs the sanitizing RDKit conversion roundtrip;
the consumer observes counts, declared state and coordinate/identity preservation.
No local molecular parser, conformer generation, protonation or scaffold routine
is added. Raw SDF/archive bytes remain outside the repository; URLs, hashes,
attributed labels and the acquisition recipe are retained.

The single-reference native model requests donor, acceptor and aromatic families;
all emitted sites are essential, with radius 0.15 nm. Native `RigidPoseSearch`
uses 10000 trials, point tolerance 0.10 nm, direction tolerance 30 degrees and
minimum fit 0. Native `RetrospectiveValidator` records failures, evaluated-subset
ROC AUC, BEDROC(alpha=20) and tie-aware EF at 10%. This small selected cohort
does not support full-benchmark early enrichment, affinity or prospective claims.

## Execution and acceptance

Use an owned isolated public-provider environment with PharmacophoreMT 0.4.0
and MolSysMT 0.23.0. Execute the driver by file path so the installed runtime,
not the checkout package, supplies the API. Retain actual runtime origins,
versions, driver/manifest/query hashes and producer identity. Molecular work
stays upstream; newer-provider qualification remains a separate #41 task.

Completion requires original full outputs, saved query, per-input preparation
and evaluation outcomes, clear denominators, independent accounting/metric
checks, a maintained validation case and an updated checkpoint. An uninformative
or negative scientific result is retained without tuning held-out parameters.
Any later consensus or conformer continuation has a distinct declared run.

## Current evidence

The pre-score protocol/driver is committed at
`ee064102f3701a280297e01ec0c549207f10bfd3`; the installed public runtime is
PharmacophoreMT 0.4.0 / MolSysMT 0.23.0, Python 3.14.9. No source runtime changes
or new provider implementation is needed. The [summary](../evidence/esr1_activity_pilot_20261023_summary.json)
qualifies original full output, preparation journal, saved query and log.

Of 32 inputs, 27 have PubChem 3D records; one further input (CID 6842999) is
rejected by MolSysMT's explicit stereo guard. Reference self-fit is 1; its query
emits two acceptors and one aromatic site, with no donor. Held-out outcomes are
25 evaluated (6 active / 19 inactive) and six unscored (1 active / 5 inactive).
One active hits; 23 scores tie at zero. AUC is 0.5614035088, BEDROC(alpha=20)
0.5994951770, EF at 10% 1.6908212560. All 25 declared triplet enumerations
complete, with at most 256 raw trials; continuous pose/conformer completeness is
not established. Failure-bound hypothetical AUC is 0.4494–0.6280, not a confidence
interval. This is weak exploratory discrimination, not predictive acceptance.

The [case](../../docs/content/validation/esr1_activity_pilot.md) explains exact
denominators, failed-input placeholders versus original preparation causes,
small deterministic sampling, unresolved chemical-series overlap, actual
Ackredit payloads and the lack of population/performance claims. Three offline
guards independently check split/provenance and pairwise AUC/tie-aware EF.

Remaining acceptance is portable long-term original-input retention: raw SDF
and source archives remain in the owned acquisition directory; public strict
restore refuses changed bytes, so refreshed source responses may require those
originals. No blanket PubChem redistribution license is inferred. Keep this
issue partial for that disposition and the next separately declared comparison.
New conformer capability belongs to MolSysMT #219; stereo interpretation belongs
to #215/#299. No local workaround or silent state repair is added. Addon,
release infrastructure and deeper documentation remain deferred.

## Development replay — 2026-10-24

The separately [predeclared replay](../../tests/data/esr1_activity_pilot/seeded_replay_declaration.json)
now executes the explicit seed-only binary criterion under #63, using identical
original query bytes and all original input identities/order. The
[new summary](../evidence/esr1_seeded_hit_replay_20261024_summary.json) binds clean
source `c80325c5c3851691bcc0a993d1e73eaf294654f6`, actual runtime origins and
325 provisioned Conda records, with PHMT replaced by editable source. Public
MolSysMT is 0.23.0 and PyUnitWizard 0.29.0; this is not a new public PHMT artifact.
Stale pre-commit editable version metadata is retained explicitly, not used to
identify executed source. All 949 source tests pass in that qualified context.

The same 25 inputs evaluate and the same six remain unscored; the same sole
active CID 24964624 hits. Scores are 1 for that fitted hit and 0 for all completed
negatives (24 zero ties); raw partial coverage is not a molecular rank. Binary
AUC is 0.5833333333, BEDROC(alpha=20) 0.6496274186 and EF at 10% 1.9675925926.
Twenty-three valid negatives have no fitted pose/coverage, which is distinct
from a calculation failure. The original result is not rewritten. Changing
criterion and recording a separate runtime does not establish improved biological
prediction; this cohort is exposed development data, not a fresh holdout.

#63's bounded scoring contract is resolved. This case remains partial for
portable long-term original-input retention and stronger independent scientific
validation. Further query/criterion development must not reuse these outcomes as
unseen validation. Molecular conformer/stereo capabilities remain provider-owned.


## Portable input retention and closeout — 2026-10-24

The [input snapshot](../evidence/esr1_activity_pilot_inputs_20261023_summary.json)
now preserves the exact original 35-file bundle (12,495,338 compressed bytes,
SHA-256 `fc6a5295bbf4dbd9743f31a7f54d396b09578e60754ebcabd4388a588252e995`).
The [notice](../evidence/esr1_activity_pilot_inputs_20261023_NOTICE.md) records
Bath's CC BY-SA 4.0 terms, PubChem/NCBI computed-data and U.S. Tox21 provenance,
and the NCBI contributor-rights limitation without inventing a blanket license.
The original dated manifest's narrower publication decision is preserved.

The existing unshipped case driver reuses `evidence_archive.read_archived_bytes`
for checksum-qualified transport. `--restore-archive` restores all original
responses and the separately archived query into a new directory, offline,
without scientific imports or attribution registration. It verifies every file
against the original producer's manifest, refuses member/path substitutions
and existing directories, and retains all five HTTP failures. Molecular I/O
continues to belong to MolSysMT; no new runtime API, provider workaround,
optional engine, distribution dependency or shared workflow is introduced.

Seven offline guards pass, including the restored Bath selection, independent
primary-assay label agreement, original file/query hashes and rehashed malicious
archive/manifest rejection before writes. The CLI restores 35 inputs plus one
query. This is byte-retention verification, not a rerun of molecular science;
the original and development-replay measurements and environments remain dated.
The complete administrative/documentation selection passes 38 tests and 24
subtests, including the strict Sphinx build; the separate archive and reporting
processes pass 18 and three tests. The snapshot summary retains the executed
CLI receipt and corrected invocation context. Whole-tree Ruff and report-index
checks pass. No full molecular suite is rerun for this transport-only change.

This completes the bounded #62 acceptance: frozen inputs/protocol, executed
original outputs and replay, failure/metric accounting, maintained case and
portable original inputs. No predictive acceptance is claimed. A genuinely
unexposed evaluation set and any new training/consensus comparison are separate
future work, rather than indefinite conditions on this completed pilot. The
prior partial statements above describe their dates and are superseded here.
