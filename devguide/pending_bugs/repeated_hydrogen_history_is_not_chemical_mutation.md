---
summary: Separate repeat-H chemical invariance from appended operation history.
issue: uibcdf/pharmacophoremt#39
status: active
opened: 2026-10-05
closed:
severity: medium
verification: measured
area: [validation, integration, provenance]
guard: tests/test_eralpha_hydrogens.py::test_second_hydrogen_addition_is_an_unchanged_independent_copy
normative: devguide/eralpha_validation.md
blocked_by: []
supersedes: []
---

# Repeated hydrogen operations preserve chemistry and append history

## What

The original native ERalpha guard compares the complete ChemicalStates payload
after repeated fixed-state H placement. Current MolSysMT legitimately appends
unchanged terminal-attachment and H-addition operation records, so complete
payload equality incorrectly classifies historical evidence as a chemical change.

## How

Adopt the provider's proposed owner-review patch and strengthen original-source
immutability: snapshot the complete original chemical payload and history before
the call; require the original to remain unchanged; compare output assignments
separately from history; require the original history prefix and exactly the two
new unchanged records. Retain independent-copy, zero-added-H, empty parent-map
and coordinate-equality assertions. No molecular implementation is copied here.

## Why

Recording an attempted operation is distinct from modifying chemistry. Removing
all history assertions would lose the evidence that protects this distinction.
The provider handoff is retained under MolSysMT's prepared ERalpha consumer data;
its isolated qualification is separate from this owner checkout's execution.

## What is measured and what is assumed

On Python 3.14.7 in the normal editable `molsyssuite@uibcdf_3.14` workspace, the
three pilot modules pass all 27 controls in the initial 69-control selection.
Ten curation setup errors in that selection have a separate cause: the retired
Interactions.between spelling, migrated through the public between_selections
operation under the existing #36 consumer theme. The strengthened repeat-H guard
and six CI route/backlog controls subsequently pass seven tests in 7.26 s.
The full historical 542-test evidence remains a dated result, not a claim for
today's changed providers. Current source integration and hosted checks are
recorded in the publication checkpoint.

## Alternatives and refuted paths

Do not change the provider to suppress valid history, reinterpret reports as
assignments, remove source-immutability checks or manufacture chemical changes.
Comparing only atom counts would not protect chemical fields or retained history.

## Scope and exclusions

One native pilot regression and its explicit provider-history contract. No new
hydrogen algorithm, state choice, receptor preparation or biological acceptance.
Original inputs, historical reports and evidence archives remain unchanged.

## Acceptance criteria

Independent returned object; original complete payload/history unchanged; equal
chemical assignments and coordinates; zero new H; preserved history prefix and
two unchanged appended operations. Execute the owning guard and relevant pilot
modules, publish the owner change and synchronize #39 with the exact commit.
