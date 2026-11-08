# CDPKit: screening-database identity, updates and failures

Source inspection, 2026-11-08; owners LMMV/dprada;
[#128](https://github.com/uibcdf/pharmacophoremt/issues/128),
[CDPKit record](https://github.com/uibcdf/pharmacophoremt/discussions/132),
consumer destination [#108](https://github.com/uibcdf/pharmacophoremt/issues/108).

## Question and evidence

The initial [workflow survey](pharmacophore_library_workflow_survey.md) left
duplicate/replacement semantics unresolved. This review follows those operations
through CDPKit tag `v1.3.0`, commit
`a8c798572f28eefd564b020621e514909b5552d8`. Ten captured source blobs retain
their Git identities and SHA-256 in the
[source receipt](evidence/cdpkit_library_update_review_20261108.json).
Selected functions were inspected; this is not an exhaustive code audit.

The live documentation labels itself 1.3.0. Its page label does not authenticate
the deployed binaries or bind every page to that source commit. No CDPKit binary
was installed, compiled or executed; no molecule, timing or PHMT adapter was used.
Findings below describe the inspected implementation and remain separate from
the proposed consumer requirements and unexecuted cases.

## What the operations actually select

Official [creation](https://cdpkit.org/applications/psdcreate.html) and
[merge](https://cdpkit.org/applications/psdmerge.html) help distinguish the three
modes. Their defaults differ: creation uses CREATE, merge APPEND; duplicate
dropping is disabled in both. These defaults agree with their pinned command
implementations. A friendly facade must resolve and display the actual operation.

| Mode with duplicate policy | Selected source behavior |
| --- | --- |
| CREATE | Recreates the owned tables before input processing. |
| APPEND, duplicates allowed | Inserts incoming entries alongside existing entries. |
| APPEND, duplicates dropped | Rejects hashes already present at opening or successfully processed in this session. |
| UPDATE, duplicates allowed | Replaces opening-time rows with the same hash; subsequent same-hash inputs in this session can accumulate. |
| UPDATE, duplicates dropped | Replaces opening-time matching rows with the first successful incoming entry; later same-hash entries are rejected. |

The implementation loads existing hash/ID mappings at opening and removes a
hash from that map after successful replacement. New rows receive insertion IDs;
stable external identity cannot be inferred from their numeric values. This is
replacement behavior, not a union of old/new conformer ensembles.
[Creator processing/setup](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Libs/C++/Source/CDPL/Pharm/PSDScreeningDBCreatorImpl.cpp#L258).

## Identity, coverage and failure distinctions

| Inspected boundary | Observation and its implication |
| --- | --- |
| Molecular duplicate key | The default graph hash uses atom/bond properties including charge, isotope and stereochemical configuration. It folds its digest into 64 bits. Coordinate/source identity needs separate records; no collision or chemistry equivalence test was run. [Hash defaults](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Libs/C++/Include/CDPL/Chem/HashCodeCalculator.hpp#L59), [result](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Libs/C++/Source/CDPL/Chem/HashCodeCalculator.cpp#L284). |
| Searchable coverage | Insertion can succeed without pharmacophores when both conformations and 3D coordinates are absent. Molecule and pharmacophore counts are separate accessor operations. Insert count alone cannot establish searchable coverage. [Generation](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Libs/C++/Source/CDPL/Pharm/PSDScreeningDBCreatorImpl.cpp#L467), [accessor counts](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Libs/C++/Source/CDPL/Pharm/PSDScreeningDBAccessorImpl.cpp#L113). |
| Merge compatibility | The merge path copies stored pharmacophores, derives feature counts and rehashes molecules. It does not regenerate chemical features or explicitly compare feature-generation contexts there. Readable storage is not sufficient evidence of semantic compatibility. [Merge](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Libs/C++/Source/CDPL/Pharm/PSDScreeningDBCreatorImpl.cpp#L304). |
| Failure scope | Transactions and rollback guards surround individual insert/replacement operations; CREATE setup commits separately. Earlier completed records can remain after a later failure/cancellation. Whole-refresh publication needs a separate contract. [Transactions/setup](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Libs/C++/Source/CDPL/Pharm/PSDScreeningDBCreatorImpl.cpp#L147), [merge cancellation](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Apps/CmdLine/PSDMerge/PSDMergeImpl.cpp#L148). |
| Input accounting | Read failures log and advance; molecule-processing exceptions set a terminal error. Source-file annotation is optional and uses a filename. Original selected-record denominators and persistent lineage need more than inserted/processed totals. [Read loop](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Apps/CmdLine/PSDCreate/PSDCreateImpl.cpp#L478), [worker](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Apps/CmdLine/PSDCreate/PSDCreateImpl.cpp#L124). |

Two tempting interpretations were rejected during review. Reopening does reset
the processed-hash set in `loadMolHashToIDMap`; this inspection supports no
stale-cache defect report. Per-operation rollback also must not be equated with
power-loss durability; the selected source is not a crash-recovery experiment.
[Opening/reset](https://github.com/molinfo-vienna/CDPKit/blob/a8c798572f28eefd564b020621e514909b5552d8/Libs/C++/Source/CDPL/Pharm/PSDScreeningDBCreatorImpl.cpp#L407).

## Proposed PHMT and provider requirements

These are concrete consumer requirements to review under existing owning issues,
not accepted API names, new containers, implemented connectors or a CDPKit engine
adoption. Molecular representation/preparation remains MolSysMT-owned.

| Requirement | Owner and user consequence |
| --- | --- |
| Keep source record, occurrence, prepared molecule/state/conformer and search-work identities distinct | MolSysMT collection operations under [#624](https://github.com/uibcdf/molsysmt/issues/624); PHMT consumes mappings. A duplicate decision retains every original occurrence and its disposition. |
| Make replace, append and conformer-union separate explicit choices | Molecular provider defines preparation/merge policy; PHMT records it in the task. A preset preview explains which previous variants survive and why an input is omitted. |
| Publish a replacement only after its declared acceptance | MolSysMT owns molecular snapshots; PHMT owns its feature/search assets. Keep the previous qualified snapshot available, and report candidate failure or staleness without silently changing its identity. |
| Record compatibility before reusing annotations | PHMT binds prepared snapshot, feature definitions, units/frames and actual producer/build context. A schema-readable merge cannot silently certify those scientific meanings. |
| Report coverage by stage | Preserve original records, imports, prepared states/conformers, annotated/searchable work, omissions and failures. A successful insertion or geometric nonmatch cannot manufacture a compound-level activity label. |
| Resolve defaults and resources in the public plan | Guided and expert composition use the same effective operation, grouping, selection and resource budget. Concurrency is explicitly admitted, rather than inferred from hardware or a tool's optional flag. |

The current PHMT reader already distinguishes work, attempts, confirmed failure
and pending state under [#157](archive/inspect_saved_work_item.md). These additional
requirements concern preparation/update/search assets; that reader does not
implement molecular collections or qualify these lifecycle guarantees.

## Declared follow-up cases, not executed

| Case | Observation required before accepting an implementation |
| --- | --- |
| Same graph, different source IDs/coordinates | Preserve both original occurrences; state explicitly whether coordinates, aliases or conformers are retained, replaced or rejected. |
| Two existing entries plus two same-key incoming entries | Check all modes/duplicate choices, exact surviving ensembles, aliases and counts. |
| Same update in one session versus two chunks/reopens | Declare and verify partition/winner semantics; do not assume that session boundaries preserve the result. |
| No conformers and no 3D coordinates | Distinguish imported-but-not-searchable from a valid evaluated negative, with original denominators. |
| Failure while constructing a replacement | Verify both per-record rollback and availability of the preceding qualified complete snapshot; retain the failed candidate and honest partial counts. |
| Cancellation after one successful record | Retain completed versus unprocessed work without claiming whole-refresh completion or durable recovery beyond tested limits. |
| Merge assets with changed feature/preparation context | Refuse or explicitly rebuild/migrate through the owning operation; prove the supported semantic relation. |
| Invalid input and duplicate source filenames | Preserve exact source/record keys, error/omission causes and replay/seek limits. |
| Reopen and deterministic duplicate selection | Verify reset and selected-winner behavior for admitted serial/chunked execution; separately qualify any later parallel policy. |

No case above has been run. Their preparation needs a separate prospective
question, authorized inputs, exact providers, bounded execution and independent
oracles. #148's original failures, workload and resource limits remain unchanged;
this study neither retries that route nor substitutes another benchmark.
