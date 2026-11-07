# Native point-center inspection

Owners LMMV/dprada; source/owned-installed received2026-11-07;
[#142](https://github.com/uibcdf/pharmacophoremt/issues/142).
The source correction is implemented and passes338 selected cases, including16
new controls. Exact owned installed receiving passes the same338 bodies. The
[source receipt](evidence/point_inspection_source_20261107_summary.json) retains
the actual before/after source, tests, limits and failures.

A native Point has exactly its supplied position. Expose `Point.center` as a
read-only alias to the same canonical `position` quantity, including subclasses
and later valid position replacement. Do not store another coordinate, change
units or serialize an additional native field. InteractionSite's existing center
delegation can then serve ordinary public center and distance queries.

Keep bulk center queries in nm and encounter order, with shape(N,3), including
empty/filtered results. Only the empty case needs explicit coordinate columns;
do not reshape malformed nonempty inputs into plausible coordinates. Distances
retain the existing definition and units. No new molecular/numerical kernel,
Cylinder midpoint, Point radius or direction semantics are introduced. Broader
bulk-field admission and viewer/browser qualification retain their own scopes.

Protect normal calls without a digestion bypass, inherited Points, distinct
standard-unit contexts, known3-4-5geometry for points/spheres/mixed models,
empty selections/filters, source immutability and unchanged native JSON fields.
Run affected core, geometry, native I/O and RDKit projection controls. Preserve
the failing regression before correction; source and exact owned installed
receiving remain distinct from full supported current-head CI under#9/#23.
Use serial CPU19/backend1/nice19/idle I/O,512MiB DATA per process and pressure
checks; no owned aggregate cgroup is available. Do not alter a shared provider,
prefix or existing source checkpoint to hide an input/query defect.

## Source receiving and continuity

The original ordinary-call reproduction fails on Points and mixed models with
PUW-ERR-FORM-001 because the host passes None; Sphere controls succeed. The new
regression records13failures/3positive controls before correction, then all16pass.
A separate earlier setup attempt accidentally combined explicit plugin loading
with autoload; preserve that exit3 separately from the actual regression. The
corrected source selection uses explicit Pytest Receptor with autoload disabled.
All338 selected cases pass:16new inspection,3core,47curation,1original RDKit,
58projection,44native geometry,68native admission,43native diagnostics and58native
schema controls. Repeats do not add distinct cases. Native/schema/metadata and
nondefault-unit cases preserve their identities; no provider/prefix/native change.

The changed two runtime files conservatively change prepared-run source bindings.
Preserve original plans and databases; independent saved readers are separate
from reexecution. Frozen CI489be12 started before this fix and cannot qualify it.
The exact owned wheel and same338 bodies are now received; full current-head/installed/public/platform gates retain#9/#23 scope.


## Exact owned installed receiving

Producer858fe5a4d3d4ea61649479802721c80476ae4925 builds one owned
wheel0.4.0+151.g858fe5a. The [installed receipt](evidence/point_inspection_installed_20261107_summary.json)
authenticates210payload files/155nongenerated runtime files, and141loaded main
file modules/three namespaces resolve to that target. The same338 library bodies,
two original diagnostic/absence subprocess bodies and the unchanged RDKit recipe
pass outside the checkout. Copied test-only helper modules are explicitly admitted
from the fixture workspace; they are not wheel payload. Startup is isolated,
shared-provider files/native hash remain unchanged, and the qualified shared SDK
origin checker is reused. The original harness rejection of the extra curation
child remains preserved alongside its correction. This resolves#142's bounded
core defect, separately from full supported source/installed/public/platform
qualification. No new package release or general library integration is claimed.
