"""Offline refusal guards for the fixed #148 receiving client; no native work."""

import argparse
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from devtools import feature_reuse_native_qualification as client


class NativeQualificationTests(unittest.TestCase):
    def test_manager_refuses_implicit_concurrency_before_any_child(self):
        with (
            patch.dict(
                os.environ,
                {"MAMBA_EXTRACT_THREADS": "0", "MAMBA_DOWNLOAD_THREADS": "1"},
            ),
            patch.object(client.subprocess, "check_output") as child,
        ):
            with self.assertRaisesRegex(ValueError, "explicit serial"):
                client.manager_controls(Path("unused"))
            child.assert_not_called()

    def test_manager_binary_drift_refuses_before_config_or_installation(self):
        with (
            patch.dict(
                os.environ,
                {"MAMBA_EXTRACT_THREADS": "1", "MAMBA_DOWNLOAD_THREADS": "1"},
            ),
            patch.object(
                client, "identity", return_value={"bytes": 1, "sha256": "0" * 64}
            ),
            patch.object(client.subprocess, "check_output") as child,
        ):
            with self.assertRaisesRegex(ValueError, "reviewed official binary"):
                client.manager_controls(Path("unused"))
            child.assert_not_called()

    def test_manager_effective_defaults_or_wrong_controls_are_refused(self):
        for controls in (
            {"extract_threads": 0, "download_threads": 5},
            {"extract_threads": 1, "download_threads": 5},
            {"extract_threads": True, "download_threads": 1},
            {"extract_threads": 1},
        ):
            with (
                self.subTest(controls=controls),
                patch.dict(
                    os.environ,
                    {"MAMBA_EXTRACT_THREADS": "1", "MAMBA_DOWNLOAD_THREADS": "1"},
                ),
                patch.object(
                    client,
                    "identity",
                    return_value={"bytes": 14606408, "sha256": client.MANAGER_SHA},
                ),
                patch.object(
                    client.subprocess,
                    "check_output",
                    side_effect=["1.5.10\n", json.dumps(controls)],
                ),
            ):
                with self.assertRaisesRegex(ValueError, "concurrency must equal one"):
                    client.manager_controls(Path("unused"))

    def test_exact_manager_reports_verified_serial_controls(self):
        identity = {"bytes": 14606408, "sha256": client.MANAGER_SHA}
        with (
            patch.dict(
                os.environ,
                {"MAMBA_EXTRACT_THREADS": "1", "MAMBA_DOWNLOAD_THREADS": "1"},
            ),
            patch.object(client, "identity", return_value=identity),
            patch.object(
                client.subprocess,
                "check_output",
                side_effect=[
                    "1.5.10\n",
                    '{"extract_threads": 1, "download_threads": 1}',
                ],
            ),
        ):
            self.assertEqual(
                client.manager_controls(Path("owned-manager")),
                {
                    "manager": identity,
                    "version": "1.5.10",
                    "controls": {"extract_threads": 1, "download_threads": 1},
                },
            )

    def test_services_use_supported_group_oom_policy_and_owned_cleanup_root(self):
        import yaml

        workflow = yaml.load(
            (
                client.ROOT
                / ".github/workflows/feature_reuse_native_qualification.yaml"
            ).read_text(),
            Loader=yaml.BaseLoader,
        )
        steps = workflow["jobs"]["native"]["steps"]
        services = [s["run"] for s in steps if "systemd-run" in s.get("run", "")]
        self.assertEqual(len(services), 2)
        self.assertIn("--setenv=MAMBA_EXTRACT_THREADS=1", services[0])
        self.assertIn("--setenv=MAMBA_DOWNLOAD_THREADS=1", services[0])
        for body in services:
            # systemd.service OOMPolicy=kill owns memory.oom.group=1;
            # MemoryOOMGroup is not a supported transient-service assignment.
            self.assertIn("--property=OOMPolicy=kill", body)
            self.assertNotIn("--property=MemoryOOMGroup=", body)
        setup = next(
            i
            for i, step in enumerate(steps)
            if step.get("uses", "").startswith("mamba-org/setup-micromamba@")
        )
        self.assertEqual(
            steps[setup - 1]["run"],
            'mkdir -p -- "$RUNNER_TEMP/phmt148-native-mamba"',
        )
        self.assertEqual(steps[setup]["with"]["post-cleanup"], "all")

    def test_changed_client_refuses_before_any_route_or_scope_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            with (
                patch.dict(
                    os.environ,
                    {
                        "RUNNER_TEMP": temporary,
                        "PHMT148_NATIVE_CLIENT_SHA256": "0" * 64,
                    },
                ),
                patch.object(client, "fixed_inputs") as declarations,
                patch.object(client, "own_scope") as scope,
            ):
                with self.assertRaisesRegex(ValueError, "reviewed workflow binding"):
                    client.main(
                        [
                            "native",
                            "--output",
                            temporary,
                            "--unit",
                            "unused",
                            "--cpu",
                            "0",
                            "--uid",
                            str(os.getuid()),
                            "--gid",
                            str(os.getgid()),
                        ]
                    )
                declarations.assert_not_called()
                scope.assert_not_called()

    def test_stopped_route_refuses_revised_dependencies_without_scientific_imports(
        self,
    ):
        import sys

        before = set(sys.modules)
        # #207 advances the main CI reader. The frozen #148 client retains its
        # original dependency fingerprint and must refuse before installation.
        self.assertNotEqual(
            client.identity(client.ROOT / client.SOURCE_INPUT)["sha256"],
            client.SOURCE_SHA,
        )
        with self.assertRaisesRegex(ValueError, "pinned dependency input"):
            client.fixed_inputs()
        added = set(sys.modules) - before
        self.assertFalse(
            any(
                name.split(".")[0] in {"pharmacophoremt", "molsysmt", "numpy", "openmm"}
                for name in added
            )
        )

    def test_changed_original_guard_is_refused(self):
        original = client.identity

        def changed(path):
            result = original(path)
            if str(path).endswith(client.SOURCE_INPUT):
                # Reach the downstream guard in this unit control using the
                # frozen admitted fingerprint, without changing real inputs.
                result = {**result, "sha256": client.SOURCE_SHA}
            if str(path).endswith(client.SELECTORS[0]):
                result = {**result, "sha256": "0" * 64}
            return result

        with patch.object(client, "identity", changed):
            with self.assertRaisesRegex(ValueError, "original native guard changed"):
                client.fixed_inputs()

    def test_changed_probe_source_is_refused(self):
        with patch.object(
            client, "identity", return_value={"bytes": 1, "sha256": "0" * 64}
        ):
            with self.assertRaisesRegex(ValueError, "resource-probe"):
                client.fixed_inputs()

    def test_changed_pinned_input_is_refused(self):
        original = client.identity

        def changed(path):
            result = original(path)
            if str(path).endswith(client.SOURCE_INPUT):
                result = {**result, "sha256": "0" * 64}
            return result

        with patch.object(client, "identity", changed):
            with self.assertRaisesRegex(ValueError, "pinned dependency"):
                client.fixed_inputs()

    def sample(self):
        return {
            "memory": {"MemTotal": 16 * 1024**3, "MemAvailable": 14 * 1024**3},
            "memory_psi": "some avg10=0.00\nfull avg10=0.00\n",
            "unit_memory_psi": "some avg10=0.00\nfull avg10=0.00\n",
            "swap_pages": {"pswpin": 0, "pswpout": 0},
        }

    def test_reserve_includes_full_phase_budget_and_supervisor_margin(self):
        sample = self.sample()
        budget = 2 * 1024**3
        reserve = (sample["memory"]["MemTotal"] + 4) // 5
        sample["memory"]["MemAvailable"] = reserve + budget + client.MARGIN
        client.healthy(sample, budget)
        sample["memory"]["MemAvailable"] -= 1
        with self.assertRaisesRegex(RuntimeError, "reserve"):
            client.healthy(sample, budget)

    def test_global_and_unit_pressure_refuse_work(self):
        for key in ("memory_psi", "unit_memory_psi"):
            with self.subTest(key=key):
                sample = self.sample()
                sample[key] = "some avg10=1.00\nfull avg10=0.00\n"
                with self.assertRaisesRegex(RuntimeError, "pressure"):
                    client.healthy(sample, 536870912)

    def test_unsafe_entry_starts_no_command(self):
        with (
            patch.object(client, "snapshot", return_value=self.sample()),
            patch.object(client, "healthy", side_effect=RuntimeError("reserve")),
            patch.object(client.subprocess, "Popen") as launch,
        ):
            with self.assertRaisesRegex(RuntimeError, "reserve"):
                client.run_fixed(
                    ["must-not-run"],
                    Path("unused"),
                    Path("unused"),
                    536870912,
                    "native",
                )
            launch.assert_not_called()

    def test_native_phase_refuses_shared_workstation_before_any_child(self):
        args = argparse.Namespace(
            phase="native", uid=os.getuid(), gid=os.getgid(), unit="unused", cpu=0
        )
        with (
            patch.dict(os.environ, {"RUNNER_ENVIRONMENT": "self-hosted"}),
            patch.object(client.subprocess, "Popen") as launch,
        ):
            with self.assertRaisesRegex(ValueError, "declared hosted"):
                client.own_scope(args)
            launch.assert_not_called()

    def test_failure_after_launch_stops_only_the_owned_process_group(self):
        sample = self.sample()
        process = unittest.mock.Mock(pid=34567)
        process.poll.return_value = None
        with (
            tempfile.TemporaryDirectory() as temporary,
            patch.object(client, "snapshot", return_value=sample),
            patch.object(
                client, "healthy", side_effect=[None, RuntimeError("pressure")]
            ),
            patch.object(client.subprocess, "Popen", return_value=process),
            patch.object(client.os, "killpg") as stop,
        ):
            with self.assertRaisesRegex(RuntimeError, "pressure"):
                client.run_fixed(
                    ["fixed-owned-child"],
                    Path(temporary),
                    Path("unused"),
                    536870912,
                    "native",
                )
            self.assertEqual(
                stop.call_args_list, [unittest.mock.call(34567, client.signal.SIGTERM)]
            )
            process.wait.assert_called_once_with(timeout=3)

    def test_intense_swap_stops_the_owned_child(self):
        first = self.sample()
        second = copy.deepcopy(first)
        second["swap_pages"]["pswpout"] = 65537
        process = unittest.mock.Mock(pid=34568)
        process.wait.side_effect = [client.subprocess.TimeoutExpired("owned", 5), None]
        process.poll.return_value = None
        with (
            tempfile.TemporaryDirectory() as temporary,
            patch.object(client, "snapshot", side_effect=[first, first, second]),
            patch.object(client.subprocess, "Popen", return_value=process),
            patch.object(client.os, "killpg") as stop,
        ):
            with self.assertRaisesRegex(RuntimeError, "intense swap"):
                client.run_fixed(
                    ["fixed-owned-child"],
                    Path(temporary),
                    Path("unused"),
                    536870912,
                    "native",
                )
            stop.assert_called_once_with(34568, client.signal.SIGTERM)

    def test_cli_cannot_select_private_snapshot_or_other_command(self):
        with (
            self.assertRaises(SystemExit),
            patch.object(client, "fixed_inputs") as check,
        ):
            client.main(["benchmark", "--snapshot", "private.h5msm"])
        check.assert_not_called()

    def test_native_interpreter_must_match_the_new_owned_environment(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / "prefix.json").write_text(
                json.dumps({"python": "/not-this-interpreter"})
            )
            args = argparse.Namespace(output=output)
            with (
                self.assertRaisesRegex(ValueError, "newly created interpreter"),
                patch.object(client.runpy, "run_path") as execute,
            ):
                client.native(args, Path("unused"), 536870912)
            execute.assert_not_called()

    def test_wrong_kernel_limits_refuse_before_any_installer_or_native_child(self):
        controls = {
            "memory.max": "536870912",
            "memory.swap.max": "0",
            "memory.oom.group": "1",
            "pids.max": "32",
            "cpu.max": "100000 100000",
            "cpuset.cpus.effective": "3",
        }
        changes = {
            "memory.max": "2147483648",
            "memory.swap.max": "1",
            "memory.oom.group": "0",
            "pids.max": "64",
            "cpu.max": "200000 100000",
            "cpuset.cpus.effective": "2",
        }
        unit = "phmt148-probe-native-17-1.service"
        args = argparse.Namespace(phase="native", uid=17, gid=18, unit=unit, cpu=3)
        for key, value in changes.items():
            observed = {**controls, key: value}

            def content(path, *unused_args, **unused_kwargs):
                if path == Path("/proc/self/cgroup"):
                    return "0::/system.slice/" + unit
                return observed[path.name]

            with (
                self.subTest(key=key),
                patch.dict(
                    os.environ,
                    {
                        "RUNNER_ENVIRONMENT": "github-hosted",
                        "GITHUB_RUN_ID": "17",
                        "GITHUB_RUN_ATTEMPT": "1",
                    },
                ),
                patch.object(client.sys, "version_info", (3, 14)),
                patch.object(client.os, "getuid", return_value=17),
                patch.object(client.os, "getgid", return_value=18),
                patch.object(client.os, "sched_getaffinity", return_value={3}),
                patch.object(Path, "read_text", content),
                patch.object(client.subprocess, "check_output") as child,
            ):
                with self.assertRaisesRegex(ValueError, "actual kernel controls"):
                    client.own_scope(args)
                child.assert_not_called()

    def test_bootstrap_cannot_target_base_or_an_unrelated_environment(self):
        with tempfile.TemporaryDirectory() as temporary:
            args = argparse.Namespace(
                output=Path(temporary),
                name="base",
                manager=Path(temporary) / "micromamba",
            )
            with (
                patch.dict(
                    os.environ,
                    {
                        "RUNNER_TEMP": temporary,
                        "GITHUB_RUN_ID": "17",
                        "GITHUB_RUN_ATTEMPT": "1",
                    },
                ),
                patch.object(client, "run_fixed") as command,
                patch.object(client.subprocess, "check_output") as version,
            ):
                with self.assertRaisesRegex(ValueError, "fixed fresh environment"):
                    client.bootstrap(args, Path("unused"), 2147483648)
                command.assert_not_called()
                version.assert_not_called()

    def test_exited_child_race_does_not_hide_the_original_pressure_failure(self):
        process = unittest.mock.Mock(pid=34569)
        process.poll.return_value = None
        with (
            tempfile.TemporaryDirectory() as temporary,
            patch.object(client, "snapshot", return_value=self.sample()),
            patch.object(
                client, "healthy", side_effect=[None, RuntimeError("pressure")]
            ),
            patch.object(client.subprocess, "Popen", return_value=process),
            patch.object(client.os, "killpg", side_effect=ProcessLookupError),
        ):
            with self.assertRaisesRegex(RuntimeError, "pressure"):
                client.run_fixed(
                    ["fixed-owned-child"],
                    Path(temporary),
                    Path("unused"),
                    536870912,
                    "native",
                )
            process.wait.assert_called_once_with(timeout=3)
