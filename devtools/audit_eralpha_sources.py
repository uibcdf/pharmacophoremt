"""Compatibility entry point; implementation lives in unshipped test support."""

from phmt_test_support.audit_eralpha_sources import (
    ROOT as ROOT,
)
from phmt_test_support.audit_eralpha_sources import (
    Counter as Counter,
)
from phmt_test_support.audit_eralpha_sources import (
    Path as Path,
)
from phmt_test_support.audit_eralpha_sources import (
    audit as audit,
)
from phmt_test_support.audit_eralpha_sources import (
    get_features as get_features,
)
from phmt_test_support.audit_eralpha_sources import (
    hashlib as hashlib,
)
from phmt_test_support.audit_eralpha_sources import (
    json as json,
)
from phmt_test_support.audit_eralpha_sources import (
    msm as msm,
)
from phmt_test_support.audit_eralpha_sources import (
    np as np,
)
from phmt_test_support.audit_eralpha_sources import (
    puw as puw,
)

if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
