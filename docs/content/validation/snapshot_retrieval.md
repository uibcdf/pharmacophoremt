# Candidate retrieval from original feature snapshots

This analytical case, owned by LMMV/dprada under
[issue181](https://github.com/uibcdf/pharmacophoremt/issues/181), connects the
[native snapshot study](feature_snapshots.md) to the existing
[finite retrieval prototype](retrieval_controls.md). It checks complete original
correspondences and traceability. The composition remains unshipped; no stable
public index or performance result is introduced.

## Frozen inputs and independent controls

The [declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/snapshot_retrieval/declaration.json)
and [originals manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/snapshot_retrieval/originals.json)
receive all 16 unchanged source/owned snapshots from the earlier hash-qualified
archive. These are project-created analytical fixtures, with no external chemical
database or activity labels. No molecular preparation or feature extraction is
repeated. Original native units, recognition, attribution and producer labels
remain intact; source trust remains a declared precondition, not authentication.

Each context contains nine ordered work occurrences: its eight original nm/pm
captures plus an explicit repeated capture. Work keys and positions are kept
separately from the recorded parent source/occurrence names. In particular,
`nm`, `1 nm` and `repeat=α` remain literal identifiers.

| Original work positions | Native features | Treatment |
| --- | --- | --- |
| 1, 4, 5 | Three signed charge centers each; positions 1/5 share snapshot bytes | Index all three work occurrences, retaining their distinct positions |
| 0, 7 | Complete explicitly requested empty aromatic family | Retain empty coverage and evaluate the full-query reference |
| 2, 6 | Two donors sharing a center with distinct hydrogen maps/directions | Retain full evidence and evaluate the full-query reference |
| 3, 8 | One six-atom aromatic feature with an unoriented normal | Retain full evidence and evaluate the full-query reference |

Positions are zero-based. The six shorter inputs cannot supply a complete
three-feature mapping in this declared proposal family. Their absence of such
proposals does not mean biological inactivity or failure of a smaller query.
The index's compact positions 0/1/2 must map back to originals 1/4/5.

Four explicit mathematical three-point queries cover identity, a slightly
perturbed anchor, a shared-anchor geometric impossibility and a wrong-kind
negative. They are test hypotheses, not new molecular states. Widths are
0.125/0.5/1 angstrom, with public PyUnitWizard conversion to explicit angstrom
coordinates. An independent rational permutation oracle checks every original
inventory against the public native association reference. Candidate lookup
then calls that same reference on the shortlisted original inventories.

## Executed results — 2026-11-10 UTC

The [receipt and full original archive](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/snapshot_retrieval_20261110.json)
receive 41 passing guards per source/exact-owned218 context: 28 new ingestion
controls and 13 existing retrieval controls. Each context completes 24 rows over
four queries, three widths and two application unit policies, nm/pm. All complete
original work/feature/atom mappings agree with exhaustive native evaluation;
72 independent rational comparisons pass per context.

Each policy evaluates 36 exhaustive reference cases, then nine retrieved cases
per width, 27 across all three widths. Each context therefore makes 72 exhaustive
and 54 retrieved calls, 126 in total. Every asset contains nine pair entries.
These are workload counts; build/query timing, storage cost and memory efficiency
are not measured.

The deliberately unsafe exact-bin lookup misses original 4 at width 1 and all three
eligible originals at width 0.125. The first guard incorrectly required all three
misses at width 1. The preserved six-row diagnosis explains the difference:
original nm centers convert to 5.0 angstrom, while the pm capture converts to
4.999999999999999 angstrom. The corrected assertion keeps those original operands;
queries, tolerances, widths and conservative-reference expectations are unchanged.
Original first evidence has 35 passes/6 setup errors from that one postcondition;
it is not relabeled as a completed result.

The conservative lookup retains all declared positives. The shared-anchor
impossibility is shortlisted and rejected by the native reference. A candidate
prefix keeps pending original positions 4/5 and unknown unsearched work; it does
not become a complete negative result. Changed original byte/work bindings,
including unindexed donor direction, coverage or producer changes, refuse stale
reuse even when projected centers and counts stay equal.

No molecular operation is observed. Original reading/reconstruction creates no
new original-workflow credit. Each actual new reference workflow retains eight
references/eight uses; full original nested attribution stays separate as saved
data. A fresh process reads both original reports with scientific imports blocked
and refuses both existing output destinations before importing science.

## Reproduce and maintain

The [unshipped driver](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/qualify_snapshot_retrieval.py)
and [focused guards](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/test_snapshot_retrieval_ingestion.py)
use the same frozen originals. The
[receiving contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/snapshot_retrieval_ingestion.md)
records exact source/provider/native/fixture identities, original failures,
explicit units and resource controls. Prepare an admitted compatible environment,
apply shared-workstation limits and choose an unused destination:

```bash
python -m pytest --receptor=llm tests/test_snapshot_retrieval_ingestion.py \
  tests/test_retrieval_control_oracles.py
python -m devtools.qualify_snapshot_retrieval --output retrieval-result.json \
  --snapshot-context source --admission-sha256 YOUR_FROZEN_CONTEXT_SHA256
```

The received route uses Python 3.14/one CPU/backend thread and unchanged
owned 0.4.0+218.g5515e93. All 214 wheel payloads, 159 runtime bodies, 4594 provider Python
files, native identity and 30 case files verify. Source/installed origins are
144 PHMT modules for selected guards and 146 for the complete driver. Changes to
snapshots, projection, identity binding, numerical/reference operations or
independent expectations need a new run and retained original evidence.

This finite experiment does not qualify final fitting/orientation/activity,
universal floating-point recall, arbitrary runtime compatibility, generic
molecular collections, public API/index promotion, human usability or supported
installed-platform/release delivery. Wider feature/numerical and equivalent-cost
receiving remain open. MolSysMT#624 retains collection/lifetime ownership and
resource-stopped measurements #148/#165 are not retried.
