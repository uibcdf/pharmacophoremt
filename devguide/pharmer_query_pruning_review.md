# Pharmer: query meaning, pruning and final acceptance

Selected source review, 2026-11-09; owners LMMV/dprada;
[#128](https://github.com/uibcdf/pharmacophoremt/issues/128),
[canonical Pharmer record](https://github.com/uibcdf/pharmacophoremt/discussions/131).
The [prospective scope](evidence/pharmer_query_review_plan_20261109.json) precedes
the captured source and [receipt](evidence/pharmer_query_review_20261109.json).

## Source and evidence boundary

The official standalone source is fixed at **SourceForge SVN revision95**,
through `https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/`. Twenty-four selected
text files retain their response metadata, lengths and SHA-256 identities.
The root listing reports revision95; a file's ETag can name its earlier last
change. These are captured HTTPS snapshot bytes, not a built binary or an
independent audit of server history. Selected functions were read; this is not
an exhaustive source audit.

The historical `/trunk/` URL returns404. The maintainer's
[2019 correction](https://sourceforge.net/p/pharmer/discussion/1669176/thread/dd9e495e75/)
points to the repository root, which works. A guessed `dkoes/pharmer` GitHub
repository also returns404. The GitHub mirror and current Pharmit tree are not
substituted for the authenticated standalone snapshot.

The [2011 paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC3124593/) explains typed
triplet indexes, range searches, fingerprints, correspondence reconstruction and
radius-weighted alignment. Its optional-feature section proposes extensions;
that discussion alone does not qualify an implemented optional/counting query.
Historical timings establish neither present PHMT performance nor equivalent
scientific answers. This review builds/runs neither Pharmer nor Pharmit and
acquires no chemical library. The three PHMT arithmetic controls below are
explicitly separate from competitor or public-native execution.

## Query fields need execution-level interpretation

The [JSON reader](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/pharmarec.cpp)
drops `enabled=false` entries and unrecognized feature names. It accepts bare
numeric centers/radii, vectors and size restrictions. Removed entries are not
equivalent to PHMT optional sites, which remain eligible for weighted coverage.
The parser provides no physical-quantity record; a future exchange profile must
declare/verify units and feature-definition correspondence explicitly.

The point type declares Required/Optional/NotPresent, but that enum does not prove
an end-to-end Boolean matcher. In this snapshot, the JSON requirement guard
checks membership of `requirement` but string type of `required`, then reads
`requirement`. This is a source-observed field-name inconsistency, not an executed
parser test or a claim about all versions. Selected query construction forms
triplets over all retained points; fingerprint construction skips non-required
remaining points. Complete optional/negated semantics therefore remain
**unqualified** here. No external bug report is published; the observation stays
in this authorized internal study and needs a complete reproduction before
any upstream report or interoperability promise.

PHMT retains its own [constraint semantics](native_constraint_semantics.md):
alternative kinds within one site, injective typed-record assignment, required
zero-weight sites, optional weighted coverage and explicit exclusions. A future
adapter must report/refuse unsupported or lossy fields, not infer equivalence
from matching field names. No adapter or new query policy is implemented here.

## How the selected search path narrows candidates

| Stage | Inspected standalone behavior | Consequence for PHMT design |
| --- | --- | --- |
| Typed triplets | `initializeTriplets` constructs query triples; `generateQueryTriplets` chooses a connected mesh using database histogram estimates and expands legal orderings | Separate query planning from query meaning; test permutation/symmetry coverage before using selectivity to reorder work |
| Length/index search | `Triplet` forms pair-radius intervals in reduced numeric coordinates; `queryIndex` traverses typed geometric ranges with additional triangle checks | A cheap rejection must remain conservative relative to the final predicate and stored precision |
| Additional context | `QueryTripletFingerprint` checks remaining required points through coarse/fine distance/type/chirality fingerprints; a single-triplet query skips fingerprints | A fingerprint positive is only a candidate; ordinary Bloom membership properties do not prove conservative geometric encoding |
| Joining candidates | `TripletMatches` keeps compatible conformer/triplet matches, checks metadata filters and connecting-point consistency; `Corresponder` enforces injective point indices | Preserve original conformer/record identity, repeated roles and filter denominators instead of conflating indexed triangles with compounds |
| Final pose | `Corresponder` fits a complete correspondence, checks every positional radius and exclusions, then publishes an accepted orientation | Keep original final evaluation authoritative after any faster proposal/filter stage |

Primary paths:
[query planning](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/PharmerQuery.cpp),
[triplet predicates](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/Triplet.h),
[database search](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/pharmerdb.cpp),
[fingerprint query](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/QueryTripletFingerprint.cpp),
[joining](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/tripletmatching.h) and
[final correspondence](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/Corresponder.h).
No source observation is a measured speedup or proof that every pruning branch
is sound for arbitrary queries.

## Numerical and result contracts differ

The default fit uses inverse-square radius weights. Final publication additionally
checks each site's radius, computes an **unweighted positional RMSD** for the
returned value and applies `maxRMSD`. PHMT's present MolSysMT anchor fit and its
weighted-coverage/seeded-hit scores answer different questions. Search feasibility,
placement objective, displayed score and activity labels need separate columns
in any comparison.

The [packed representation](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/ThreePointData.cpp)
rounds coordinates/lengths with a multiplier of 1000 and bounded integer fields;
angles also use finite storage. The fingerprint source uses coarse/fine bins 4/1
in its native numeric units. The database builder clips indexed feature triples
to the first 256 points after reporting an oversized feature count, and can omit
oversized molecule records. Those limits require explicit coverage accounting;
they are not PHMT defaults or a license to silently truncate a new index.

Direction is another admission boundary. `Triplet::setExtra` uses the first query
vector and sphere-grid masks with nominal settings of 45 degrees for aromatic
axes and 60 degrees for other vectors. The examined final publishing branch does not repeat a
PHMT-style exact angular predicate. PHMT's configured donor-vector/aromatic-axis
checks therefore need a separate compatibility case, not a copied vector field.

The selected [exclusion predicate](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/Excluder.h)
uses a closed sphere (`distance_squared <= radius_squared`) on stored molecular
coordinates after fitting. PHMT excludes selected heavy atoms strictly inside
the radius. Even with matched geometry, equality/atom-set/precision policies need
declared controls. Stored atom membership was not fully traced in this review;
no universal equivalence or discrepancy is claimed for real molecules.

`max-orient` stops orientation enumeration for a conformer; conformer reduction
and `max-hits` filter retained outputs. These are distinct from PHMT's raw seed
product budget and explicit incomplete-search failure. A returned prefix is not
automatically every pose or an exhaustive negative. The standalone README's
host-wide resource-setting suggestions are historical deployment instructions;
none is applied to this shared workstation.

## Concrete PHMT finding

The conservative-filter question exposes [PHMT#160](https://github.com/uibcdf/pharmacophoremt/issues/160).
Its evaluator admits an eight-epsilon relative positional allowance, while its
triplet pair filter uses the strict physical radius sum. With exactly representable
nm values r=1/8 and delta=2^-52, two accepted per-site deviations of r+delta
produce a pair-distance excess of `2r + 2delta` that the strict pair filter rejects.

Three declared stdlib arithmetic controls, checked independently with rational
binary values, confirm that literal predicate mismatch: nominal radius,
accepted numerical boundary and a beyond-allowance negative. They import no PHMT,
MolSysMT, NumPy or competitor and perform no fitting. An actual public-native
search reproduction, correction and source/installed receiving remain pending
under#160. The checked-pose route also tests the original placement; the seeded
route does not. This does not establish an end-to-end failure of every method.
It justifies qualifying the numerical candidate boundary before new indexes.

## Proposed comparison cases, not executed results

These are research questions, not a frozen executable benchmark plan. Each needs
admitted feature/preparation definitions, exact coordinates/units, complete inputs,
native versions, stopping rules and safe resources before execution.

| Case | Declared question / required observation |
| --- | --- |
| P1 Required spherical interior | Compare compatible typed three-point rigid cases, then a multi-point case; retain every original mapping and final predicate result |
| P2 Unequal radii/objectives | Separate radius-weighted placement, unweighted RMSD and PHMT coverage/seeded scores; record differing objectives without forcing a common ranking |
| P3 Optional, disabled and negated fields | Reproduce the exact r95 parser behavior, then trace a missing optional point through mesh/join/final stages; use refusal/loss reports where meanings differ |
| P4 Filter ablation | Compare full final outcomes with and without fingerprint/range filters on the same admitted stored representation; retain false-positive counts and any candidate false negative |
| P5 Chirality, symmetry and degeneracy | Include repeated feature types, proper transforms, a noncoplanar reflection, coplanar/collinear and near-degenerate anchors; inspect omitted/permuted mappings |
| P6 Quantization and capacity | Test reduced-coordinate/bin boundaries, large coordinates and feature-index limits; account for omitted/truncated inputs and rebuild compatibility |
| P7 Positive/exclusion boundaries | Freeze binary-exact distances/units and a common atom set; distinguish inclusive positives, exclusion equality and numerical allowances |
| P8 Assignment identity | Retain distinct typed records sharing atoms, repeated source/conformer occurrences and one-record capacity; do not infer chemical independence |
| P9 Stopping/denominators | Distinguish trial budgets, cancellation, conformer/orientation limits and output pages; preserve incomplete/failure versus confirmed negative |
| P10 PHMT numerical filter | Qualify#160 against the actual public operation, including nominal/allowance/outside controls and seeded versus checked-pose behavior |
| P11 Search-asset compatibility | Bind feature definitions, prepared geometry, units, quantization, source/frame/state and build parameters; changed context must receive a new qualified asset |
| P12 Direction/size stages | Trace first/multiple query vectors, aromatic-axis symmetry, configured angle and size restrictions through coarse filters and final acceptance; declare unsupported mappings |

PHMT owns query/search semantics, compatible feature assets and result accounting.
MolSysMT retains molecular perception, formats, preparation, transforms and collection
snapshots under its existing#624 boundary; the review creates no molecular fork.
The useful next increment is#160qualification, while the environment/native gates
and original#148failures retain their separate recovery routes. No engine,
index, connector, method acceleration or public dependency is adopted by this study.


## Subsequent PHMT numerical receiving — 2026-11-09

The original study and its unexecuted comparator cases retain their scope.
[PHMT#160](https://github.com/uibcdf/pharmacophoremt/issues/160) now has a
separate conservative pair-filter correction, independent public guard and
real public-native before/after witness. All116selected source/same-file owned
installed cases pass and twelve ordinary outputs/counters remain unchanged.
See the [numerical contract](pair_distance_pruning.md) and
[installed receipt](evidence/pruning_slack_installed_20261109.json).
This does not execute a competitor, qualify#148or establish biology/scale.
