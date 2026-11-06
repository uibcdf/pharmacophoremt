# Current development checkpoint

Maintained 2026-11-06 for the machine-migration handoff, owners LMMV/dprada.
Start with [onboarding](onboarding.md), [decisions/workstreams](decisions_and_workstreams.md)
and [migration](machine_migration.md). The former long log is preserved verbatim
after its preface in [checkpoint history](checkpoint_history_20261106.md).
This page is current; old dated "Next" paragraphs are historical observations.

## Where we are

The library has native prepared/cached ligand-, interaction-, complex- and
receptor-based workflows, finite rigid search, pose/conformer screening, metrics
and native persistence. [Capability inventory](capability_inventory.md) names
actual routes/controls and limits. These analytical/preparation deliveries do
not establish predictive accuracy. Neither complete receptor-based biological
study under #103 has executed.

Actual release plan/latest GitHub Release remains **0.4.0**. Proposed0.5.0 is
reviewed, not frozen/published. This handoff changes documentation/evidence and
the reporting inventory, not runtime, molecular inputs, dependencies or workflows.
The addon remains deferred; its source exists but live-browser acceptance is #58.

| Workstream | Current evidence | Next action |
| --- | --- | --- |
| #103 two receptor studies | Preparation/analytical controls exist; no full admitted biological study | Complete source/cohort/preparation admission, freeze the full comparison/evaluation plan, then execute |
| #66 ERalpha | Original Sun2006/Xin2023/Gungor2006/Scott2023 methods remain unresolved; original pools/thresholds/exposure retained | New authorized access lead; don't repeat exhausted routes or silently substitute a source |
| #106 BRD4 admission | Complete1,780-AID census;53 incompatible/nine isolated-BD1 leads/19 unresolved among81 survivors; no accepted cohort | Resume only the published single-AID label-capacity plan after environment/custody checks |
| MolSysMT | #105 native aromatic-N received; #323/#375/#447 remain open at this handoff | Consume supported H-refinement/carboxylate/grouping contracts; report actual missing general tools there |
| #95/#10/#23 | Proposed intermediate release and separate public/installed/support gates remain partial | Qualify actual public provider capabilities and exact candidate/source/file/platform gates before freeze |
| #9 | Narrow local controls do not clear the full source backlog | Inspect exact hosted run/attempt IDs; retain failures/skips/pending evidence |
| #6/#41/#74 | Broader support adoption and bounded molecular/annotated-SDF migration debt remain | Use owning provider contracts; don't expand historical local compatibility code |

## What was in progress when development moved

[BRD4 capacity receiving](receptor_study2_capacity_receiving.md) stops the earlier
11 pending sources for this design: each has at most9 SIDs. AID1805333 is the
largest explicit isolated-BD1 method lead, with499 raw SIDs/494 CIDs; those counts
are not independent molecules or class balance.

The [original-method review](receptor_study2_primary_method.md) and
[receipt](evidence/brd4_primary_method_20261106_summary.json) now retain the actual
patent binding method, separate BRD4/cellular Table24 columns, source interval
legend and unchanged PubChem version3/revision2 descriptors. Incorporated human
construct information is documented, while exact transfer to the patent remains
an inference. No molecular sequence mapping, receptor preparation or score ran.

The [prospective activity-capacity plan](evidence/brd4_activity_capacity_plan_20261106.json)
is preserved for publication in this handoff before dedicated activities. **No dedicated activity
table or class-frequency projection has been received/executed.** Strong means
IC50≤0.5 micromolar, weak means IC50>5 micromolar under this assay, with complete
censoring intervals and50 eligible SID upper bounds/class. Intermediate, ambiguous,
invalid, missing and conflicting outcomes must remain explicit.

After publication and deliberate scientific resumption, receive the single CSV
between the declared before/after metadata checks. If either eligible class is
too small, record the source/design stop without pooling, threshold changes or
favorable replacements. If raw capacity passes, full material/interference/rights/
exposure and MolSysMT identity/state/series/grouping admission still precede
cohort/receptor/model selection and scores. Current raw-source prose is private;
source-curation/license version needs resolution before raw-row redistribution.
Earlier ERalpha/exposure ledgers remain intact; no unseen-holdout claim is made.

## Evidence and execution that must not be overstated

#105's original250 unique selected controls and #102's corrected111-control
selection retain their exact producers. The earlier complete hosted old-head
source run had2,071 passes/two failures; the two envelope-oracle failures were
subsequently repaired, but selected repair controls are not a full current suite.
The later local full attempt stopped at its1GiB cap after1,428 passing reports.
Do not launch a larger whole-suite retry on this shared machine.

The public MolSysMT0.23.0 receiving record has203 selected passes and18 capability
skips, not modern-provider or full installed/public qualification. Controlled
source MolSysMT0faf1584 is distinct from the preserved sibling checkout71fbe4f.
The historical controlled prefix/SDK/native binary are now absent; reconstruct
their declared sources/environment and record fresh native/import receiving.

For source head7395ad004dc08c0442572a12f3e952d59c5fdec4, the latest migration
observation records CI42197647509 still queued; policy42197647866 and publication
governance42197647985 succeeded. This is not a complete source-matrix pass.
The final documentation head's exact observation belongs in #9/#107; consult
those run/attempt records rather than restarting old work because a poll expires.

## Receiving the new machine

All59 declared support files are tracked/hash-correct. Tracked evidence archives
are portable; ignored raw papers/controllers/environments are not supplied by a
clone. [Migration inventory/checklist](machine_migration.md) marks available BRD4
capsules, absent old #66/controlled-source roots and reconstruction authority.
Do not overwrite old receipt paths/hashes or copy credentials/native binaries.

Use Python3.14, the exact SDK/selected dependency context, `pip check`, import/
native identities and scoped checks from onboarding. Heavy work remains serial,
one actual allowed CPU/backend thread, low priority and512MiB/no swap where
enforceable. Old method-review phases had a one-CPU quota but CPUs0–19 affinity;
preserve that fact. Use explicit taskset and verify affinity on subsequent Linux
checks; CPU19 is historical, not a destination requirement.

The destination environment and scientific compatibility have not been executed
by this handoff. There is no running local scientific task to resume. Rehydrate
the selected context first, then choose the next owned task explicitly.
