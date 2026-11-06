# Public chemical libraries: screening support priorities — 2026-11-06

Owners LMMV/dprada; product work [#108](https://github.com/uibcdf/pharmacophoremt/issues/108)
and the [public registry](https://github.com/uibcdf/pharmacophoremt/discussions/109);
related scientific work [#103](https://github.com/uibcdf/pharmacophoremt/issues/103),
[#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
[data ownership](../MOLSYSSUITE_GUIDE.md#component-responsibility-map).
The user explicitly requests both retrospective validation and new-library
screening, with powerful, friendly public-library management. This note records
primary-source research and proposed implementation priorities. It does not
claim working provider integrations, downloaded libraries, accepted cohorts,
executed new screening, a frozen public API or a release commitment.

## Recommendation by scientific use

Support several complementary provider families through one consistent workflow.
Discovery catalogs, bioactivity references, approved-drug collections, natural
products and evaluation benchmarks serve different purposes. A compound count
or a convenient API is insufficient to rank their scientific value.

| Priority / resource | User value | Verified access and preparation boundary |
| --- | --- | --- |
| Core discovery: **ZINC-22 / ZINC20** | Catalog-oriented discovery, purchasable/synthesizable subsets, chemical-space selection and prepared structures where available | Official documentation describes tranche selection and 2D/3D routes. Preserve ZINC IDs, supplier/catalog mapping, state and tranche identity. Individual ZINC-22 3D rebuilding may require login; access to a structure does not establish present stock or unrestricted redistribution. Some web routes timed out during this research; no download was qualified. [Selection documentation](https://wiki.docking.org/index.php?title=ZINC-22:Select_chemical_space_for_docking), [search documentation](https://wiki.docking.org/index.php/Zinc22:Searching). |
| Core structure source: **PubChem / PubChem3D** | General compound collections, identifier resolution and computed conformer acquisition for selected records | PUG-REST and bulk downloads provide SDF 2D/3D; 3D availability is a separate subset. Preserve CID, depositor SID and conformer identities. Computed geometry is not an experimental bound pose; not every compound has 3D. Source-specific rights and rate limits remain part of acquisition. [Downloads](https://pubchem.ncbi.nlm.nih.gov/docs/downloads), [PubChem3D](https://pubchem.ncbi.nlm.nih.gov/docs/pubchem3d), [PUG-REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest). |
| Important commercial discovery target: **Enamine Stock / REAL** | Real in-stock screening collections and much larger make-on-demand chemical space, including lead-like and fragment subsets | Official pages offer SDF/SMILES/CXSMILES and catalog IDs; REAL Database is an enumerated subset of REAL Space. Do not equate Stock, REAL Database and reaction/synthon spaces. Current website terms require specific attention before computational use; see the access finding below. [Stock](https://enamine.net/compound-collections/screening-collection), [REAL Database](https://enamine.net/compound-collections/real-compounds/real-database), [subsets](https://enamine.net/compound-collections/real-compounds/real-database-subsets). |
| Core activity reference: **ChEMBL** | Retrospective cohorts, target/assay annotations and interpretation of screening hits | Public paginated API and versioned SDF/SQL dumps; release documentation currently lists ChEMBL37, May 2026, with a release DOI. Primarily a 2D/bioactivity source, not a prepared conformer library or supplier. The live API is not a historical snapshot. Data license is CC BY-SA 3.0. [Downloads](https://chembl.gitbook.io/chembl-interface-documentation/downloads), [API](https://chembl.gitbook.io/chembl-interface-documentation/web-services/chembl-data-web-services), [FAQ/license](https://chembl.gitbook.io/chembl-interface-documentation/frequently-asked-questions/general-questions). |
| Core binding reference: **BindingDB** | Binding measurements with source provenance, target-focused collections and affinity interpretation | Official downloads advertise TSV and 2D/3D SD files, including source-specific partitions. Measurements, compounds and targets retain separate identities. Some current catalog entries show zero-byte/epoch metadata; actual asset receiving must verify availability and bytes. Curation/source-specific terms require preservation. [Official downloads](https://www.bindingdb.org/rwd/bind/chemsearch/marvin/SDFdownload.jsp?all_download=yes). |
| First repurposing collection: **DrugCentral** | A manageable collection of known drugs with regulatory annotations | Official SDF V2000/V3000, SMILES/InChI and regulator-specific approved-drug exports; a database dump dated 2026-09-25 is listed. Structure files can be consumed without installing PostgreSQL. V3000 includes undefined structures, so admission must be explicit. 3D ensembles were not verified. Data license CC BY-SA 4.0. [Downloads](https://drugcentral.org/download), [license route](https://drugcentral.org/privacy). |
| Repurposing extension: **Broad Drug Repurposing Hub** | Annotated approved/clinical/tool-compound sets and sample-level supplier correspondence | The current portal offers batch Drug information and Sample information files, including SMILES and Broad/vendor identifiers, and states that an annotations API is unavailable. Preserve file version and compound/sample distinctions. Annotation and downstream experimental-data terms differ; physical access uses its own agreement. No 3D ensemble was verified. [Official portal](https://repo-hub.broadinstitute.org/repurposing). |
| Focused diversity extension: **NCI/DTP/NExT sets** | Defined diversity and oncology collections with institutional identifiers | Official NExT pages offer SD files; DTP describes Diversity Set VII and approved-oncology sets. File availability does not guarantee 3D preparation or physical access. The current DTP page restricts new physical requests from outside the US/territories. Preserve NSC/set identity and current access status. [NExT libraries](https://dctd.cancer.gov/drug-discovery-development/services/next/resources/screening-libraries), [DTP sets/access](https://dctd.cancer.gov/drug-discovery-development/reagents-materials/vialed-plated-compounds). |
| First natural-product collection: **COCONUT** | Natural-product diversity, collection-based selection and additional discovery space | Versioned monthly Zenodo releases and CSV/SDF 2D/3D are documented; REST API requires authentication. Verify each data artifact's terms rather than applying the software MIT license to all data. 3D presence does not certify state or conformer coverage. [Versions](https://steinbeck-lab.github.io/coconut/versions.html), [API](https://steinbeck-lab.github.io/coconut/api-documentation.html), [source/license notice](https://github.com/Steinbeck-Lab/coconut/blob/main/README.md). |
| Natural-product provenance extension: **LOTUS** | Organism/source/publication context for discovery and hit interpretation | SDF/SMILES and frozen DOI releases; CC0 data. No ready conformer ensemble was verified. An organism–structure occurrence is not another independent molecule. [Documentation](https://lotus.naturalproducts.net/documentation), [snapshot](https://doi.org/10.5281/zenodo.5794106). |
| Supplier catalog expansion: **Mcule, MolPort, Chemspace, eMolecules** | Connect predicted hits to supplier identities and acquisition options | Official download/API/export routes exist, with public structures and credential/subscription-dependent supplier metadata varying by provider. Preserve a dated catalog snapshot separately from a live stock lookup; never infer availability from a stale catalog. Initial compatibility should include authorized local SDF/SMILES imports. [Mcule files/API](https://doc.mcule.com/api), [MolPort access](https://www.molport.com/blog/database/ftp-database-download/), [Chemspace sets](https://chem-space.com/compounds), [eMolecules screening](https://www.emolecules.com/products/screening-compounds). |
| Licensed/optional repurposing extension: **DrugBank** | Drug/target annotation and licensed drug collections | The current release page lists 5.1.22, June 2026, and explicitly pauses academic downloads, including SDF/3D. Do not advertise a functioning anonymous downloader. Support user-authorized local files first and recheck access before an automatic connector. [Current release and access](https://go.drugbank.com/releases/latest.md). |

These are product priorities, not evidence that every provider can presently
deliver every requested subset or be used under the same terms. Numerical
catalog sizes are deliberately not an integration contract: the search index
and fresh REAL page, for example, advertised different totals during this review.

## Evaluation datasets belong beside the library catalog

**LIT-PCBA** is the first benchmark adapter to consider for measured active/
inactive assay outcomes. Its official distribution documents SMILES, partitions
and crystallographic references. Endpoints can be cellular or functional and
must be qualified for the scientific question; they are not automatically direct
binding. [Official dataset](https://lab.drugdesign.unistra.fr/datasets/lit-pcba/).

**DUD-E** is useful for historical compatibility and additional tests. Its decoys
must retain a separate label from measured inactive compounds and must not be
the sole evidence of predictive utility. [Official target/download example](https://dude.docking.org/targets/fpps),
[original benchmark](https://pmc.ncbi.nlm.nih.gov/articles/PMC3405771/),
[published bias analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC6701836/).
No unrestricted dataset redistribution license was established for these two
benchmark distributions in this review.

The existing [ERα signaling pilot](../docs/content/validation/esr1_activity_pilot.md)
used a Bath ESR1ago derivative checked against Tox21/PubChem AID743075. It is an
executed ligand-reference pilot with weak predictive discrimination, not the
new receptor study, a complete LIT-PCBA evaluation or a fresh unseen holdout.

## Access findings that change the integration order

The current [Enamine website terms](https://enamine.net/terms-of-use), section 15,
state that computational processing of Enamine data requires express written
authorization, including traditional cheminformatics. The marketing pages also
describe virtual-screening use. This research does not resolve which separate
catalog agreement applies to a particular user; the connector must represent
the applicable agreement/access status instead of assuming unrestricted use
from public visibility. No Enamine collection was downloaded or processed.

Mcule documents an official public database-file metadata endpoint containing
formats, URLs, dates and checksums; richer supplier/availability data may require
authentication/subscription. Use sanctioned API/download routes rather than
website scraping. MolPort distinguishes structure access and richer professional
data, with credentials and monthly downloadable updates separate from daily
online stock. These are practical product requirements, not hypothetical gates.

DrugBank's paused downloads make a first automatic acquisition demo unsuitable
today. DrugCentral is the more practical first drug-set candidate; that is a
workflow recommendation, not proof of a prepared 3D library.

## What powerful and friendly support must mean

The default user journey should be: choose the scientific task and collection,
request a bounded subset, receive an immutable library, prepare it explicitly,
screen with a declared pharmacophore and inspect/export traceable hits.

1. Discover collections with purpose, release, access state, available 2D/3D,
   subset choices, download size and preparation requirements visible before work.
2. Select by catalog-native properties and reproducible rules; support fragments,
   lead-like/drug-like, natural products, approved drugs and explicit user files.
   Do not silently sample a moving live endpoint or download an entire huge space.
3. Download/resume/cache with exact URLs, release/date, original bytes/hashes,
   source terms and identifiers. Refresh deliberately; replay a frozen selection.
4. Preserve record → molecule → state → conformer correspondence. Stereochemistry,
   protonation, tautomers, salts, duplicate supplier records and conformer
   ensembles need explicit provider policies and original-ID mappings.
5. Stream bounded batches and persist incremental results/checkpoints. Retain
   valid negatives, unsupported inputs and failed preparation/scoring separately;
   never turn a failed molecule into a zero score or silently drop it.
6. Return ranked compounds with matched features, source conformer/state and
   provenance; group conformer hits under a declared compound policy. Catalog
   links and dated availability are useful, while purchase/order actions remain
   distinct explicit user operations.
7. Export source-linked hits and a reproducible run record. Validation summaries
   retain actual assay endpoints, measured/decoy distinctions, splits, grouping,
   leakage and original/evaluated/failure denominators.

Implementation should start with this common workflow plus ZINC/PubChem and
reference-data access, then a small DrugCentral or COCONUT demonstration. Enamine
is a high-value compatibility target with explicit agreement handling. Supplier
extensions, LOTUS and optional licensed data then reuse the same contracts.
This order balances screening utility and a verifiable first user experience;
it is not an accepted public API or release schedule.

## Current implementation and ownership limits

Repository inspection finds a real gap: [ZincDownloader](../pharmacophoremt/data/zinc.py)
currently calculates tranche-bin indices, prints a download message and returns
a directory. It performs no HTTP acquisition or manifest validation. It must not
be described as working public-library support.

[VirtualScreening.run](../pharmacophoremt/screening/virtual_screening.py) materializes
the complete iterable; prepared-native evaluators exist, but this is not a
bounded streaming library workflow. The current conformer route consumes prepared
frames; it does not generate conformers. Collection reading/preparation and
reusable molecular operations remain MolSysMT-owned, including any missing
multi-record SDF/SMILES, state and conformer capabilities. PHMT owns the screening
experience, query/method settings, results and scientific interpretation. No
retired molecular collection reader is recreated by this proposal.

Before claiming a provider works, qualify an actual small acquisition/import,
manifest replay, molecular preparation, screening and interrupted-run recovery
through supported contracts, with fixtures for failure/accounting and rate-limit
behavior. Documentation or a provider's API description alone is not execution
evidence. No new connector, library download, molecule preparation, model, score,
benchmark result, package dependency or external notification was produced here.

## Review provenance and maintenance

Research used official provider/laboratory documentation, terms and primary
papers, plus read-only repository inspection, on 2026-11-06. Some ZINC routes
timed out and a PubChem browser route showed a challenge; these observations do
not certify that the services or documented download routes are unavailable.
Provider documents were read as documentation, not downloaded chemical datasets.
Recommendations and unverified boundaries above are explicit inferences from
those sources. Recheck changing access, licenses, releases and actual endpoints
before implementing a connector or choosing a screening snapshot. Scientific
source admission, provider qualification and retrospective/prospective results
retain separate authority.
