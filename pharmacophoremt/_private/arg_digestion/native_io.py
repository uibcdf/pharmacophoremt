"""Closed native-I/O admission; path and scientific values keep their owners."""

from argdigest import DigestConfig, FunctionContract

CONTRACTS = [
    FunctionContract(caller=f"pharmacophoremt.io.phmt.{name}", admits="signature")
    for name in ("load_json", "load_yaml", "to_json", "to_yaml")
]

# Python open owns path/descriptor admission; native codec bodies own validated
# model/schema/quantity reconstruction. Do not normalize opaque values here.
CONFIG = DigestConfig(
    argument_digestion=False,
    standardizer=None,
    function_source=__name__,
    contract_owner="definition",
)
