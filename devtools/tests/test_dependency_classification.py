"""Dependency classification agrees with the actual installed-package contract."""

import ast
import tomllib
import unittest
from pathlib import Path

from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parents[2]


class TestDependencyClassification(unittest.TestCase):
    def test_public_tables_own_a_python_314_compatible_pandas_dependency(self):
        metadata = tomllib.loads((ROOT / "pyproject.toml").read_text())
        requirements = {
            requirement.name.lower(): requirement
            for requirement in map(Requirement, metadata["project"]["dependencies"])
        }
        # MolSysMT/test-only availability cannot replace this direct contract.
        self.assertIn("pandas", requirements)
        self.assertTrue(requirements["pandas"].specifier.contains("2.3.3"))
        self.assertFalse(requirements["pandas"].specifier.contains("2.3.2"))
        self.assertTrue(requirements["pandas"].specifier.contains("3.0.0"))
        tree = ast.parse((ROOT / "pharmacophoremt/_depdigest.py").read_text())
        declaration = next(
            node.value
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "LIBRARIES"
                for target in node.targets
            )
        )
        pandas = ast.literal_eval(declaration)["pandas"]
        self.assertEqual(pandas["type"], "hard")
        self.assertEqual(pandas["pypi"], "pandas")
        self.assertEqual(pandas["conda"], "pandas")
        self.assertEqual(pandas["channel"], "conda-forge")

    def test_yaml_runtime_codec_is_declared_directly(self):
        metadata = tomllib.loads((ROOT / "pyproject.toml").read_text())
        required = {
            Requirement(value).name.lower()
            for value in metadata["project"]["dependencies"]
        }
        self.assertIn("pyyaml", required)
        yaml_requirement = next(
            Requirement(value)
            for value in metadata["project"]["dependencies"]
            if Requirement(value).name.lower() == "pyyaml"
        )
        self.assertTrue(yaml_requirement.specifier.contains("5.1"))
        self.assertFalse(yaml_requirement.specifier.contains("5.0"))
        tree = ast.parse((ROOT / "pharmacophoremt/_depdigest.py").read_text())
        declaration = next(
            node.value
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "LIBRARIES"
                for target in node.targets
            )
        )
        libraries = ast.literal_eval(declaration)
        self.assertEqual(libraries["yaml"]["type"], "hard")
        self.assertEqual(libraries["yaml"]["pypi"], "PyYAML")

    def test_required_nglview_is_classified_as_hard(self):
        metadata = tomllib.loads((ROOT / "pyproject.toml").read_text())
        required = {
            Requirement(value).name.lower()
            for value in metadata["project"]["dependencies"]
        }
        self.assertIn("nglview", required)
        tree = ast.parse((ROOT / "pharmacophoremt/_depdigest.py").read_text())
        declaration = next(
            node.value
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "LIBRARIES"
                for target in node.targets
            )
        )
        libraries = ast.literal_eval(declaration)
        self.assertEqual(libraries["nglview"]["type"], "hard")
        self.assertEqual(libraries["nglview"]["pypi"], "nglview")
        self.assertEqual(libraries["molsysviewer"]["type"], "soft")
        self.assertEqual(libraries["ackredit"]["type"], "soft")
