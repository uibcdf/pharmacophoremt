---
summary: Separate repeat-H chemical invariance from appended operation history.
issue: uibcdf/pharmacophoremt#39
status: resolved
opened: 2026-10-05
closed: 2026-10-09
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


## Resolution — 2026-10-09

The owner correction incorporated in
`eb50131ddbd40450c6e5eae95af7940ef80cf1f1` is reviewed and accepted. This closure
strengthens consumer guards, maintained guidance and evidence; runtime and
provider implementations are unchanged. The original text above retains its
historical publication and qualification claims.

The guard now runs under nm/ps and pm/fs and copies the original coordinates
before calling. It checks original payload, explicit original history and
original coordinates after the call, then compares the distinct returned object's
assignments and coordinates with the unchanged original/snapshot. This prevents
an equal post-call mutation of both objects from passing a preservation test.
It still requires zero new H, an empty `(0, 2)` parent map, the complete original
history prefix and exactly the unchanged terminal-attachment and hydrogen-addition
records. Actual fresh reference-EST calls preserve all 44 atoms and assignments;
returned history grows from three to five records while the original keeps three.

On normal editable Python 3.14.7, the selected hydrogen/template/input-audit run
passes 23 tests in 151.89 s; the exclusion consumer passes four tests in 50.91 s.
The six expected warnings describe B-factor drops under explicit intersection
policy. All five original hydrogen cookbook blocks execute and strict isolated
rendering passes. The audit is based on
`2132fa0ba6013b9adaf4615e1d055a1899f86cd6` plus the recorded test overlay.

`devguide/evidence/repeat_hydrogen_review_py314.json.gz` retains the actual
before/output/original-after payloads, coordinate snapshots, histories, repeated
provider reports and application captures for both unit policies. The execution
source is retained inside that archive with its own checksum. The linked
`devguide/evidence/repeat_hydrogen_review_py314_summary.json` records full-output
hashes, producer/input/native extension identities, focused commands and limits.
Seven producer Python source snapshots and recorded inputs remain unchanged
during the audit; all eighteen earlier gzip archives retain their original bytes.
The maintained contract is `devguide/eralpha_validation.md`. Report-index checks,
three offline reporting controls, Ruff, archive integrity and whitespace checks
pass before publication.

This resolves the reference-EST repeat-H consumer regression only. Environmental
hydrogen refinement remains MolSysMT #323; #22 pilot, energy, biological and
hosted/public artifact acceptance are separate. No hydrogen algorithm, chemical
state selection or provider history suppression is introduced.
