# ERα binding source pool 3 — capacity declaration of 2026-10-28

Owner #66, LMMV/dprada. This declaration precedes new activity-resource
requests. The first two source pools and their terminal outcomes remain intact.
The existing query hashes, twenty independent groups per class, 1,000/10,000 nM
thresholds, endpoint separation, no-pooling and historical exclusions are unchanged.

## Nomination without a description filter

The [machine declaration](../tests/data/esr1_binding_evaluation/pool3_declaration_20261028.json)
contains every remaining single-protein assay from the two original, hash-verified
ChEMBL_37 discovery pages. Those pages contain 1,485 human CHEMBL206/B/9 records;
520 have `bao_format=BAO_0000357`. Excluding the 42 pool-2 assays and the three
previously reviewed sources leaves **475 nominees**, in numeric assay-ID order.
No new metadata or activity values are used to choose these nominees.

No description words are required or excluded. Recruitment, variants, relative
binding, single-concentration and incompletely described experiments can therefore
remain in this capacity census. A database annotation does not qualify an
orthosteric human ERα competition endpoint. The census excludes other annotated
formats and is not a review of every possible binding source.

The metadata pages remain in the original owned
`/tmp/phmt66-binding-metadata-20261024/`, with identities in
`tests/data/esr1_binding_evaluation/source_inventory.json`. The declaration retains
the nominated source projections and their separate
[ChEMBL notice](../tests/data/esr1_binding_evaluation/pool3_NOTICE.md).

## Capacity only; detailed acquisition remains a later stage

Request status once, requiring ChEMBL_37, then one `only=activity_id&limit=1`
response for each of the 475 nominees. Reuse the existing declared-pool
acquisition/reader rather than another fetch or classifier. Requests are sequential;
at most 476 requests are allowed, with the existing 60-second per-request timeout,
no automatic retries and no replacement. Record original URLs, timestamps,
response bytes/hashes, failures and acquisition producer in a new owned directory.

Every declared total must resolve before ranking. Unknown, failed, changed-version
or unexpected-projection responses stop acquisition; none becomes zero. Retain any
unexpected compound exposure and do not describe exposed values as unseen.
Fewer than 40 raw records cannot supply twenty disjoint groups per class.
Record all other assays, sorted by descending total then numeric assay ID, as
**pending capacity survivors**, without choosing detailed tables in this run.

`maximum_assays=0` explicitly prevents detailed activity acquisition. A nonempty
pending list is `capacity_survivors_require_source_review`, not a terminal negative
result. Capacity is only an upper bound; it establishes neither class balance nor
molecular independence. If there are no survivors, stop this bounded census.
Incomplete acquisition remains unresolved, even if some larger populations have
already been observed. Do not rank a partial census as a complete result.

## Next decision and molecular boundary

After a complete census, review the original experimental methods of capacity
survivors before any detailed-table request. Declare a finite source order,
experimental inclusion decisions and detailed acquisition budget in another dated
pre-data record. Ineligible recruitment/relative/variant endpoints cannot be
rescued by size. Preserve this census and both earlier pools if a different source
or study design is needed.

No activity values, labels, compound information, structures, preparation or
pharmacophore scores are requested here. The previous 25 ChEMBL identifiers,
8,099 CIDs and 149 unresolved historical rows remain exposed history. A later
eligible population still requires MolSysMT-owned identity/alias/scaffold checks
(#447) and preparation. #323/#375 do not block this source census, and this work
does not implement or qualify molecular directions or environmental refinement.

## Execution and qualification

```bash
python -m phmt_test_support.esr1_binding_pool2 \
  --declaration tests/data/esr1_binding_evaluation/pool3_declaration_20261028.json \
  --data-dir /new/owned/path/inputs --acquire --output /new/path/review.json
```

Omit `--acquire` for offline replay of the retained inputs. Defaults still replay
pool 2 with its original declaration/schemas. New guards cover a capacity survivor
with detailed acquisition disabled, declaration mismatch, misleading metadata and
the unchanged original-response replay. These are unshipped case-support tools;
no public scientific API, molecular engine, dependency floor or release changes.

Record actual acquisition/results and clean-producer identity separately after
this declaration is committed. The shared Python 3.14.7 environment's `pip check`
still fails on cross-suite requirements (including NumPy, PDB2PQR, Biopython and
newer editable support libraries). No environment repair or clean-install claim
is made. This standard-library source census imports no molecular provider.

Pre-acquisition local checks pass: 63 administrative unittest controls, the
separately executed strict full-Sphinx guard, three reporting tests, generated
indexes, whole-tree Ruff lint/format and whitespace checks. Acquisition is still
pending at this declaration checkpoint. Existing historical archives are unchanged;
no new full scientific matrix or installed-package qualification is claimed.
