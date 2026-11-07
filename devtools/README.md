# Development and publication tools

Optional, checked environment generation/create/update calls are documented in
[conda-envs/README.md](conda-envs/README.md). Runtime comes from `pyproject.toml`;
`environment_tools.toml` selects ordinary generated files and `requirements.yaml`
contains local tools. The shared environment SDK is fixed and qualified; recipe,
plan, science/source-manifest and artifact controls remain separate.

Publication controls: [conda-build/README.md](conda-build/README.md).
Source/context preflight: `check_dependency_routes.py`. Run it in the actual
selected environment before tests; declaration success is not installed evidence.
Routine workspace development uses `molsyssuite@uibcdf_3.14`; install eligible
local clones with `python -m pip install --no-deps --editable PATH`.

Contributions follow the root instructions and synchronized suite guide. External
contributions require owner review through a PR; authorized internal direct pushes
retain the common checkpoint rules. Scientific repairs and release decisions stay
local. Independent governance runs the reporting, route and distribution/helper
guards without importing the scientific package.

## Scientific evidence archives

Scientific fixture implementations live in the unshipped
[`phmt_test_support`](../phmt_test_support/README.md) package. The documented
`devtools.*` commands remain compatibility entry points. Installed tests use
MolSysSuite's declared private staging contract, independently of runtime package
discovery; the support namespace must never enter the distributed payload.

Prepared end-to-end qualification: `python -m devtools.prepared_workflow --output FILE`
composes the existing CCD fixture client, cached-model tools, three native codecs
and placed screening with independent negative/failure controls. Its
[contract](../devguide/prepared_end_to_end_workflow.md),
[recipe](../docs/content/cookbook/prepared_workflow.md) and
[case](../docs/content/validation/prepared_workflow.md) declare the scope.
This opt-in driver requires the development checkout and Ackredit for its
explicit application-session review. It is not biological or performance evidence.
Its explicit `--case search` continuation exercises saved rigid queries and
prepared-frame budget/score accounting; see the
[search contract](../devguide/prepared_search_workflow.md). The default placed
case retains its original contract and evidence identity.
The `--case consensus` continuation checks distinct prepared EST/DES supporters,
original occurrence maps and empty-versus-failed facade rebuilding; see the
[consensus contract](../devguide/prepared_consensus_workflow.md).
The `--case receptor` continuation consumes the archived prepared ERα native
artifact and cached observations, reviewing explicit ring projections, exclusion
vetoes and observed-contact reconstruction; see the
[receptor contract](../devguide/prepared_receptor_workflow.md).

`evidence_archive.read_archived_evidence()` reads the existing local gzip/JSON
archive envelope with compressed/uncompressed SHA-256 and optional byte-count
checks. It preserves original failed, partial and unknown fields, requires a
sibling archive and imports no scientific providers. Scientific schema and
acceptance remain with each producer/caller. `read_archived_bytes()` exposes the
same integrity checks for binary evidence without decoding; native molecular
formats remain provider-owned. Use
`python -m devtools.evidence_archive SUMMARY.json` for archive integrity only.
The [collection contract](../devguide/validation_collection.md) and
[case template](../devguide/templates/evidence_case.md) define contribution,
ownership, execution and historical-result rules.

`python -B -m devtools.brd4_label_capacity PRIVATE.csv REVIEWED_LAYOUT.json`
projects the single AID1805333 capacity case offline. Its caller must first verify
the published plan, before/after metadata and explicit micromolar descriptor.
The layout declares exact column indices and all five observed metadata rows;
no header alias, qualifier, missing value or biological label is inferred.
Output contains aggregate denominators and conservative SID bounds only. See
the [case outcome](../devguide/receptor_study2_label_capacity_receiving.md) and
`devtools/tests/test_brd4_label_capacity.py` for boundaries and stopping behavior.

Before publication, the CLI's two-MiB guard was hardened to read at most the
limit plus one byte before rejecting oversized input. Separate CLI controls
protect that bound and frozen-plan validation before source access. Classification
and aggregate output remain unchanged; earlier archived source/result identities
retain their original meaning.

The unshipped `phmt_test_support.prepared_library_reference.screen_prepared` prototype composes the
three native evaluators one prepared entry at a time, preserving work/source
occurrences, nested IDs and explicit score/failure meaning. It is development
code, with caller-owned readers and no acquisition, index, journal or public API
commitment. Its [contract and qualification](../devguide/prepared_library_reference.md)
link the declared analytical controls and original execution receipt.

`phmt_test_support.prepared_library_recovery` reconstructs native evaluators from
saved query bytes/effective settings and composes them with the unshipped
`reference_run_store`. The latter uses only the standard library for ordered
manifest validation, single-owner transactions, immutable confirmed outcomes and
saved replay. See the [controlled recovery contract](../devguide/prepared_library_recovery.md)
for publication versus delivery, producer preconditions and the separate evidence.

`python phmt_test_support/reference_run_store.py RUN.sqlite3 --score-method seeded_hit@1 --limit 10`
opens a saved run read-only and prints work coverage plus a bounded scalar view
of observed scores. It needs only the standard library and performs no molecular
work. [Inspection contract](../devguide/reference_run_inspection.md) explains
failures/pending work, ordinal ties and the source-only `ReferenceRunView`.

`python -m phmt_test_support.pubchem3d_receiving_pilot PLAN ACQUISITION OUTPUT`
executes the opt-in fixed-three receiving case **offline**, from authorized
original bytes whose plan/order/hash admission passes. It uses a fresh output
directory and records per-stage failures; one failed preparation stops scoring.
It adds no downloader or parser. See [the measured contract](../devguide/pubchem3d_receiving_pilot.md)
for local-only molecular artifacts, scalar publication and exact rerun context.
