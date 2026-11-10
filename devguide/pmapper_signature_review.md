# pmapper signatures, matching and screening artifacts

Owners LMMV/dprada; 2026-11-10; [#174](https://github.com/uibcdf/pharmacophoremt/issues/174)
under#128/#108 and mature-0.x milestones5/6. This reviews **DrrDom/pmapper**,
distinct from ChemAxon PMapper. Source inspection is not an executed comparison,
a runtime dependency decision, or evidence of biological prediction or speed.

## Exact source and documentary scope

Selected [commit2f77e648](https://github.com/DrrDom/pmapper/commit/2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd)
declares1.1.3 in its package initializer. Ten selected original files retain
Git-blob/byte/SHA-256 identities in the
[review receipt](evidence/pmapper_review_20261110.json). The source
[license](https://github.com/DrrDom/pmapper/blob/2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd/LICENSE.txt)
is BSD-3-Clause; the [setup](https://github.com/DrrDom/pmapper/blob/2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd/setup.py)
declares NetworkX>=2 and an RDKit extra. Its Python>=3.6metadata does not establish
execution on the current PHMT development interpreter or a supported matrix.

The [hosted API documentation](https://pmapper.readthedocs.io/en/latest/pharmacophore_class.html)
identifies0.2 and describes a tuple-based matching result. The inspected1.1.3
source instead returns a source-feature→model-feature dictionary, optionally
combined with a transform/RMS. Do not design against the older return shape.
The [2018 method record](https://pubmed.ncbi.nlm.nih.gov/30486389/) names Alina
Kutlushina, Aigul Khakimova, Timur Madzhidov and Pavel Polishchuk,
DOI10.3390/molecules23123094, and links a2019correction. This study does not
reproduce that paper's cohorts, modeling process or reported biological results.

## What the selected implementation actually represents

The [coordinate loader and distance graph](https://github.com/DrrDom/pmapper/blob/2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd/pmapper/pharmacophore.py#L68)
assign sequential node IDs, preserve label/coordinate pairs and remove exact
duplicate pairs with a warning. It builds a complete distance graph. A positive
bin_step stores floor(distance/bin_step); zero retains numerical distances.
External tuples carry no declared physical unit themselves. A comparison must
freeze explicit units and label correspondence; a bin is not a PHMT site radius.

The [signature](https://github.com/DrrDom/pmapper/blob/2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd/pmapper/pharmacophore.py#L126)
counts canonical feature subsets of at most four nodes and includes an explicit
chirality classification where applicable. An MD5 digest summarizes those
strings/counts. Labels, binned distances, chirality policy and planarity tolerance
all affect the representation. Digest equality is not authenticated provenance,
source-record identity or universal chemical/geometric equivalence.

[Fingerprints](https://github.com/DrrDom/pmapper/blob/2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd/pmapper/pharmacophore.py#L405)
compress subset hashes into activated bit positions. They lose information beyond
the upstream representation and need their own retrieval guarantees. Count-based
descriptors are a different output. Source calls random.seed on the module-global
RNG while activating bits: an application-isolation question, not an observed
execution result at this stage.

## Matching is a staged, versioned question

[fit_model](https://github.com/DrrDom/pmapper/blob/2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd/pmapper/pharmacophore.py#L543)
requires equal bin_step, enumerates NetworkX subgraph mappings, compares subset
signatures and returns its first retained mapping. It does not enumerate all
accepted poses for its caller. Omission mode separately enumerates omitted model
features; its meaning must not be relabelled as PHMT essential-site semantics.
The zero-bin graph path still uses a0.75absolute edge-match tolerance; it is not
an exact floating-distance equivalence promise.

Optional RDKit fitting returns a transformation/RMS after signature acceptance.
The inspected path does not add a final per-feature PHMT sphere/vector/exclusion
acceptance test. Equal-bin hashing and a continuous positional tolerance are
different predicates. Necessary-distance PHMT proposals are also a different
stage from either a final fit or a complete continuous search. Compare each stage
by its own definition rather than forcing identical truth values or score units.

## Cache, persistence and identity questions

The [subset cache](https://github.com/DrrDom/pmapper/blob/2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd/pmapper/pharmacophore.py#L126)
uses feature-ID tuples plus tolerance. Source add_feature explicitly drops the
cache. The inspected coordinate-reload and update(bin_step=...) paths do not
show that same invalidation. This is a concrete warm-object/fresh-object equality
question to execute before trusting a mutable cached asset; no runtime defect
is claimed by source inspection alone.

[Native PMA persistence](https://github.com/DrrDom/pmapper/blob/2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd/pmapper/pharmacophore.py#L916)
saves bin_step and labeled coordinates, rather than a PHMT source/preparation/
unit/frame/producer manifest. Pharmit import keeps enabled centers/labels and
ignores radii/directions; export rounds coordinates and writes bin_step as radius.
These are lossy projections with different semantics, not equivalent query
round-trips. Original record/occurrence mappings require a separate owner.

## Concrete PHMT decisions and prospective controls

1. Treat any future hash/fingerprint asset as a versioned retrieval stage with
   original source/prepared-snapshot, feature definition, units/frame, parameters,
   representation and producer identity. Never use its digest as chemical identity.
2. Before using bins as a reject filter for PHMT's continuous-tolerance problem,
   measure same-bin geometric false positives and cross-bin feasible pairs.
   A rejection guarantee needs a proof/qualified neighborhood strategy.
3. Compare fresh, cached and mutated objects for coordinate reload/bin changes;
   retain identical input/settings/output controls before measuring speed.
4. Retain original ordered IDs through duplicate reduction, query omission and
   the first-match output. Different denominators or coverage prevent speed claims.
5. Test a noncoplanar reflection and planarity policy separately from distance
   graph acceptance. Preserve proper-fit versus chirality-filter distinctions.
6. Isolate any fingerprint RNG effects and distinguish immutable artifact reuse
   from live mutable-object caching. MolSysMT owns molecular/source collections;
   PHMT owns its search-asset compatibility and pharmacophore interpretation.

No cache/index, molecular preparation, optional engine adapter or new dependency
is implemented here. Later analytical execution needs its own frozen cases,
independent rational oracles, exact import/native identities and conservative
resource plan. #148/#165remain stopped; actual human and supported public/
installed-platform, biological/performance/release gates retain their own evidence.
