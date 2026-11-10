# Reuse prepared feature inventories

Extract features once when you want to compare several queries against the same
unchanged prepared input. The [modular rigid-tools recipe](../cookbook/modular_rigid_tools.md#reuse-one-prepared-source-across-queries)
uses public `modeler.get_features()`, correspondence and placement operations.
The caller retains the prepared source and declares the same selection, frame,
chemical state and requested feature families for reuse. This is the current
supported development-source composition; its installed/public qualification
has the scope recorded in the linked recipe and installation guide.

A feature inventory describes participants and geometry. It carries the original
feature ordering and atom mappings. A query describes what to match. A saved run
also binds that query, effective settings, preparation declarations and producer
context. Changing a query can leave an inventory useful while requiring a new run.

## Decide what needs new work

| What changed? | Action |
| --- | --- |
| Only the query or its tolerance, with the prepared source and feature request unchanged | Reuse the inventory through supported modular operations. Create a new saved plan/run for changed query/settings. |
| Coordinates, chemical state, conformer, selection or atom mapping | Obtain the new prepared input through MolSysMT and extract features for it. Keep its original correspondence and preparation evidence. |
| Requested feature families or their definition | Capture the new request, including families that return no features. Missing observed kinds do not prove they were requested. |
| Source names/occurrences or order | Preserve each original occurrence and mapping. Equal names or coordinates do not authorize merging records. A changed saved manifest requires a new run. |
| A saved run has unfinished work under the same exact contract | Resume it using the documented recoverable-run workflow. Confirmed results remain original. |
| A request fails, lacks required context or stops before covering all work | Keep failures and pending work explicit. They are not zero-score negatives. |
| You only need to inspect or export historical results | Use the independent saved-result reader; current molecular providers need not repeat the calculation. |

The [saved-plan inspection recipe](../cookbook/prepared_run_plan_inspection.md)
shows the original query identity and resolved context before execution.
[Recoverable screening](../cookbook/recoverable_prepared_screening.md) explains
when to resume and when to create a new linked run. Keep old results and their
producer versions as originally recorded.

## What a compatible cache must establish

A feature list with valid geometry does not verify its origin. Current manual
reuse assumes the source, state, frame, selection and requested families remain
unchanged. Keep the preparation and original source/occurrence information with
your application. Source pointers, filenames and version labels are insufficient
for automatic persistent reuse.

A [bounded snapshot study](../validation/feature_snapshots.md) now checks native
capture, structural inspection and explicit quantity reconstruction. It remains
an unshipped prototype. The [ingestion study](../validation/snapshot_retrieval.md)
now checks that finite candidate retrieval preserves original snapshot/work maps
and refuses changed bindings. Its [six-family extension](../validation/typed_retrieval.md)
checks full three/four-point queries and keeps numerical boundary proposals
separate from later orientation/pose acceptance. Persistent public snapshots and automatic compatibility
preflight retain their own acceptance gates. The [developer contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/prepared_feature_snapshot_contract.md)
requires a verified prepared parent, explicit request coverage, complete ordered
feature evidence, units and predicate/producer compatibility. Molecular source
preparation and collection lifetimes remain MolSysMT-owned. The planned guided
and expert routes must expose the same decision and evidence.

The [finite retrieval study](../validation/retrieval_controls.md) preserves its
declared reference mappings, but its numerical domain and build/query costs need
further qualification before a production index is selected. Candidate retrieval
still needs later fitting/final evaluation; geometric matching does not establish
binding activity. The contract does not add a public snapshot API or change the
current saved-run format.
