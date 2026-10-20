"""Compatibility entry point; implementation lives in unshipped test support."""

from phmt_test_support.audit_legacy_cliques import (
    LegacyCliqueAuditHelpers as LegacyCliqueAuditHelpers,
)
from phmt_test_support.audit_legacy_cliques import (
    audit as audit,
)
from phmt_test_support.audit_legacy_cliques import (
    json as json,
)
from phmt_test_support.audit_legacy_cliques import (
    np as np,
)
from phmt_test_support.audit_legacy_cliques import (
    nx as nx,
)

if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
