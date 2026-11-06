# How pharmacophore tools use chemical libraries — 2026-11-06

Owners LMMV/dprada; product destination
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108). This survey complements
the [provider catalog research](public_library_support_research.md): it studies
how existing pharmacophore tools turn libraries into usable screening workflows.
The user explicitly requests this comparison before public-API design and
reaffirms powerful capabilities, measured performance, intuitive use, a deep
coherent public API and careful work without a deadline-driven shortcut.

The user also requests a separate [tool-study registry](pharmacophore_tools_registry.md)
under [#128](https://github.com/uibcdf/pharmacophoremt/issues/128), with records for
what to study, learn and compare. That registry retains open questions and
evidence levels beyond this first library-workflow survey.

## Scope and evidence method

Compare toolkits, local screening engines and integrated products without treating
them as interchangeable. Use official documentation, source repositories and
original publications. Separate documented behavior, historically published
methods and our proposed design implications. An unavailable document or an
undocumented capability is an evidence gap, not proof that a tool lacks it.
No competitor has been installed, benchmarked or executed in this survey.

Trace the full workflow: library acquisition/import; identifiers and compound,
state/conformer grouping; preparation; feature annotation; persistent indexing;
query and filters; match/pose/compound ranking; inspection/export; updates and
run recovery. Assess simple-user and expert-user routes separately. Preserve the
distinction between a library of compounds and a library of pharmacophore models.

The initial incremental-screening sketch remains a candidate. Public method
names, return schemas, batching and index formats are not accepted by this note.
Implementation and a tiny PubChem technical demonstration wait for this comparison
and the ensuing bounded design decision. No new chemical download, preparation,
pharmacophore, score or streaming runtime change has been executed here.

## Comparison by role

| Ecosystem and source scope | How it uses chemical libraries | Transferable lesson and evidence limit |
| --- | --- | --- |
| **Pharmit / Pharmer**: hosted workflow and indexed engine | Named supplied/user libraries, stored conformers and pharmacophore/shape indexes; interactive queries, filters, aligned hits and session export | Prepare/search lifecycles and indexes are first-class concerns. Web convenience depends on substantial preparation/storage infrastructure. [Current help](https://pharmit.csb.pitt.edu/help.html), [original Pharmit publication](https://pmc.ncbi.nlm.nih.gov/articles/PMC4987880/), [Pharmer method](https://pmc.ncbi.nlm.nih.gov/articles/PMC3124593/). |
| **CDPKit 1.3.0**: toolkit and command-line applications | Separate conformer generation, screening-database creation, screening, inspection and merge/update applications | Strong separation of reusable artifacts and operations; explicit selection of first/best/all matches and export identifiers. Current names are `psdcreate`/`psdscreen`, not assumed historical names. [Applications](https://cdpkit.org/applications/index.html), [screening](https://cdpkit.org/applications/psdscreen.html). |
| **LigandScout**: integrated commercial workflow | iCon-based preparation, optimized multi-conformer `.ldb` databases, visual queries, ranked hit inspection; local CLI and remote chunked jobs | A short guided route can coexist with detailed preparation/search controls. Current 4.5/XT pages and older CLI/tutorial documents have different evidence scope. [Product](https://www.inteligand.com/products/ligandscout/), [library generation](https://www.inteligand.com/solutions/library-generation/). |
| **Schrödinger Phase**: commercial prepared-database workflow | Import/manage, state/conformer/site generation, reusable database search, property subsets and export | Distinguish source records, prepared variants and search artifacts; document attrition and restart support per operation. [Product](https://www.schrodinger.com/platform/products/phase/), [dated pipeline implementation](https://learn.schrodinger.com/public/python_api/2022-2/_modules/schrodinger/pipeline/stages/phase.html). |
| **RDKit Pharm3D**: algorithmic building blocks | Feature matching, bounds checks, pharmacophore-constrained embedding and optimization per molecule; molecular suppliers and general conformer generation are separate APIs | A chemistry toolkit does not by itself supply collection lifecycle, provenance and run management. [Pharm3D](https://www.rdkit.org/docs/source/rdkit.Chem.Pharm3D.EmbedLib.html), [molecular suppliers](https://www.rdkit.org/docs/GettingStartedInPython.html). |
| **Historical OpenPharmacophore**: lightweight Python screening facade | In-memory/file-backed collections and an approachable define-query → screen → inspect aligned hits route | Learn from the short journey, while qualifying iteration/reuse, diagnostics and distinct failure stages. The inspected historical documentation is not current product qualification. [Collection source](https://www.uibcdf.org/OpenPharmacophore/_modules/openpharmacophore/screening/mol_db.html), [screening source](https://www.uibcdf.org/OpenPharmacophore/_modules/openpharmacophore/screening/screening.html). |
| **Align-it / Pharao family**: alignment tool and Python-wrapper fork | Pharmacophore-based alignment with separate CLI/Python examples | Useful as a narrow alignment component, with a much thinner verified library-management story in this review. The fork explicitly warns of experimental wrappers and possible differences from the original. [Author-maintained fork](https://github.com/OliverBScott/align-it), [examples](https://github.com/OliverBScott/align-it/tree/main/example). |
| **BIOVIA Discovery Studio / Catalyst**: integrated commercial platform | Library design/filtering and state enumeration; reusable 3D-conformation databases; multiple mappings and compound-level fit selection | Include preparation, query execution and hit triage in the product model. Public vendor descriptions establish advertised behavior, not measured completeness or speed. [Current product description](https://www.3ds.com/products/biovia/discovery-studio/ligand-and-pharmacophore-based-design), [2025 datasheet](https://www.3ds.com/assets/invest/2023-10/biovia-discovery-studio-overview.pdf). |
| **MOE**: integrated commercial platform | Conformation databases, pharmacophore/shape constraints, preparation and a database viewer with interactive property filters | Preparation, searchable data and inspection need a coherent user journey. The reviewed public material does not establish current low-level index or restart contracts. [Product capabilities](https://www.chemcomp.com/en/Products.htm), [versioned 2024.06 release notes](https://www.chemcomp.com/release_notes/moe202406/rnotes.htm). |

This is a workflow comparison, not a ranking of scientific quality or performance.
No inference of equal feature definitions, conformer coverage, query semantics or
score scale follows from similar product terminology.

## Preparation and library-building practices worth examining

**Pharmit distinguishes supplied geometry from generated geometry.** Its 2016
publication describes preparing SMILES, retaining a main component, protonation,
deduplication and generated conformers, while treating uploaded SDF geometry as
provided conformations. Those publication-era choices must not be assumed to be
current deployed defaults. The inspected `createconfs.py` source uses a different
conformer-count default from the paper, supports energy/RMSD filtering and reuses
prepared files. Its structure/name tables separate canonical structures from
aliases, but the examined table does not establish a preparation-preset/version
identity. Our inference is to record the actual effective preparation and cache
identity rather than infer it from a source SMILES or an unversioned preset name.
[Preparation source](https://github.com/dkoes/pharmit/blob/master/scripts/createconfs.py),
[storage schema](https://github.com/dkoes/pharmit/blob/master/scripts/conformers.sql).
The inspected file blobs were respectively
`60bd3df80819855cb445bb83a11ef359d61ddd85` and
`ea6d92020353d70a3eea8b7f8b6d460e56b39a9d`; these identify source files,
not an installed release or a complete frozen deployment.

**CDPKit makes several molecular policies explicit.** `confgen` exposes sampling
mode, named diversity/density presets, energy/RMSD limits, output-conformer limits,
source-coordinate use and failed-molecule output. `isogen` separately controls
stereoisomer enumeration and treatment of specified/source stereochemistry;
`tautgen` handles tautomer generation/standardization. These operations are not
synonyms for importing an SD file or constructing a search index. In PHMT's
architecture, their reusable molecular equivalents belong in MolSysMT.
[Conformer generation](https://cdpkit.org/applications/confgen.html),
[stereoisomers](https://cdpkit.org/applications/isogen.html),
[tautomers](https://cdpkit.org/applications/tautgen.html).

**LigandScout makes library building a visible user action.** Its public CLI
summary describes `idbgen` producing `.ldb` databases and `iconfgen` producing
multi-conformer SDF. Current pages describe iCon and tautomer-generation tools;
older tutorial cards demonstrate a preparation preset, loading the resulting
library, screening and inspecting hits. The detailed current default state/stereo
policies were not established from the public material reviewed. Preserve that
uncertainty rather than treating a named fast preset as a reproducible universal
chemical policy. [CLI document, 4.4 and later](https://www.inteligand.com/download/LigandScout_4_Command_Line_Tools.pdf),
[official 4.2 tutorial cards](https://www.inteligand.com/download/LigandScout-4.2-Tutorial-Cards.pdf),
[current manual entry](https://docs.inteligand.com/ligandscout/usage/).

**Phase publishes useful preparation provenance.** Its 2024Q1 MolPort report
identifies source input, preparation commands, stereochemical/tautomeric/charged
variants, conformers/sites/fingerprints, property subsets and update cadence.
It distinguishes input records from property-calculable structures and prepared
3D variants, including attrition. Property-based categorization uses a specified
representation and precedence among overlapping categories. These are useful
patterns for manifests and accounting, not defaults to transplant into PHMT.
[Official preparation report](https://www.schrodinger.com/wp-content/uploads/2024/04/2024q1_molport_report.pdf).

**Toolkits require orchestration.** RDKit documents streaming/compressed SDF
suppliers, malformed-record checks and multithreaded suppliers that can change
return order. Its general conformer-generation configuration is separate from
Pharm3D, whose embedding API distinguishes attempts, generated embeddings and
failures. PHMT should consume molecular capabilities through MolSysMT while
retaining their declared method and source identity.
[Suppliers](https://www.rdkit.org/docs/GettingStartedInPython.html),
[conformer-generation cookbook](https://www.rdkit.org/docs/Cookbook.html?highlight=etkdg).

The historical OpenPharmacophore adapters create ligand objects during iteration;
the examined file-backed path closes consumed source files. Its screener retains
aligned matches in memory and combines different unsuccessful outcomes in a
failure counter, with global RDKit logging disabled in that module. These source
observations motivate testing repeat queries, separating failure stages and
keeping diagnostics available. They do not imply that every historical route
has the same behavior. [Official historical tutorial](https://www.uibcdf.org/OpenPharmacophore/contents/examples/virtual-screening/screening.html).

## Indexing, search semantics and result handling

**An index is a separate engineering/scientific asset.** The original Pharmer
method precomputes pharmacophore-triplet indexes and uses additional fingerprints
before final alignment. Its historical benchmarks show substantial index storage
beyond source conformer files. This supports investigating reusable indexing;
it does not predict PHMT latency or establish that any indexed engine has
identical feature/matching semantics. The local Pharmit server additionally
separates feature extraction, database construction, search and serving, with
partitioning/storage and operating-system limits that matter to operators.
[Pharmer original method](https://pmc.ncbi.nlm.nih.gov/articles/PMC3124593/),
[server operation/source](https://github.com/dkoes/pharmit/blob/master/README.md).

**CDPKit exposes search and provenance choices.** `psdcreate` supports source
ranges, compressed files, CREATE/APPEND/UPDATE and optional duplicate dropping;
source-file annotation is optional. `psdscreen` distinguishes first, best and all
matches, omitted-feature/exclusion policies, aligned hits and optional database/
molecule/conformer/query identifiers in exports. Several provenance fields are
off by default. These are useful expert controls, but our proposed manifest/result
policy should make lineage dependable rather than optional. `psdinfo` and
`psdmerge` make inventory and maintenance separate operations. Exact duplicate/
replacement semantics still need inspection before adoption as a scientific
identity policy. [Creation](https://cdpkit.org/applications/psdcreate.html),
[screening](https://cdpkit.org/applications/psdscreen.html),
[inventory](https://cdpkit.org/applications/psdinfo.html),
[merge/update](https://cdpkit.org/applications/psdmerge.html).

**Limits can change which answer is returned.** Pharmit help distinguishes limits
on configurations, molecules and total results, and documents sorting, alternative
identifiers, SDF export and sessions. A greedy first-configuration limit is not
the same as selecting globally best molecules after ranking. Optional receptor
minimization introduces another score and displacement filter. Preserve these
stages explicitly instead of calling every number a pharmacophore score.
[Current help](https://pharmit.csb.pitt.edu/help.html).

**Maintenance and recovery require explicit semantics.** The dated Phase pipeline
separates creation/append, optional duplicate handling, grouping by titles or
stereochemical connectivity, existing versus new conformers, sites-only work and
export. Later public API pages document restartable stages and task-specific
restart support. LigandScout Remote supports database chunks and subjobs, with
recovery of failed/cancelled subjobs documented in its history. None of this
establishes a universal byte-range downloader or arbitrary-operation resume
contract. [Phase pipeline](https://learn.schrodinger.com/public/python_api/2022-2/_modules/schrodinger/pipeline/stages/phase.html),
[Phase stage API](https://learn.schrodinger.com/public/python_api/2024-1/api/schrodinger.pipeline.stages.phase.html),
[Phase job utility](https://learn.schrodinger.com/public/python_api/2024-4/api/schrodinger.application.phase.packages.phase_database_job_utils.html),
[LigandScout Remote configuration](https://docs.inteligand.com/ls-remote/server-configuration/),
[Remote version/recovery history](https://docs.inteligand.com/ls-remote/version-dependencies/).

**Hit triage matters as much as starting a search.** LigandScout's current pages
and older tutorials expose ranked hits, multiple queries/databases, visual
inspection, property filters and export; model combinations can include target
and anti-target logic. Discovery Studio describes selecting fits across multiple
mappings/pharmacophores and property/diversity filtering. MOE's 2024.06 notes
document interactive filters with visible included/excluded subsets and a policy
for empty/non-finite values. These are useful workflow references, not evidence
that their scores, constraints or filters are interchangeable.

## Important limits of the comparison

- Reviewed tools often start with local/supplied molecular files or prepared
  databases. The examined pages do not establish universal direct acquisition,
  source-version management or unrestricted use of every public catalog. Our
  provider research and receiving qualification remain a distinct requirement.
- A compound library and a pharmacophore-model library serve different directions
  of screening. LigandScout's licensed **IL PharmDB** and BIOVIA's **PharmaDB**
  describe model/profile resources; they must not be counted as ordinary supplier
  compound catalogs. [IL PharmDB](https://www.inteligand.com/products/pharmacophoredb/).
- Billion-scale product language is not a measured local capability. LigandScout
  XT advertises very large workflows; Schrödinger's current prepared-library
  compatibility table assigns some enormous virtual spaces to other engines,
  rather than Phase. Do not transfer platform-wide scale claims to an individual
  pharmacophore method. [LigandScout XT](https://www.inteligand.com/products/ligandscout-xt/),
  [prepared-library compatibility](https://www.schrodinger.com/platform/products/prepared-commercial-compound-library/).
- Current product pages, dated manuals/API code and original papers carry
  different authority. In particular, the reviewed CDPKit manual is 1.3.0;
  LigandScout sources span current product pages and 4.2/4.4-era documents;
  Phase's public implementation/API examples span 2022–2024. No installed-current
  binary or deployment was qualified.
  The inspected OpenPharmacophore documentation identifies the historical
  development revision `0+untagged.471.gea8c857`, not a newly qualified release.
- Some documents were inaccessible: Align-it's linked original manual timed out;
  detailed MOE routes and its auxiliary-database route could not be read; the
  full current Phase documentation required authentication in the agent review.
  These are bounded access observations, not product/service absence claims.
- Software and chemical-data licensing are separate. RDKit states BSD-3-Clause,
  historical OpenPharmacophore MIT, CDPKit LGPL-2.1-or-later, and the inspected
  Align-it fork GPL-3.0. Pharmit's README/license files have differing descriptions;
  do not assert one permissive license for the whole integration. Commercial
  products have their own licensing routes. No code adoption, redistribution
  conclusion, account registration or license purchase follows from this survey.
  [RDKit license](https://raw.githubusercontent.com/rdkit/rdkit/master/license.txt),
  [OpenPharmacophore repository](https://github.com/uibcdf/openpharmacophore),
  [CDPKit introduction/licensing](https://cdpkit.org/introduction.html),
  [Pharmit license files](https://github.com/dkoes/pharmit),
  [LigandScout licensing](https://docs.inteligand.com/ligandscout/),
  [Schrödinger agreement](https://www.schrodinger.com/eula/).

## Proposed PHMT structure: learn from the lifecycle before naming the API

The following are design inferences and alternatives to evaluate, not frozen
public classes, methods, formats or release promises.

| Concept to keep distinct | Information the user/API needs | Owning boundary |
| --- | --- | --- |
| Source collection and selection | Provider/release/terms, original identifiers, exact subset/filter, original bytes and exclusions | PHMT collection experience and receiving provenance; reusable molecular acquisition/collection tools in their provider |
| Prepared molecular collection | Record → molecule → state → conformer mapping, explicit preparation and omissions, versions/parameters and immutable identity | MolSysMT molecular operations; PHMT records the chosen preparation contract and eligibility |
| Pharmacophore annotations/search asset | Feature definitions, supported constraints, coordinate/unit/frame policy, preparation identity, index/build identity and rebuild condition | PHMT owns pharmacophore semantics/search artifacts; reusable chemistry/geometry remains MolSysMT-owned |
| Screening run | Frozen query, search strategy, finite budgets, filters, completeness, checkpoints, per-input outcomes and actual resource use | PHMT screening/orchestration and scientific interpretation |
| Compound and pose results | Declared aggregation, matched features/transformations, source state/conformer/query, score meaning, valid negatives/failures and export provenance | PHMT result contracts; molecular serialization through MolSysMT |

Source-catalog discovery, receiving, preparation, indexing, screening and live
availability should have individual coverage claims. A successfully downloaded
SDF is not a prepared searchable library; an index valid for one feature definition
is not automatically valid after that definition changes.

For a casual user, evaluate a short route: choose a public source, import an
authorized local file, or reopen an existing prepared collection; inspect expected
coverage/cost, choose an explicit preset, screen, inspect grouped hits and export.
Offer a small preview with original/eligible/state/conformer counts, failures,
unknowns and required preparation/index rebuilds before expensive work. Show
progress and a useful recovery action if a stage fails. Preserve source identifiers
and current-stock check dates in exported hits.

Define visible lifecycle states for pending work, preparation, indexing, searchable
assets, failures, stale assets and superseded snapshots. Specify what remains
usable while a refresh or rebuild is pending or fails. Preserve the prior immutable
asset until the replacement has met its declared acceptance checks. These are
proposed lifecycle requirements; the surveyed builders do not by themselves prove
transactional or reproducible updates.

For expert users, expose the same underlying operations as documented composable
public tools. Allow inspection of resolved preset parameters, preparation policy,
feature inventory, constraints, candidate filtering, search budgets, score and
aggregation rules. Save/replay those choices. Keep data objects and results
inspectable without requiring private modules. A small high-level surface should
not introduce a second scientific implementation with different defaults.
Separate portable manifests/settings/results from live molecular objects, file
handles and lazy readers. Both need supported public access, while their owning
serialization contracts determine what can actually be persisted/replayed.

## Execution strategies that need a measured decision

| Candidate | Appropriate question | Costs and scientific obligations |
| --- | --- | --- |
| Incremental scan over prepared inputs | Small/one-off collections, strict RAM limits, reference calculations, heterogeneous provider inputs | Low additional persistent storage; full repeated scan cost. Preserve global identity, lazy consumption, per-input/per-frame failures and incremental output. This alone does not provide indexed large-library latency. |
| Reusable prepared feature/index asset | Many queries against stable medium/large collections | Preparation/build time, disk footprint, schema/version/invalidation and update policy. Validate any prescreen against the declared final matcher; document false-negative/completeness limits. |
| Hybrid filtering/index followed by exact native evaluation | Reduce expensive matching after cheap declared selection | Separate user filters, candidate generation and final scoring; verify admissibility/equivalence for supported queries and preserve the relevant denominators. |
| Optional delegated screening engine | Reuse a qualified external index or special execution capability | Feature/constraint/score/identity translation, installation/license and reproducibility need an explicit adapter contract. No automatic equivalence or new engine dependency is accepted here. |

A bounded iterator can remain useful as the reference/low-memory path, but choosing
its public schema before the broader lifecycle would leave preparation artifacts,
repeat-query costs, indexing and maintenance unresolved. An index is not a reason
to duplicate molecular perception or geometry inside PHMT. Hardware acceleration,
parallelism and distribution require evidence of a bottleneck and equivalent
answers before expanding the execution model.

## Proposed acceptance experiments

| Area | Evidence before choosing/freezing behavior |
| --- | --- |
| Intake and identity | Repeated supplier records, malformed/missing structures, undefined stereochemistry, states/conformers and multiple aliases preserve all original mappings and explicit omissions. |
| Preparation | Existing prepared 3D and provider-generated variants have distinct explicit policies; presets resolve to saved parameters and methods. Every stage reports input/retained/failed counts. |
| Search semantics | Known analytical positive/negative/failure cases, feature/shape exclusions, units and proper frame changes; first/best/all results and truncation/aggregation have independently known answers. |
| Index correctness | For supported feature/constraint domains, compare candidates/results against the declared native reference; test build identity, feature-definition changes, corruption and supported updates. Do not call a lossy prescreen exact. |
| Recovery and reuse | A second query works on the same immutable prepared collection; interruption preserves completed outcomes without duplicating/skipping records. Resume rejects a mismatched query/preparation/index identity. A failed refresh preserves the last qualified snapshot and exposes stale/superseded states. |
| Friendly workflow | A user can select/preview/screen/inspect/export without private APIs, understand an unsupported input/failure, and retrieve effective settings for reproduction. |
| Expert API | Public operations compose consistently; portable settings/results/identities and live provider handles have distinct supported contracts. Guided and composed routes resolve to the same effective settings and equivalent declared answers. |
| Performance | Report receiving, preparation, build time/disk, cold/warm query latency, throughput, peak memory and serialization separately, at declared molecule/state/conformer/query counts. Include unselective queries and no-hit cases. |
| Predictive utility | Use scientifically admitted measured endpoints, grouping/splits, simple comparators, uncertainty and honest negative results. Throughput and geometric exactness do not establish biological predictive power. |

For repeated queries, evaluate total cost as preparation + index construction +
all query/inspection/export costs, rather than reporting query latency alone.
Freeze the comparison population, prepared geometries/coverage, feature definitions,
constraints, budgets, stopping rules and hardware/environment. If compared tools
cannot express the same problem, report the difference instead of manufacturing
a common score or interpreting missing results as negatives.

These experiments are proposed, not run. Shared-host resource limits and existing
scientific source/exposure admission remain in force; no large library or benchmark
is scheduled merely because a product advertises it.

## Current PHMT gap and the next design decision

Current `VirtualScreening.run()` materializes inputs and retains ranked hits and
all evaluations. The shared native batch helper also accumulates results. Prepared
native evaluators already expose explicit constraints, finite searches and
negative/failure distinctions, but PHMT has no newly qualified prepared-library
index or public-provider lifecycle in this work. The ZINC downloader remains a
stub. [Facade](../pharmacophoremt/screening/virtual_screening.py),
[batch helper](../pharmacophoremt/_private/pose_batch.py),
[ZINC source](../pharmacophoremt/data/zinc.py).

The immediate design record should specify the identities/lifecycle, high-level
journey and expert operations, with two candidate execution strategies: bounded
prepared-input scanning and a reusable search asset. Choose a first implementation
slice only after that record names ownership, supported molecular-provider
contracts, representative workloads and acceptance checks. The three-compound
PubChem example considered earlier could become a technical smoke case after its
own declaration; it cannot select an index strategy or establish predictive/large-
library performance.

The user accepts the product ambition and careful evidence-led development. The
particular API, index structure, engine, default preparation/conformer policy and
first provider/subset remain design decisions to make from this comparison.
