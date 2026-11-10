# Retrieval-driver interruption controls

This analytical developer-tool case, owned by LMMV/dprada under
[issue183](https://github.com/uibcdf/pharmacophoremt/issues/183), checks that an
interrupted experiment retains the last committed scientific progress and its
observed references. It follows [six-family controls](typed_retrieval.md).
The [receipt and original archive](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/retrieval_checkpoints_20261110.json)
retain the new evidence separately from earlier runs.

## Question and controls

Both opt-in retrieval drivers previously wrote progress during science but saved
actual application-session attribution only at the end. Four original controls
reproduce the missing `actual_attribution` field after a completed native call.
One private application-owned checkpoint composition now saves progress and the
public Ackredit session payload together, using local atomic file replacement.

Eighteen controls pass per source/exact-owned218 context. Controlled own children
use the existing frozen analytical snapshots and two actual native calls: a
positive and a completed-empty result under nm/pm application policies. These
small injected prefixes test driver persistence; they are not full analytical
experiments. No molecular preparation or external chemical database is involved.

| Control | Received behavior |
| --- | --- |
| SIGTERM/SIGKILL after a committed native prefix | Original saved JSON and actual bibliography remain unchanged; running means incomplete |
| SIGKILL before replacement | Previous target remains intact despite later uncommitted work |
| Normal positive/empty nm/pm prefixes | Scientific mappings and completion remain explicit |
| Scientific exception after a completed native prefix | Original error type/reason and failed policy remain, with completed science and observed references |
| Attribution export failure | Latest science remains; prior successful credit/sequence or null is explicitly unavailable |
| Invalid scientific JSON or replacement failure | Failure propagates and previous target remains unchanged |
| Existing output or invalid admission | Original caller bytes remain untouched |

No signal handler delays termination. The added checkpoint record identifies the
committed sequence and observed attribution scope. Uncommitted/in-flight work is
unknown; an unavailable or null export does not establish zero citable work.
Reading/exporting the real provider snapshot creates no new reference use.

## Complete experiment receiving — 2026-11-10 UTC

Separate complete driver executions receive 24 ordinary and 72 six-family
query/width/unit-policy combinations in each source/exact-owned218 context.
Original scientific projections and complete actual bibliography/uses agree:
ordinary sessions retain eight references/eight uses, and six-family sessions
retain eight references/twelve uses. The original numerical candidate-band
differences remain distinct from exact physical pair checks and final acceptance.

All 214 wheel payloads, 159 unchanged scientific runtime bodies, 4594 provider
Python files/native identity and 62 final case files verify. Tests/full drivers
load 144/146 PHMT module origins respectively, with no molecular operation.
Source/editable/owned version labels remain independent from admitted bodies.
The new helper and guards are unshipped developer support.

The old #182 interrupted result remains unchanged: its unsaved original
attribution stays unknown. New successful runs do not restore that earlier
session or rewrite the original 20+4 scientific composite.

## Reproduce and limits

The [contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/retrieval_driver_checkpoints.md)
and [guard](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/test_driver_checkpoints.py)
retain the exact scope. Admit a compatible environment and shared-machine
resources before running the focused tests or either complete opt-in driver:

```bash
python -m pytest --receptor=llm tests/test_driver_checkpoints.py
```

The received route uses Python 3.14, one CPU/backend thread, low CPU/I/O priority
and unchanged conservative memory/pressure stops. There is no automatic resume,
final cancellation-status inference, general filesystem/journal API or resource
manager. Before the first commit the reserved output may be empty. Hard termination
can leave a nonauthoritative temporary file. Local POSIX atomic replacement does
not qualify power-loss durability, network filesystems or concurrent writers.

No performance, production-index, biological, human-usability or public-platform/
release claim follows. Next define equivalent build/storage/cold/repeated-query
workloads and resource admission before measuring costs. #148/#165 remain stopped.
