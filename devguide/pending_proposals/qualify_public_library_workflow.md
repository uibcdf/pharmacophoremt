---
summary: Qualify reproducible public-library acquisition, preparation and pharmacophore screening.
issue: uibcdf/pharmacophoremt#108
status: active
opened: 2026-11-06
closed:
verification: inspected
area: [data, screening, usability]
guard:
normative: devguide/public_library_registry.md
blocked_by: []
supersedes: []
---

# Public-library acquisition and screening

## What

The user requests both retrospective validation and new-library screening, with
powerful, friendly public-library management. The
[provider research](../public_library_support_research.md) proposes complementary
discovery, activity-reference, drug, natural-product and benchmark resources.
The [Discussions index](https://github.com/uibcdf/pharmacophoremt/discussions/109)
is the public registry; this issue owns actionable product work, separately from
#103/#66/#106's scientific source and receptor admission.

## How and ownership

Before fixing the API, the maintainer explicitly requests comparison with how
established pharmacophore tools use chemical libraries. The
[workflow survey](../pharmacophore_library_workflow_survey.md) now separates
preparation, reusable search assets, query execution, maintenance and hit triage.
It compares nine ecosystems using official documentation/source and original
papers; no competitor or new PHMT screening workflow was executed.

The reaffirmed product targets are powerful, measured capabilities, an intuitive
guided route and a coherent, detailed public API. Quality takes precedence over
a delivery deadline. A bounded iterator is one execution candidate alongside
reusable prepared/indexed assets; neither its interface nor an index format is
accepted by identifying the current memory gap. First record lifecycle/identity,
user/expert journeys, provider boundaries and acceptance experiments, then choose
a bounded implementation slice.

Qualify the journey from task/collection selection through a bounded subset,
immutable acquisition or authorized import, explicit molecular preparation,
declared pharmacophore screening, source-linked export and reproducible recovery.
Keep provider discovery/download/import/preparation/screening/availability coverage
explicit instead of assigning blanket support to a provider name.

MolSysMT owns molecular collections, formats, identity, states, conformers,
scaffolds and geometry. PHMT owns pharmacophore orchestration, screening/results
and scientific interpretation. Missing general molecular operations need an owning
provider issue and supported contract; no retired molecular reader or local
preparation fallback is recreated here.

## What is inspected and what remains

The [architecture proposal](../public_library_architecture.md) now specifies
source/prepared/search-asset/query/run identities, guided/expert operation parity,
invalidation and a single-writer journal policy. A committed terminal failure
stays authoritative in that run; retrying it creates a linked new run, while
resume handles uncommitted/interrupted work. It does not claim that current
native writers provide transactional checkpoints.

[Worked native examples](../public_library_contract_examples.md) ground that
design in explicit status/score/coverage/witness expectations. The separately
[declared control selection](../evidence/public_library_native_contract_plan_20261106.json)
checks existing native behavior; it is not an implemented iterator/journal,
public-library receiving or biological validation. The first
[incremental prepared-input prototype](../prepared_library_reference.md) now
composes the existing native tools before choosing an index strategy. Its
[separate analytical receipt](../evidence/public_library_incremental_support_20261107_summary.json)
owns the new lazy-consumption/source-mapping/evidence controls. It adds no public
API, molecular snapshot or provider receiving qualification. The separately
[declared recovery experiment](../prepared_library_recovery.md) adds a saved-query
recipe and ordered work manifest, retained attempts and single-owner SQLite
publication. It distinguishes confirmed results from generator delivery and keeps
terminal failures authoritative. Its analytical controls do not authenticate
live molecular inputs or qualify power-loss/distributed/platform durability.

The [first fixed real-structure pilot](../pubchem3d_receiving_pilot.md) now receives
three PubChem computed conformers, prepares them through public MolSysMT, verifies
native persistence and executes a declared caffeine-acceptor query with recovery.
The initial precision-keyword dispatch failure remains separate from its corrected
public-codec attempt. This is finite-file case evidence, not a managed public
connector or biological validation. The provider-owned reusable collection need is
handed to [MolSysMT #624](https://github.com/uibcdf/molsysmt/issues/624).

The dated [quantity-report correction](../pubchem3d_receiving_pilot.md#quantity-report-correction-2026-11-07-utc)
adds sealed coordinate records, five non-default-policy guards and a fresh run
of the same originals. Nine report inventories and the unchanged full native
results pass a separate read-only verification; the first post-run verifier
failure remains retained. This does not enlarge the chemical sample or qualify
the pending general collection boundary.

The [read-only inspection increment](../reference_run_inspection.md) exposes
confirmed/scored/failed/pending work and bounded observed rankings through the
same stdlib ledger. Its standalone scalar command and detailed source-only view
preserve original producer/native evidence without current molecular providers,
source access or recalculation. Historical reading of the unchanged PubChem3D
database is separate from the new analytical guards. No grouping, compound
independence, reusable index or new public API is inferred.

The [fresh/reused feature experiment](../feature_inventory_reuse.md) now compares
full native correspondence, explicit-placement and checked-pose evidence across
the same three original artifacts and two distinct acceptor references. All six
comparisons agree and the public composition recipe executes without its helper.
Only a mapping prefix is fitted in the real case; omitted work does not become
a compound negative. Fewer outer extraction requests establish no speedup or
full-search/cache/index equivalence.

The selected [public prepared-input task](../public_prepared_screening.md) is now
implemented with one runtime, exact legacy aliases, definition-owned admission
and lazy native evaluation.89 source controls and both public query/files/export
recipe blocks pass.24 distribution,3 reporting and18 archive cases also pass;
Ruff, indexes and declared dependency routes pass. Owned installed-wheel receiving
remains pending at this source checkpoint. Public recovery/results and
MolSysMT#624 collection ownership retain their separate acceptance.

At source `0925d97a7d9d219cb8caabfc1dba0ce1bee66b7f`, the ZINC downloader
calculates tranche bins but performs no HTTP acquisition; virtual screening
materializes its full input iterable. Prepared-native evaluators do not constitute
a qualified arbitrary-public-library workflow. The research records official
provider documentation and access limitations, not acquisition/preparation evidence.

The registry records proposed priorities and initial assessments for 17 resources.
No provider is qualified for blanket managed-library support. The three-record
PubChem3D case has only its explicitly measured receiving/import/scoring scope.
DrugBank's automatic-acquisition route is deferred
under the observed download pause, with a specific revisit trigger. Enamine's
applicable agreement/access requirements remain an explicit assessment item.
The registry research did not download or prepare a chemical dataset or run a
screening score. Native and incremental analytical fixture controls are separately
declared executions, not screening of a newly acquired public collection.

## Alternatives and limits

Do not equate a public page with unrestricted computational use or redistribution,
an SDF with a prepared conformer ensemble, a catalog snapshot with current stock,
or a generated decoy with a measured inactive. Do not turn failed preparation into
a negative score. Provider priorities remain proposals, not release commitments.

## Acceptance criteria

1. Maintain the category, public index, source-specific records, intake template
   and dated dispositions under the [registry guidance](../public_library_registry.md).
2. Select a bounded first provider/subset with explicit data rights, original IDs,
   actual access, molecular preparation requirements and immutable manifest.
3. Qualify acquisition/import, replay and interrupted recovery with original-byte
   hashes and transparent rate-limit/failure accounting.
4. Receive supported molecular-provider contracts; retain record → molecule →
   state → conformer correspondence through bounded incremental screening.
5. Demonstrate source-linked hit export and reproducible run recovery. Preserve
   negatives, unsupported inputs and failures, with actual denominators.
6. Keep retrospective endpoints, grouping/leakage, splits and prospective-library
   claims separately qualified; registry delivery does not complete #103.

The first implementation provider and release scope remain to be selected from
the evidence. Future bounded integrations can use linked issues when accepted.
