# Pharmer P1 external receiving declaration

Owners LMMV/dprada; 2026-11-09; [#164](https://github.com/uibcdf/pharmacophoremt/issues/164),
parent [#128](https://github.com/uibcdf/pharmacophoremt/issues/128).
This prepares the external arm of [P1](pharmer_p1_comparison.md); it does not
install, build or execute Pharmer. The original case/query and independent
positive/permutation/negative oracles remain unchanged. It is a case-specific
research declaration, not a public engine adapter or runtime dependency.

## Exact input and executable identity

The machine-readable [receiving declaration](../tests/data/pharmer_p1/external/receiving.json)
freezes source-derived commands, staged gates, explicit settings and unknowns.
The [export manifest](../tests/data/pharmer_p1/external/export_manifest.json)
binds three original SDF V2000 files, atom order/charges/frame/coordinates and
actual export provenance. All serialization/reading uses public MolSysMT tools;
PHMT has no new molecular parser or writer.

The source arm remains [standalone SVN r95](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/).
Eight additional source/build texts and the official binary README are captured
with response metadata and SHA-256. They supplement the original 24-file study;
neither selected-file capture is a complete reproducible build tree. Local raw
source remains in the owned evidence capsule; the tracked receipt publishes
identities and interpretation, not a new mirror or binary.

The official [file notice](https://sourceforge.net/projects/pharmer/files/)
warns that published executables need not track source. Its listed static binary
is dated 2014-12-18; r95 `main.cpp` is dated 2015-02-19. Consequently that binary
is not silently substituted for the selected source. No executable is on the
observed PATH, and no binary is downloaded. A qualified arm must bind one exact
command/path/hash to its source/compiler/linker/dependency context and execute
the same path that was checked. Neither a filename nor `--help` establishes that
build relationship. Pharmit and similarly named nonchemical tools are different
programs, not fallback routes.

## Build gate remains unreceived

The pinned [README](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/README)
describes Eclipse-generated builds, not a standard CMake recipe. The
[project configuration](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/.cproject)
selects legacy OpenBabel include paths and links JsonCpp, Boost, FastCGI/cgicc,
tcmalloc, OpenBabel, curl and smina; it defines OUTPUTSMINA and an Eigen stack
assertion switch. Documentation's historical compiler/version hints are not a
qualified modern dependency set. Observed local GCC15.2/Make4.4.1 and unsuccessful
configured pkg-config probes do not establish either ABI compatibility or global
library absence. No compilation or package-manager transaction is attempted.

Before a build, receive the complete pinned source and generated recipe, exact
compiler/flags/dependency artifact hashes and applicable licenses. Review optional
server/smina and ZINC-registration paths explicitly; record any configuration or
diagnostic-only patch instead of calling it unmodified r95. Keep original source,
patch, logs and produced file hash. Never repair global headers, install with sudo,
modify the shared prefix or substitute an unqualified OpenBabel ABI. Use one
compiler job and a separately admitted small resource pilot before a full build.

## Input identities and resource behavior

The three disconnected ions are geometric probes. They have Na/K/Li atom order,
formal charges +1, no bonds, one supplied frame and no conformer generation or
minimization. Their files have an empty title because native SDF has no single
molecule name for this three-component source. The r95
[reader](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/ReadMCMol.h)
groups consecutive equal-title records as conformers. Use **one separate database
per original case**, one untouched SDF record each, sequentially. This is a
receiving design, not a new claim of independent chemistry. Do not concatenate
same-title exports, rewrite CTAB text or infer case identity from an empty title.

The [CLI source](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/main.cpp)
can fork one creator per database directory. Loading spawns per-directory threads;
search multiplies worker count by directory count, with a coordinator as well.
Therefore `-nthreads=1` is a worker setting, not a one-task guarantee. One database
per process, one allowed CPU and actual task/group monitoring remain necessary.
Do not apply the README's host-wide file/map-limit suggestions to this workstation.

Export receiving uses the established DATA512MiB/AS1GiB per-process limits,
sampled own-group RSS cutoff512MiB, CPU19/backend1/nice19/idleIO,120CPU/180wall
seconds and20percent host reserve. Availability is not a reservation. No aggregate
kernel memory/swap/task/quota guarantee is claimed. The external compiler/engine
has not been measured under this profile; prefer an allocated enforced envelope,
start with help/perception/single-record DB pilots and stop on pressure/refusal.
No automatic budget increase, exhausted #148 retry or borrowed service is allowed.

## Commands, completeness and observable meaning

The declaration retains argv templates for help, default definitions, perception,
creation and search. Verify their syntax/effective values against the selected
binary before use. Keep output paths new and raw stdout/stderr/SDF immutable.
Search explicitly selects one worker, no conformer reduction, UINT_MAX hit/orientation
caps and `max-rmsd=0.3125` angstrom, equal to the P1 common physical radius. Any
complete equal-radius per-site placement satisfies that RMSD bound; this is no
unequal-radius or numerical-boundary equivalence test. A finite cap remains a cap:
reaching it, cancellation, omitted input or abnormal completion prevents a
complete-negative statement. Preserve indexed/searchable counts and all filters.

Perception must actually return exactly three size1 PositiveIon centers with no
extra features before search is interpreted. Source-side PHMT recognition cannot
supply that external observation. The
[JSON writer](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/pharmarec.cpp)
returns type, center, size, vectors, radius and requirement but no atom indices.
The [result writer](https://svn.code.sf.net/p/pharmer/code/!svn/bc/95/PharmerQuery.cpp)
returns CSV-like scores/record/location fields and fitted SDF, not complete native
query-feature correspondences. Coordinate association from these unique probes
is derived evidence, not an emitted engine membership. Full P1 mapping acceptance
therefore needs an independently admitted diagnostic path; otherwise retain an
unsupported-observation outcome or declare a distinct reduced-scope case. Do not
silently weaken the original P1 contract to label a partial output complete.

Retain separate unavailable/build/export/perception/database/search/output-mapping
outcomes. Only a completed, admitted search can produce a geometric nonmatch;
none of these stages predicts biological activity. Actual native candidate counts,
returned orientation multiplicity, RMSD, PHMT scores and performance remain distinct.

## Executed preparation and maintenance

The opt-in command `python -m devtools.prepare_pharmer_p1 --output-directory NEW`
claims a new directory before scientific imports and writes a complete manifest
as each case completes. Failed exports remain failures while later cases retain
their own outcomes. Existing files/directories are refused without replacement.
The first pilot's authored bitwise readback assertion fails solely on ordinary
unit-conversion roundoff and is retained. Readback now uses P1's existing absolute
1e-12nm tolerance, with no relative allowance; measured maximum error is
2.220446049250313e-16nm. Original source coordinates remain exactly unchanged.
There is no geometry, matching tolerance, provider or budget change.

All17selected source cases pass: five new export/lifetime/failure guards and12
original P1cases. The three original files are frozen after actual export/round-trip;
future exports must match those bytes as well as the independent physical answers.
The [source receipt](evidence/pharmer_p1_external_source_20261109.json) retains
those original results and the authored unit-assertion/lint recovery. The
[installed receipt](evidence/pharmer_p1_external_installed_20261109.json) then
receives the same17original bodies from source76ac909 around unchanged exact owned
wheel198/runtime b4b062a. All214payload/159runtime files,14fixtures and155loaded
runtime origins verify without PHMT checkout fallback. The complete export driver
also produces the same three frozen SDF byte payloads and refuses replacement;
source and installed producer-version labels retain their distinct identities.
Installed sampled own-group peak is362999808bytes. This closes preparation#164;
the external executable/build/perception/database/search/output-mapping gates
above remain unreceived or unexecuted under#128.
This route adds no shipped runtime code and needs no replacement wheel. Full
installed/public/platform, actual external execution, biology/performance and
release gates remain independent. Reassess on changes to original inputs,
serialization/provider/native context, executable/build, observations or resources.
