# Native I/O ArgDigest receiving readiness

Reviewed 2026-11-04 at `6dc3da62a5d4623b6c22617b8d528582a52b1f79`, under
[#6](https://github.com/uibcdf/pharmacophoremt/issues/6) and
[#82](https://github.com/uibcdf/pharmacophoremt/issues/82).
**Migration is not activated.** Original candidate probes reproduce provider
violations; passing legacy controls are not evidence that these violations are
fixed. No runtime, dependency, provider, prefix, SDK or scientific input changes.

## Measured gate failures

1. Closed JSON/YAML functions wrapped with public ArgDigest 0.17.0 change eight
   of twelve TypeError refusals to UnknownArgumentError outside that family.
   Unknown keywords and False skip controls change; True bypass reaches the
   original closed callable. Both refuse input, but legacy catch compatibility
   differs. This needs supported provider policy or an explicit accepted API
   migration, not a local error/contract engine.
2. A literal option named like VAR_KEYWORD is flattened twice. An opaque value
   disappears; a mapping becomes top-level options and can overwrite an explicit
   named parameter. An ordinary option and True-bypass contrast controls preserve
   the examples. The defect occurs before normalization/domain admission.
3. The second defect reaches current PHMT model dispatch. With an endpoint spy,
   `model(original, method='reference-ligand', kwargs={'molecular_system': other})`
   reaches the endpoint with `other`. This is a measured argument-routing defect,
   not molecular recognition or a biological result. It remains open under #82.

Generic binding, normalization and refusal policy belong in ArgDigest. Molecular
forms/options/calculations belong in MolSysMT. Renaming a variadic parameter,
copying validation rules or using private provider patches does not qualify the
public contract. The runtime I/O functions remain unchanged while this gate fails.

## Existing compatibility protected

[Focused legacy controls](../tests/test_native_io_admission.py) preserve:

- TypeError refusal before file/model work, including unsupported skip controls;
- missing/duplicate call binding; original str/Path/custom PathLike/bytes routes;
- existing direct descriptor behavior delegated to Python open;
- raw molecular option key/value identity, including literal kwargs mappings,
  potential name collisions and explicit False/True controls;
- dispatcher string-only PHMT-E109 refusal and application unit policy.

Provider spies assert routing/result identity only and supply no chemical answers.
Existing real molecular dispatch, parser/encoder/filesystem, native schema/value,
diagnostic and dispatcher-contract controls supply their separate regression scope.
The [receipt/full original evidence](evidence/native_io_admission_readiness_20261104_summary.json)
retains candidate/current-consumer probes, exact sources, provider/native identity,
legacy outputs and recorded test selection. No full-suite, installed/public,
all-platform, fixed-provider or predictive qualification follows.

## Published provider issues

The [authorized destination/title/body record](evidence/native_io_argdigest_issue_drafts_20261104.json)
retains the exact two reviewed drafts and their published issue identities.
The user explicitly authorized publication on 2026-11-04. Both issues have the
registered `component:pharmacophoremt` label. Provider source is unchanged.

### 1. Literal keyword matching **kwargs parameter is expanded twice and can overwrite named arguments

Owning issue: [ArgDigest #47](https://github.com/uibcdf/argdigest/issues/47).

```python
from argdigest import arg_digest, DigestConfig

@arg_digest(config=DigestConfig(argument_digestion=False, standardizer=None))
def delegate(file_name, **kwargs):
    return file_name, kwargs

delegate('original', kwargs={'file_name': 'changed'})
# Expected: ('original', {'kwargs': {'file_name': 'changed'}})
# Actual:   ('changed', {})
```

Request: fix provider flattening and preserve literal option identity/named
parameters, ordinary domain/alias enforcement and bypass parity. Cover current
model-source routing and assess other suite consumers before rollout.

### 2. Support TypeError-compatible contract refusals when adopting existing Python I/O APIs

Owning issue: [ArgDigest #48](https://github.com/uibcdf/argdigest/issues/48).

Request: a supported provider-owned way to retain TypeError catches with
ArgDigest diagnostics/domain enforcement. The exact draft includes a minimal
original/decorated comparison. It is a compatibility request, distinct from the
first defect. Eight measured family changes are not eight separate defects.

## Publication and continuation

Two earlier creation attempts were rejected pending explicit destination
authorization; neither created an issue. After reviewing the concrete drafts,
the user authorized both publications. The exact drafts were published as #47
and #48; no alternative route or provider source change was used.

The bounded cross-repository refresh preserves the four consumer work files;
ArgDigest's clean clone is six documentation commits behind origin/main and
remains unmerged. Those upstream commits do not change the provider runtime;
the measured published 0.17.0 artifact remains the receiving subject.

Provider correction/publication and consumer receiving are separate next
steps. The current model-source routing defect must pass an adversarial regression
before being described as repaired. #82 and broader #6 remain open; scientific
sensitivity and #66/#74/installed/public gates retain their own scope.

Owned capsule: `/tmp/phmt-native-admission-20261104-9_parngb`, LMMV/dprada, review
2026-11-18 or provider readiness. Borrowed sources/prefixes remain unchanged;
no continuing local process is needed.
