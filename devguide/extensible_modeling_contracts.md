# Growth contracts and order of implementation

The accepted direction is broad pharmacophoric modeling built on independently
usable tools. The immediate acceptance gate is executing conventional workflows
reliably. Advanced methods remain objectives; they do not justify skipping the
classical controls or implementing speculative infrastructure first.

## Keep the scientific boundaries separate

MolSysMT owns molecular input, topology/chemical states, recognition, coordinate
access, preparation, molecular geometry and transformations. PharmacophoreMT
owns pharmacophoric hypotheses, constraints, correspondence, matching and scores.
TopOMT supplies pocket analysis, DockingMT supplies docking workflows and
MolSysViewer displays the resulting molecular scene and model. Provider gaps
belong in the owning library instead of a second local implementation.

`Feature + Shape` remains a useful site representation, but is not the whole
scientific model. Growth needs stable site identities, explicit source mappings,
relations and joint/logical constraints, reference frames, uncertainty and
provenance. Ensembles and temporal models should reference these objects instead
of requiring incompatible replacements. These are design requirements; the
current site lists and hardcoded serializer branches do not implement them all.

Separate the tools for chemical participant extraction, hypothesis construction,
correspondence search, alignment, geometric evaluation and scoring. Version each
scientific definition that changes a result. One-to-one assignment with essential
sites and weighted coverage is one declared method, not a universal meaning of
every pharmacophore. A new strategy may require relations, alternative matches,
densities or probabilistic constraints while reusing source and geometry tools.

Extend feature/shape vocabularies together with validated schemas, matching
capabilities and portable serialization. Unknown extensions must remain explicit;
do not silently flatten them to spheres or drop their scientific meaning.
Registered extensions are a later implementation step, not currently supported.

## Independent method, compute and execution choices

There are three axes: scientific method; compute backend (reference CPU, Rust,
future GPU); and execution plan (local, bounded chunks, parallel, distributed).
A faster backend must preserve the chosen scientific contract. Molecular backend
selection stays inside MolSysMT. PharmacophoreMT may accelerate its own measured
matching/scoring bottlenecks.

At numerical boundaries, normalize lengths to a declared unit, use arrays and
packed memberships, and keep chemical recognition and provider calls outside
numerical kernels. Return inspectable assignments and physical result units,
retain executed method/backend versions and precision, and define deterministic
tie handling and numerical tolerances. Batching must preserve input identity and
failure state; failed calculations never become zero-valued scientific negatives.

First establish a reference implementation and realistic profiling cases. Then
use Rust where measurements justify it, with reference-equivalence and memory
controls. GPU/distributed execution also needs deterministic reduction, bounded
memory and scientifically equivalent results before adoption. None is required
for the present reference-ligand slice; no accelerated PHMT backend is claimed.

## Classical gate before advanced generations

Complete native prepared-ligand search/alignment, observed-complex construction,
ligand/complex consensus and pocket-derived hypotheses with independent positive
and negative controls. Persist models, inspect them in the shared viewer, evaluate
actives/decoys without data leakage and execute the selected vertical pilots.
Preparation policies (pH, salts, protonation, tautomers) must be explicit scientific
choices delegated to MolSysMT, not unconditional hidden transformations.

Inactive compounds provide negative evidence; an inactive-only chemical feature
does not by itself identify a steric excluded volume. Steric exclusions need
receptor/geometry evidence, while antitarget or inactive constraints require their
own scientifically justified negative model.

After the classical gate, the roadmap retains dynamic pharmacophores and kinetic
models, peptide/macrocycle hierarchy, covalent geometry, water networks, ESP/density
representations, graph/tensor exports, generative design, multiobjective modeling
and large-scale screening. Their contracts should extend the common data and
tool boundaries, with their own observable acceptance controls.

Retain alternative scientific strategies when particular tests or benchmarks
favor another. Document the observed preference with inputs, parameters, objective,
coverage/alternatives and resource evidence. A bounded comparison does not establish
universal superiority or justify removing other implemented scientific options.
