"""Compatibility entry point; implementation lives in unshipped test support."""

from phmt_test_support.audit_eralpha import (
    MANIFEST as MANIFEST,
)
from phmt_test_support.audit_eralpha import (
    ROOT as ROOT,
)
from phmt_test_support.audit_eralpha import (
    Counter as Counter,
)
from phmt_test_support.audit_eralpha import (
    Path as Path,
)
from phmt_test_support.audit_eralpha import (
    _observation as _observation,
)
from phmt_test_support.audit_eralpha import (
    _state as _state,
)
from phmt_test_support.audit_eralpha import (
    audit as audit,
)
from phmt_test_support.audit_eralpha import (
    get_features as get_features,
)
from phmt_test_support.audit_eralpha import (
    hashlib as hashlib,
)
from phmt_test_support.audit_eralpha import (
    json as json,
)
from phmt_test_support.audit_eralpha import (
    msm as msm,
)
from phmt_test_support.audit_eralpha import (
    np as np,
)
from phmt_test_support.audit_eralpha import (
    puw as puw,
)

if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
