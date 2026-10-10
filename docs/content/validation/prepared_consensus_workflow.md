# Prepared distinct EST/DES consensus control

## Identity and claim

Case `prepared-distinct-consensus-est-des@1`, owned by
[PharmacophoreMT #51](https://github.com/uibcdf/pharmacophoremt/issues/51),
maintainers LMMV/dprada; review date 2026-10-10. Evidence class: analytical
workflow controls on prepared public chemical data. The claim concerns distinct
support, original occurrence maps, completed empty outcomes, failed rebuilds and
saved native hypotheses. It extends the [original CCD case](prepared_ccd.md)
with independent controls rather than just additional returned-model counts.

## Inputs and preparation

Use the untouched EST/DES ideal SDFs from the
[frozen manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/prepared_ccd/manifest.json).
Original source URLs, acquisition date, references/redistribution provenance and
chemical-state interpretation limits remain in the original case. No new data
is acquired. EST SHA-256 is
`9b3fe86469dd81554830f01ea11daa6d58fe329a887e6b36f0a42481eb18980f`;
DES is `a5066a55ebb0bce8678df671014f75b4cd666cab35936ed36da5b7d8a12722f4`.
MolSysMT preparation retains source hydrogens, atoms, bonds and coordinates:
EST 44 atoms/47 bonds/24 H; DES 40 atoms/41 bonds/20 H. Its CTAB stereo
interpretation is not independently qualified by this case.

Select acceptor spheres and aromatic axes: EST contributes two acceptors/one ring;
DES two acceptors/two rings. All atom/frame/state contexts are explicit. EST frame
zero and DES frame one participate; public MolSysMT creates DES frame one by
Rz(+90°)+`[2,1,3] nm` from the same ideal conformation. That extra placement does
not create a third supporter or establish conformer diversity. Original full
chemical states/coordinates remain unchanged.

## Execution and independent expectations

The [recipe](../cookbook/prepared_consensus_workflow.md) uses the explicit native
facade; the [maintained contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/prepared_consensus_workflow.md)
records options and independent occurrence/geometry expectations.

```bash
python -m devtools.prepared_workflow --case consensus --output /tmp/prepared-consensus.json
python -m pytest tests/test_prepared_consensus_workflow.py tests/test_prepared_workflow.py tests/test_prepared_search_workflow.py --receptor=llm
```

Normal editable Python 3.14 development uses `molsyssuite@uibcdf_3.14` without
Requires-Python/PYTHONPATH bypass. The existing recorder retains full native
output, source/input hashes, loaded MolSysMT extension, original head/dirty
source overlay, actual references and fresh-reader outputs. Ranked triplets use
four selected seeds, greedy final-angle refinement, minimum three matches/sites,
joint support two, distance 0.20 nm, angle 30 degrees and 100 fits; other bounds
use native defaults. Finite-family completion is not an exhaustive search claim.

Independent frozen atom domains, arithmetic mean centers, the known proper motion,
set intersection for joint support, injectivity and a test-only aromatic plane
oracle check the output. Geometry tolerance is 1e-12 nm/dimensionless, angular
oracle tolerance 1e-10 degrees. Both original source atom counts/identities differ;
this case does not infer chemical uniqueness from arbitrary declared IDs.

## Results and interpretation

The focused selection passes **36 tests in 78.37 s on Python 3.14.7**: eight
new consensus guards and 28 unchanged placed/search controls. Both recipe blocks
execute, the reviewed installed-development preflight passes, and strict isolated
rendering covers these two new pages. Rendering uses Sphinx 9.1 on Python 3.13;
this is documentation validation, not qualification of scientific code on 3.13.

The [2026-10-10 original summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/prepared_consensus_workflow_py314_summary.json)
links the full gzip record by compressed/uncompressed hashes and byte counts.
The producer head is `9594e99fdc6865529ad51882744902c85e189ffb` with an
explicit uncommitted developer-tool/test overlay retained as executed source bytes.
Runtime scientific source is unchanged. All 30 earlier gzip archives retain their
original bytes. Host-off/on runs pass with identical decoded scientific fields
and unchanged producer Python/input hashes.

Both the native tool and explicit facade produce one three-site hypothesis,
with joint support two/fraction one, after two fits and one accepted layout.
The mapped source occurrences are EST 0/1/2 and DES 0/1/2; DES occurrence three
(second ring) is not reused to manufacture a fourth jointly supported site.
Original atoms, frame/state records, member centers, arithmetic mean sites and
unoriented aromatic normals satisfy the independent guards.

The independent empty expectation follows
without a fit-score oracle: every jointly supported disjoint site must consume
one EST occurrence, and EST has only three. A four-site minimum therefore cannot
produce a hypothesis. Fit-resource failure must instead raise PHMT-E107 and leave
facade result/report unset. JSON/YAML/versioned PHMT virtual-site SDF comparisons
preserve exact metadata/source maps and constraints across pm/fs/degrees writing
and Å/ps/radians reading, with the declared emitted-geometry tolerance.

Actual host-on capture retains 21 items/81 uses, including both actual input
datasets and reached fitting, ranking, assignment and clique criteria. Host-off
retains independently configured provider attribution (four items/six uses).
Fresh readers register zero new uses. Complete references/contextual uses remain
in the original output; design literature is not promoted to execution credit.

No activity labels, train/test split, enrichment metric, experimental binding-mode
acceptance or speed/memory comparison applies. Returned shared hypotheses are
workflow controls, not biological evidence.

## Maintenance and independent gates

Rerun after inputs/preparation, feature occurrence domains, geometry, support/
failure contracts or codecs change. Preserve earlier archives and append new
measurement identities. Provider #375/#323/#219/#367 and #23's hosted/installed/
public delivery remain separate gates. No sibling code or runtime molecular
routine changes are required by this case.
