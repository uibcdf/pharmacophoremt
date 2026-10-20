"""Compatibility entry point; implementation lives in unshipped test support."""

from phmt_test_support.evidence_archive import (
    Path as Path,
)
from phmt_test_support.evidence_archive import (
    _check_bytes as _check_bytes,
)
from phmt_test_support.evidence_archive import (
    argparse as argparse,
)
from phmt_test_support.evidence_archive import (
    gzip as gzip,
)
from phmt_test_support.evidence_archive import (
    hashlib as hashlib,
)
from phmt_test_support.evidence_archive import (
    json as json,
)
from phmt_test_support.evidence_archive import (
    main as main,
)
from phmt_test_support.evidence_archive import (
    re as re,
)
from phmt_test_support.evidence_archive import (
    read_archived_bytes as read_archived_bytes,
)
from phmt_test_support.evidence_archive import (
    read_archived_evidence as read_archived_evidence,
)

if __name__ == "__main__":
    raise SystemExit(main())
