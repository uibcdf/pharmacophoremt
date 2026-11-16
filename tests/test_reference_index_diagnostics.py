"""Shared integer validation keeps the owning public argument in diagnostics."""

import numpy as np
import pytest

from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError

OWNERS = [
    (_contracts.digest_structure_index, "structure_index"),
    (_contracts.digest_reference_index, "reference_index"),
]


@pytest.mark.parametrize("digester,argument", OWNERS)
@pytest.mark.parametrize("value", [-1, True, np.bool_(False), 0.5, "0", None])
def test_invalid_nonnegative_index_names_its_actual_owner(digester, argument, value):
    with pytest.raises(ArgumentError) as caught:
        digester(value)
    assert caught.value.extra["argument"] == argument
    assert argument in str(caught.value)


@pytest.mark.parametrize("digester,argument", OWNERS)
@pytest.mark.parametrize("value", [0, np.int64(2), np.uint64(2**63)])
def test_valid_integer_normalization_retains_domain_and_python_type(
    digester, argument, value
):
    result = digester(value)
    assert type(result) is int and result == int(value)
