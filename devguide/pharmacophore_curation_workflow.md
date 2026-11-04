# Explicit curation of cached pharmacophore hypotheses

## Merge facade received — 2026-11-04

[#77 compatibility contract](pharmacophore_merge.md) now makes Pharmacophore.merge
a keep-policy facade over public composition: independent sites and structured
provenance of both inputs, explicit common-frame handling and unchanged molecular
reference ownership. Earlier #77 pending statements below describe their original
review checkpoints. No molecular routine is added.

## Live-reference qualification — 2026-11-04

[#60 ownership contract](live_reference_ownership.md) qualifies intentional
live molecular references and explicit public MolSysMT eager copies with
199 source controls. Cached hypotheses remain historical after source changes;
raw mutations/automatic cache authentication and installed delivery stay outside
this scope. Legacy merge metadata/alias review remains #77.

The owner is PharmacophoreMT. Curation operates on cached Feature + Shape sites;
it neither queries nor copies a molecular system. Molecular preparation,
selection, geometry and transformations remain MolSysMT operations.

## Public steps

- `get_interaction_site_indices()` returns unique local indices in caller order,
  optionally filtering exact cached feature and shape names. Both filters combine
  with AND. Unknown names and invalid/out-of-range indices raise; an empty result
  is valid. Molecular selections are a separate MolSysMT contract.
- `copy_pharmacophore()` deep-copies sites, quantities, feature lists and nested
  metadata while preserving score and evidence. Its linked molecular system is
  the same reference. `Pharmacophore.copy()` delegates to this tool.
- `extract_pharmacophore()` independently selects sites in caller order. It
  records the entire native source-model snapshot and source/output site map.
  Empty extraction is valid, but cannot be used as a nonempty pose query.
- `edit_pharmacophore()` independently changes declared essential flags, weights,
  radii or Gaussian widths. Explicit `in_place=True` stages and validates every
  target before committing. Native site identities survive the commit. Class
  `set_essential`, `set_weight`, `set_radius` and `set_sigma` delegate here and
  preserve setter return value None.

If the same native site object occurs at several model indices, an in-place
selection must include every occurrence of each targeted object. A partial
selection raises before changing any site, shape, metadata, name or score,
including when optional digestion is skipped. Use the default independent edit
to change just one occurrence: each output occurrence is a separate native site.
Selecting every occurrence in place preserves the shared site identity and
records a change for each selected index. References held by other callers still
refer to that site; use an independent variant when isolation is required.

Extraction and editing set score to None. The original score remains in the
complete `source_model` snapshot. Metadata has method
`explicit_pharmacophore_curation@1`, operation, producer version, reason,
parameters, local site map and before/after edited fields. Repeated edits retain
the earlier snapshot chain. Original observation, relation and occurrence indices
remain scoped to their original analyses; they are not renumbered as model sites.

## Constraint semantics

Essential flags are booleans. Weights are finite nonnegative scalar real numbers,
not numeric strings, vectors or quantities. Zero weight removes the contribution
to weighted coverage; it does not disable an essential site or an excluded-volume
veto. Removing a constraint requires extraction of the wanted subset.

Lengths require finite positive scalar quantities with explicit units. `radius`
applies to Sphere, SphereAndVector, Disk and Cylinder; `sigma` applies to
GaussianKernel. Editing preserves center, orientation, endpoints and other shape
parameters. A mixed incompatible selection raises before changing the original.
The previous `set_radius` convenience behavior for GaussianKernel is deliberately
rejected: use `set_sigma` to express that distinct magnitude. Skipping optional
ArgDigest preprocessing cannot bypass scientific validation.

Copying can retain native geometry independently, while extraction/edit history
requires native persistence support. This change does not add shapes to the pose
evaluator or invent serialization for unsupported extensions. Bounded native
`same_participant` composition should precede curation: its root-source contract
cannot be inferred from a curated snapshot. Generic `keep` composition preserves
explicit curated alternatives.

## Attribution and evidence limits

Pure selection, copying and extraction add no new calculation credits. They
retain original bibliography. Optional Ackredit records host constraint edits and
PyUnitWizard when editing a length, without re-crediting molecular detectors or
assigning a publication to caller choices. Missing or failed tracking does not
replace successful scientific output; existing host diagnostics record the state.

The guard is [tests/test_curation.py](../tests/test_curation.py); the executable
recipe is [the curation cookbook](../docs/content/cookbook/pharmacophore_curation.md).
The owning theme is [#38](https://github.com/uibcdf/pharmacophoremt/issues/38).
Literal-text native persistence is separately tracked by
[#25](https://github.com/uibcdf/pharmacophoremt/issues/25).

Initial focused qualification: Python 3.14.7, 54 passing controls in 42.68 s.
The cases use analytical prepared interaction geometry and independent fixed-frame
pose checks. They establish constraint behavior and evidence preservation, not
affinity, a preferred scientific hypothesis, activity-trained weights, biological
performance or CPU/GPU scaling.

The three cookbook blocks execute on Python 3.14.7 with stable hashes of all four
recorded Python producers; strict isolated Sphinx rendering passes with existing
Python 3.13 documentation tooling. The seven retained evaluations show the narrow
donor variant failing and the wider variant matching, required versus optional
coverage .9, optional weighted coverage .75, zero-weight essential rejection
despite coverage one, and an exclusion veto despite coverage one. Actual radius
editing captures two software items/two uses; pure cached steps capture no uses.
The [verification summary](evidence/curation_py314_summary.json) links the complete
compressed recipe audit, original model, edited model, complete evaluation results,
actual attribution and exact executed runner. This is curation verification,
not a new biological dataset or a timing comparison.

The full suite passes **542 tests in 730.39 s**, with eight existing warnings.
The separate source-stability audit fails because Ackredit changes from Python
source SHA `2edfd47edf88bebff9296f6249797b56c91c84051cc0793edfd5949eada794cc`
to `8209da967e583501d23919bc76863dcbc2646d14f4f7fc690a08cf24f61c68bc`
during execution. PharmacophoreMT, the MolSysMT snapshot and PyUnitWizard remain
unchanged. The full run establishes passing local tests, not qualification against
four fixed provider sources. Its original audit and log remain alongside the
independently stable cookbook evidence. The editable installation is confirmed
without a PYTHONPATH override; only MolSysMT is overridden for this full run.

## Current source/API acceptance — 2026-11-03

Clean producer **404aa3829ac8d43bd6cb3c883f5547eb460857b0** passes 84 owning
curation/contracts/model/site/pose controls, zero failures, errors or skips.
Eleven new alias controls include nine failing counterexamples before the fix;
the complete curation module now has 47 cases. The three existing cookbook blocks
reproduce all seven expected status/coverage outcomes and actual attribution.
Full source/native/helper/test and metadata lookup identities remain unchanged
during both phases. The [new receipt](evidence/curation_acceptance_20261103_summary.json)
retains complete models, evaluations, credits, commands, runners, identities and
initial harness failures. A strict isolated rendering of this cookbook page
passes with a stub for the adjacent attribution link; full-site navigation is
outside that rendering check. Original October records above are preserved.

#38's source/API acceptance is resolved and its report is
[archived](archive/public_pharmacophore_curation.md). This does not imply a full
current-suite rerun, clean installed/public/Conda/platform qualification or
biological/performance validation. The temporary venv borrows shared scientific
dependencies with disclosed MolSysSuite #82 conflicts; molecular links remain
the separate #60 policy. Exact final-head hosted receiving stays #9.
