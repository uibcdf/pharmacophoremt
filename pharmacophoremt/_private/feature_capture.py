"""Observed request/content binding, using the existing quantity/native owners."""

import hashlib

from pharmacophoremt_features import _payload_schema as spec
from pharmacophoremt_features import _schema
from pharmacophoremt_features._diagnostics import FeatureAssetError, fail

SCHEMA = "pharmacophoremt.feature-capture@1"
EVALUATION_SCHEMA = "pharmacophoremt.feature-evaluation@1"
PRODUCER_SCHEMA = "pharmacophoremt.feature-extraction-observation@1"
PROVENANCE_SCHEMA = "pharmacophoremt.feature-capture-provenance@1"
OPERATION = "pharmacophoremt.modeler.get_features"
FAMILIES = _schema.FAMILIES + ("included volume",)


def require(condition):
    if not condition:
        fail(339)


def families(values):
    require(type(values) in (list, tuple) and bool(values))
    require(all(type(k) is str and k in FAMILIES for k in values))
    return [k for k in FAMILIES if k in values]


def _inventory(inventory, evaluation):
    requested = evaluation["families"]
    require(requested == families(requested))
    require(evaluation["definition"] == inventory.get("definition"))
    for key in ("selected_atom_indices", "structure_index", "chemical_state"):
        require(_schema.encoded(evaluation[key]) == _schema.encoded(inventory.get(key)))
    coverage = spec.inventory_layout(
        inventory, evaluation["n_atoms"], requested, records=False, allow_volume=True
    )
    require(_schema.encoded(evaluation["coverage"]) == _schema.encoded(coverage))
    from .native_feature_payload import _capability, _validate_native

    _capability()
    try:
        _validate_native(inventory, allow_volume=True)
    except FeatureAssetError:
        raise
    except Exception as error:
        raise FeatureAssetError(code="PHMT-E332") from error


def binding(inventory, evaluation, producer):
    """Seal quantities through the existing representation, never strip units."""
    spec.provenance(
        inventory["recognition"], inventory.get("attribution"), evaluation, producer
    )
    from .molsysmt import detached

    raw = _schema.encoded(
        {
            "inventory": detached(inventory),
            "evaluation": evaluation,
            "producer": producer,
        }
    )
    if len(raw) > _schema.MAX_PAYLOAD_BYTES:
        fail(333)
    return hashlib.sha256(raw).hexdigest()


def validate(capture):
    require(
        type(capture) is dict
        and set(capture)
        == {"schema", "inventory", "evaluation", "producer", "capture_sha256"}
    )
    require(capture["schema"] == SCHEMA)
    inventory, evaluation, producer = (
        capture[k] for k in ("inventory", "evaluation", "producer")
    )
    require(
        type(inventory) is dict and type(evaluation) is dict and type(producer) is dict
    )
    spec.provenance(evaluation, producer)
    require(
        set(evaluation)
        == {
            "schema",
            "status",
            "operation",
            "definition",
            "families",
            "coverage",
            "n_atoms",
            "selected_atom_indices",
            "structure_index",
            "chemical_state",
            "coordinate_policy",
        }
    )
    require(
        evaluation["schema"] == EVALUATION_SCHEMA
        and evaluation["status"] == "completed"
        and evaluation["operation"] == OPERATION
        and evaluation["coordinate_policy"] == "cartesian-no-imaging"
    )
    require(
        set(producer)
        == {
            "schema",
            "operation",
            "distribution_version",
            "runtime_version",
            "observed_extractor_sha256",
            "versions",
        }
    )
    require(
        producer["schema"] == PRODUCER_SCHEMA and producer["operation"] == OPERATION
    )
    for key in ("distribution_version", "runtime_version"):
        require(
            producer[key] is None
            or (type(producer[key]) is str and bool(producer[key]))
        )
    if producer["observed_extractor_sha256"] is not None:
        try:
            _schema.digest(producer["observed_extractor_sha256"])
        except FeatureAssetError as error:
            raise FeatureAssetError(code="PHMT-E339") from error
    require(
        type(producer["versions"]) is dict
        and set(producer["versions"])
        == {"pharmacophoremt", "molsysmt", "numpy", "pyunitwizard"}
    )
    require(
        all(
            v is None or (type(v) is str and bool(v))
            for v in producer["versions"].values()
        )
    )
    _inventory(inventory, evaluation)
    require(capture["capture_sha256"] == binding(inventory, evaluation, producer))
    return inventory, evaluation, producer
