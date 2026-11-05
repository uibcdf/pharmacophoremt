# 0.5.0 source-scope and installed-support review

Reviewed 2026-11-05, owner LMMV/dprada, [#95](https://github.com/uibcdf/pharmacophoremt/issues/95).
The source review compares immutable tag 0.4.0 at
`60b21b7d183217d50c29ea3e6bc0d05fb5b797a2` with
`3d26b28ae072c106784299ee96d3a50f0edebc91`: 100 commits, 1,146 changed paths,
including 43 runtime Python files. Most changed paths are frozen study inputs,
original evidence and documentation; neither commit nor line count establishes
release readiness. [Original review receipt](evidence/release_050_review_20261105_summary.json)
records every changed runtime path, old/new hashes, public signature changes,
source-support audit, actual probe/check commands and limitations.

## Reviewed product delta

| Area | Change since 0.4.0 and release interpretation |
| --- | --- |
| Receptor hypothesis generation | New public cached donor/aromatic generation, exclusions and explicit experimental carbonyl alternatives (#87/#88/#94); bounded source API, not automatic receptor preparation or pocket inference |
| Molecular ranking and saved analysis | Explicit seed-only binary criterion, score extraction and original-cohort/paired saved-result summaries (#63/#65); incomplete searches, unscored failures and independent biological validation remain distinct |
| Native persistence | Validated reads, versioned JSON/YAML schema, pre-open export admission and catalog diagnostics (#73/#76/#81); valid historical untagged records remain accepted; SDF ownership/fidelity #74 remains separate |
| Model independence and argument admission | Shared-site edit refusal, live references, independent public merge composition and definition-owned facade/geometry contracts (#38/#60/#77/#6); stricter options and changed merge metadata require migration notes |
| Matching and scientific interpretation | Relative numerical radius-boundary repair, typed-record/any-of/essential/exclusion criteria and controlled support/redundancy/sensitivity/cardinality receiving (#79/#80/#83–#94); wider chemistry, biological prediction and performance stay partial |
| Provider and runtime metadata | Public MolSysMT recognition/vector delegation with labeled historical compatibility; ArgDigest >=0.17.0 and explicit PyYAML dependency. Controlled source pins do not qualify a new public dependency closure |
| Developer/distribution inputs | Expanded runtime resource inventory, current frozen study/support inputs and unchanged supported source/installed matrix; #96 repairs a specific private-support omission before an installed candidate |

The [draft release notes](../docs/content/about/release_notes.md) distinguish new
APIs, changed behavior, retained workflows and known limits. They document ranking
choices/fields, schema/reader/writer admission, independent merge provenance,
strict facade options, donor compatibility and source-versus-public dependencies.
No native schema bump beyond the actual new JSON/YAML @1, provider floor invented
from development versions or new biological claim is introduced by this review.

## Measured installed-support defect and repair

The installed declaration selects all `tests/`, but its 51-file support list omits
`receptor_sensitivity`, `prepared_receptor_sensitivity` and
`receptor_hypothesis_pilot`. Their three frozen module-relative plans also need
private staging. #96's new durable guard invokes the accepted shared @1 stager
with the component checkout excluded from import paths. All three subcases fail
before repair because their module specs are absent. The same guard passes after
adding only those six literal files and hashes; all original 51 entries and the
six source files retain exact bytes.

An actual safe-path child process imports all three helpers from private staging,
reads their exact plans and collects **126 selected test nodes** without running
their scientific fixtures or test bodies. All 57 declared input hashes remain
unchanged. The namespace is absent before/after, staged imports are retired and
the private directory is removed. The child records its real editable PHMT and
controlled provider origins: this is import/collection evidence, not an installed
artifact, scientific rerun or native platform matrix. The unchanged shared SDK
is `1c248b67d1daea256ed7c7f6172c6addb3f0b08f`; no staging/loader implementation is copied.

The complete administrative distribution selection passes 23 tests, including
this guard; reporting (three), archive reader (18), declared dependency routes,
indexes, Ruff/format and whitespace checks pass. Strict isolated rendering passes
for 61 linked source documents and two actual image assets, with notebook/code
execution off. These checks do not substitute for candidate science or installed
qualification. Runtime source stays byte-identical to review baseline3d26b28.

## Disposition and next step

This is a reviewed source baseline and proposed scope, **not a frozen release
candidate**. The committed release plan still identifies 0.4.0; no source tag,
version plan, build, upload, promotion, GitHub Release or documentation publication
is performed. See [readiness](release_0_5_0_readiness.md) for the separate gates.

At baseline 3d26b28, policy and Conda-governance workflows pass; the eight source
science cells are queued. Changed support/notes metadata still needs its own
exact-head checks. Before freeze, resolve/review the public dependency closure
and PHMT #82. Initial source-delivery comments describe correction
`7fdf726d984553c9d89efc08abc2016f46ef41aa` with public 0.17.0 unchanged. A fresh
publication check now finds [ArgDigest 0.17.1](https://github.com/uibcdf/argdigest/releases/tag/0.17.1)
at source `c9c9ee623dab5331fdfa4227bd784dd38620e18b`, published 2026-11-05.
The exact-version registry file has main/staging labels, and independent main
solver-index reading agrees on SHA-256
`5af09e12b0c3d344337f2a2d90ac8b5fcea5be8a8467694c41e3daac018c3899`.
Package-level latest_version fields are stale; their values are not used to infer
availability. No new provider artifact is installed by this review. Publication
is now established separately from pending PHMT consumer receiving.
Retain the measured model-source-routing limitation until the published correction
passes the consumer's adversarial regression; do not copy a binding workaround.

Next receive the applicable published providers and decide the explicit 0.5.0
candidate/version plan, then obtain its required exact-source/build/installed
and public evidence. #9/#10/#23 retain their owning recovery and delivery work.
The [roadmap](roadmap.md) permits further 0.x.y versions, including 0.10.0 and
0.11.0; neither stabilization nor 1.0 is reserved for a particular minor.

The bounded workspace refresh preserves this task's PHMT overlay and clean
MolSysMT/ArgDigest siblings, respectively 113/four commits behind fetched upstream.
It performs no pull/checkout/provider edit. Owned capsule
`build/phmt-050-review-20261105-hlkwdxao`, review 2026-11-19 or relevant change;
borrowed prefixes remain immutable and no continuing task process is needed.
