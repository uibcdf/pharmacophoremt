---
summary: Receive ERalpha occupancy custody and actual chemical-reference data credit.
issue: uibcdf/pharmacophoremt#209
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: medium
verification: measured
area: [validation, integration]
guard: tests/test_eralpha_receptor.py::test_audit_reference_oracle_rejects_missing_extra_or_misclassified_credit
normative:
blocked_by: []
supersedes: []
---

# ERalpha controlled-provider receiving

## Observed failures and ownership

Frozen source 91eed32c55cbb53b2ba5f4a36d63add62c006798 failed source run
43472677149, attempt 1. Every executed scientific job (four Linux minors and
macOS/Python 3.11) reports 3,698 passes, two failures and 48 warnings. The other
three macOS jobs were cancelled without scientific qualification. Their linked
capacity/acquisition annotations are unverified hints. The old H5MSM reader
failures are absent. Original failed runs, fixtures and published receipts stay
unchanged; this result is rejected as a complete source checkpoint.

Two consumer expectations were stale after the reviewed molecular-provider
advance. The CIF reader now preserves deposited occupancy (MolSysMT 06c065d33),
and residue coverage credits the chemical catalogues actually inspected. The
old tests expected only B-factor loss and only one observed-data reference.
The two failures reproduce locally with all seven controlled source revisions;
there is no demonstrated provider regression or molecular algorithm to repair.

## Annotation custody

The original EST heavy input retains twenty occupancy values of 1.0. Generated
hydrogens have no deposited occupancy. The explicit intersection policy reports
both b_factor and occupancy loss on the expanded copy, which has no fabricated
occupancy. The positive guard checks that exact report, the unchanged original
values and the missing output field. The existing strict-policy guard now also
checks occupancy custody after refusal. Its durable selector is
`tests/test_eralpha_hydrogens.py::test_strict_annotation_policy_rejects_without_changing_heavy_source`.

## Actual reference use

The case-only oracle binds all eleven catalogue identities to the public
residue-coverage reports and hashes of the actual packaged resources. It also
checks their independently expected filename set, the one original observed
PDB manifest, all twelve complete dataset records and their uses. Observed data
keeps input_data; catalogue reads keep chemical_reference_data and their actual
public molecular caller. No completed interaction engine, template application
or H generation is inferred from the blocked detector attempts.

Three negative controls reject missing catalogue evidence, an unexecuted extra
dataset and a wrong role. The oracle parses no molecular catalogue and imports
no private provider implementation. It is a private test-case expectation, not
a new attribution framework or public runtime API. Public user recipes now
preserve the same annotation and credit distinction.

## Executed receiving and limits

The [receipt](../evidence/eralpha_controlled_receiving_20261113.json) retains
76 passing native/reference/ERalpha cases, including the three new controls,
and 16 recipe-block executions across nm and pm. All seven runtime provider
revisions match the controlled inputs: three public payloads have 161 Python
bodies checked against their Git pins, three pure-Python providers are built
and received from exact local Git objects in task-owned paths, and the original
MolSysMT Git-source staging retains its inherited-extension limitation. Its
unstamped source truthfully reports 0+unknown. These are not public artifacts or
a supported installed-package matrix. Shared prefixes/providers remain untouched.

Original two-failure baseline, complete failed-run capture and native logs are
retained locally. Only reviewed public scalar/source facts are published. Local
work is serial, one CPU/backend thread, low CPU/I/O priority and bounded by
1 GiB DATA, 120 CPU seconds and 180 wall seconds per scientific process, with
memory/pressure and own-process-family monitoring. No shared capacity is reserved.

#207/#9/#23 retain complete corrected-source recovery. A new immutable checkpoint
must still execute every supported cell and verify its native steps, no skips
and full qualified XML. No tag, package, scientific-definition change, biological
claim or restart of #148/#165 follows from this bounded oracle resolution.

## Provider feedback

GH Run Receptor 1.5.0 intentionally selects one best cause per failed job, so
its compact result displayed the reference-count failure while native summaries
also retained the earlier independent annotation failure. [GH Run Receptor #86](https://github.com/uibcdf/gh-run-receptor/issues/86)
proposes bounded multiple-group visibility or an explicit omission notice. It is
an improvement request, not a regression claim. Native inspection resolved both
consumer mechanisms together; no receptor source/installation was changed.
