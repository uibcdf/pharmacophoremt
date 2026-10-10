"""Guard retired molecular backends while keeping PHMT's own model codecs."""

import ast
import importlib
from pathlib import Path

import pytest

import pharmacophoremt

ROOT = Path(pharmacophoremt.__file__).resolve().parent
RETIRED_MODULES = (
    "pharmacophoremt.utils.alignment",
    "pharmacophoremt.utils.chemistry",
    "pharmacophoremt.utils.conformers",
    "pharmacophoremt.utils.maths",
    "pharmacophoremt.utils.preparation",
    "pharmacophoremt.data.ligand_sets.read_sdf",
)


@pytest.mark.parametrize("name", RETIRED_MODULES)
def test_retired_molecular_modules_cannot_be_imported(name):
    # Normal editable installation; no path override or provider substitution.
    with pytest.raises(ModuleNotFoundError) as caught:
        importlib.import_module(name)
    assert caught.value.name in (name, "pharmacophoremt.utils")


def test_package_has_no_runtime_imports_of_retired_backends():
    violations = []
    for path in ROOT.rglob("*.py"):
        package = "pharmacophoremt." + ".".join(path.relative_to(ROOT).parts[:-1])
        package = package.rstrip(".")
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    base = importlib.util.resolve_name("." * node.level + base, package)
                names = [base, *[base + "." + alias.name for alias in node.names]]
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if (
                    node.func.attr == "import_module"
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                ):
                    names = [node.args[0].value]
            for name in names:
                if isinstance(name, str) and (
                    name == "pharmacophoremt.utils"
                    or name.startswith("pharmacophoremt.utils.")
                    or name == RETIRED_MODULES[-1]
                ):
                    violations.append((str(path.relative_to(ROOT)), node.lineno, name))
    assert not violations, violations


def test_pharmacophore_codecs_and_native_consumers_remain_available():
    for name in (
        "pharmacophoremt.io.rdkit",
        "pharmacophoremt.io.sdf",
        "pharmacophoremt.modeler.features",
        "pharmacophoremt.screening.alignment",
        "pharmacophoremt.screening.virtual_screening",
    ):
        assert importlib.import_module(name).__file__
