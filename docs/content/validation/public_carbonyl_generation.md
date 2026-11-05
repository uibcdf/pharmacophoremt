# Public cached-carbonyl generation

Measured 2026-11-05, owner LMMV/dprada,
[PharmacophoreMT #94](https://github.com/uibcdf/pharmacophoremt/issues/94).
The explicitly selected `donor_aromatic_carbonyl_experimental` source profile
extends cached donor/aromatic generation with separate provider carbonyl lobes.
This is experimental geometric hypothesis construction, not biological validation.

## Inputs, ownership and fixed science

The [original carbonyl receiving case](carbonyl_acceptor_receiving.md) owns the
literal CC=O/[2H]O inputs, original #92 declaration, two frames, repeated source
axis [0,1,0], unit policies, six controls and scientific limits. Plan SHA-256
`b0af26640c0b7ff6cadde2c7f7e499141921adc29fd2ec7f4c1666218be92340`
is unchanged. Original measured donor coordinates are fixed replay inputs,
reconstructed through public MolSysMT; independent original-coordinate oracles
also check them. This is regression on the same case, not a new chemical cohort.

The [public contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/public_cached_carbonyl_generation.md)
was declared before implementation/evaluation. It requires a native provider cache,
explicit source structure position, acceptor distances and the explicit
`towards_receptor` target donor orientation. Geometry/source/selection/state/
recognition/producer/units must agree with the feature cache. Native provider
arrays retain typed shape; empty detached recognition metadata retain their
zero-participant meaning. These checks establish declared cache consistency,
without authenticating molecular coordinates.

Only provider acceptor role1/model2/status1 is admitted. Unsupported, undefined,
known outside-profile chemistry and malformed cache remain different outcomes.
Two lobes become separate one-site donor hypotheses. Unchanged donor/ring choices
and optional exclusions compose through the existing tools; bounded enumeration
never turns an incomplete prefix into a negative search.

All molecular representations, construction, inspection, recognition, coordinates,
directions and transformations stay in MolSysMT. The generator consumes cached
data and accesses no molecular system. Default position-only acceptors and
`donor_aromatic_faces` remain compatible.

## Execution and results

From the qualified source environment:

```bash
python -m pytest tests/test_cached_carbonyl_generation.py devtools/tests/scientific/test_public_carbonyl_generation.py tests/test_carbonyl_acceptor_plan.py --receptor=llm
python -m phmt_test_support.public_carbonyl_generation --output /path/to/result.json
```

The [receipt and original results](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/public_cached_carbonyl_20261105_summary.json)
retain every command, failed attempt and before/after source/native/helper/test/
input/metadata identity. Linux/Python 3.14.7 uses controlled MolSysMT
`0faf1584d05ac47ddcebfc20d9c9978b7f4f230e` and public ArgDigest 0.17.0 extraction.
This is source qualification, without clean installed/public/platform certification.

**295 unique selected controls have passing evidence across preserved scopes:**
181 unchanged donor/aromatic/exclusion/projection controls; 98 new public cache,
product, role, unit, refusal, ownership, attribution and persistence controls;
eight real-provider replay controls and eight original declaration guards. The
final focused run passes 114 controls; the unchanged original-profile scope's
181 earlier passes remain applicable. This is not one full library-suite run.

The public replay completes **12 models, 72 primary and 24 JSON/YAML recovery
evaluations**, plus four unscored unsupported/undefined source queries. Both
unit policies and repeated source positions give the original answers:

| Candidate | Hypothesis0 fit | Hypothesis1 fit |
| --- | --- | --- |
| Lobe0 aligned | 1 | 0 |
| Lobe0 reversed/displaced | 0 | 0 |
| Lobe1 aligned | 0 | 1 |
| Lobe1 reversed/displaced | 0 | 0 |

Water's available donor geometry is not used as its unsupported acceptor geometry.
Collinear carbonyl retains undefined status. Both acceptors produce no usable
query or pose score. Every recovered model keeps physical geometry, original
provider/model evidence and outcomes. Source, candidates, caches, feature
inventories and application units remain intact.

The [standalone cookbook blocks](../cookbook/structure_based_modeler.md#experimental-cached-carbonyl-alternatives)
execute with real provider input, two generated models and one JSON recovery,
without pose scoring. Synthetic product/invalid-cache tests are algebraic
controls rather than recognition or chemical-model evidence.

## Attempts, attribution and limits

An initial duplicated test-fixture keyword prevents collection. The first complete
selection has 273 passes/four new guard-assumption failures: optional capture was
not explicitly enabled, and an intended .1 nm invalid-origin change was truncated
by integer test data. Correct those guards and preserve all original logs/source.
Review additionally covers empty detached participant metadata and missing
producer versions. Frozen physical inputs/settings/expected answers never change.
All complete before/after identity phases are stable.

Actual PHMT/numeric/unit capture is retained, along with original cached provider
references and their separately labeled geometric inspiration. Cached generation
does not claim new molecular recognition/direction calculation. Real enclosing
workflows, absence/failure, native persistence and independent metadata ownership
have passing evidence; unchanged shared reader controls retain their scope.

This establishes the declared experimental source API and its single-aldehyde
receiving behavior. It does not validate wider carbonyl/nitrogen chemistry, PBC,
H optimization, energetic/electronic accuracy, accessibility, affinity/activity,
target breadth or performance. Reexecute after the relevant input/provider/API/
receiving/projection/matching/persistence changes; preserve this run when adding
new scientific choices or results. Budget bounds model count, not input-cache
validation/copying size; request only needed frames from the provider.

Next [#95](https://github.com/uibcdf/pharmacophoremt/issues/95) prepares the proposed
0.5.0 consolidation and exact-candidate gates towards 1.0.0. No tag/package is
published by this source change. #9/#10/#23 hosted/installed/public, #375/#323,
#66/#82/#74/#215 and wider scientific/ownership obligations remain separate.
