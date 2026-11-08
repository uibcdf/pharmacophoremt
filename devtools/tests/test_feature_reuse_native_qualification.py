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

    def test_original_inputs_are_current_without_scientific_imports(self):
        import sys

        before = set(sys.modules)
        result = client.fixed_inputs()
        self.assertEqual(
            set(result), {client.PROBE, client.SOURCE_INPUT, *client.SELECTORS}
        )
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
