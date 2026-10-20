"""Exercise the CLI as an adopting repository would, including failed gates."""

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


REPO = Path(__file__).resolve().parents[1]
RUNNER = REPO / "skills/blueprint/scripts/harness.py"


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runner = RUNNER

    def invoke(self, command, *args, expected=0):
        result = subprocess.run(
            [sys.executable, str(self.runner), command, "--root", str(self.root), "--json", *args],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def initialize(self):
        self.invoke("init")
        # All subsequent operations use only the copied, standalone runner.
        self.runner = self.root / ".blueprint/harness.py"

    def configure(self, checks=None, **overrides):
        path = self.root / ".blueprint/config.json"
        config = json.loads(path.read_text())
        config["checks"] = checks if checks is not None else [self.check("smoke", "print('ok')")]
        config.update(overrides)
        path.write_text(json.dumps(config))

    @staticmethod
    def check(name, source, timeout=5):
        return {
            "name": name, "argv": [sys.executable, "-c", source],
            "cwd": ".", "timeout_seconds": timeout,
        }

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_init_dry_run_and_existing_files_are_preserved(self):
        agents = self.root / "AGENTS.md"
        agents.write_text("# Existing instructions\n")
        before = self.snapshot()
        planned = self.invoke("init", "--dry-run")
        self.assertEqual(self.snapshot(), before)
        self.assertIn("AGENTS.md", planned["preserved"])
        self.invoke("init")
        self.assertEqual(agents.read_text(), "# Existing instructions\n")
        config = self.root / ".blueprint/config.json"
        config.write_text('{"custom": "preserve me"}\n')
        before = self.snapshot()
        repeated = self.invoke("init")
        self.assertEqual(repeated["created"], [])
        self.assertEqual(self.snapshot(), before)

    def test_empty_checks_fail_without_false_readiness_or_execution(self):
        self.initialize()
        before = self.snapshot()
        self.invoke("doctor", expected=1)
        self.invoke("check", expected=1)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / ".blueprint/runs").exists())

    def test_doctor_is_read_only_and_does_not_run_commands(self):
        self.initialize()
        self.configure([self.check("marker", "open('executed', 'w').write('yes')")])
        before = self.snapshot()
        self.invoke("doctor")
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / "executed").exists())

    def test_failed_checks_collect_evidence_and_do_not_skip_remaining_checks(self):
        self.initialize()
        self.configure([
            self.check("failure", "print('diagnostic'); raise SystemExit(7)"),
            self.check("success", "print('still ran')"),
        ])
        result = self.invoke("check", expected=1)
        self.assertEqual([c["status"] for c in result["checks"]], ["fail", "pass"])
        self.assertEqual(result["checks"][0]["exit_code"], 7)
        self.assertIn("diagnostic", (self.root / result["checks"][0]["log"]).read_text())
        self.assertEqual(json.loads((self.root / result["report"]).read_text()), result)

    def test_success_runs_have_distinct_evidence(self):
        self.initialize()
        self.configure()
        first, second = self.invoke("check"), self.invoke("check")
        self.assertNotEqual(first["run_id"], second["run_id"])
        self.assertTrue((self.root / first["report"]).is_file())
        self.assertTrue((self.root / second["report"]).is_file())

    def test_missing_executable_is_a_failed_check(self):
        self.initialize()
        check = self.check("missing", "")
        check["argv"] = ["blueprint-test-executable-that-does-not-exist"]
        self.configure([check])
        result = self.invoke("check", expected=1)
        self.assertEqual(result["checks"][0]["status"], "error")
        self.assertIsNone(result["checks"][0]["exit_code"])

    def test_timeout_is_not_a_pass(self):
        self.initialize()
        self.configure([self.check("slow", "import time; time.sleep(10)", timeout=1)])
        result = self.invoke("check", expected=1)
        self.assertEqual(result["checks"][0]["status"], "timeout")
        self.assertLess(result["checks"][0]["duration_seconds"], 5)

    @unittest.skipUnless(os.name == "posix", "POSIX process-group contract")
    def test_timeout_also_stops_child_process(self):
        self.initialize()
        child = "import time; time.sleep(2); open('child-survived', 'w').write('bad')"
        source = f"import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(10)"
        self.configure([self.check("parent", source, timeout=1)])
        self.invoke("check", expected=1)
        time.sleep(1.2)
        self.assertFalse((self.root / "child-survived").exists())

    @unittest.skipUnless(os.name == "posix", "POSIX signal delivery")
    def test_interrupt_records_evidence_and_skips_remaining_checks(self):
        self.initialize()
        self.configure([
            self.check("slow", "import time; open('started', 'w').close(); time.sleep(10)"),
            self.check("later", "open('should-not-run', 'w').close()"),
        ])
        process = subprocess.Popen(
            [sys.executable, str(self.runner), "check", "--root", str(self.root), "--json"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        try:
            deadline = time.monotonic() + 5
            while not (self.root / "started").exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue((self.root / "started").exists())
            process.send_signal(signal.SIGINT)
            stdout, stderr = process.communicate(timeout=5)
            self.assertEqual(process.returncode, 130, stdout + stderr)
            result = json.loads(stdout)
            self.assertEqual([c["status"] for c in result["checks"]], ["interrupted", "not_run"])
            self.assertTrue((self.root / result["report"]).is_file())
            self.assertFalse((self.root / "should-not-run").exists())
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate()

    def test_argv_is_not_interpreted_as_shell(self):
        self.initialize()
        check = self.check("literal", "import sys; print(sys.argv[1])")
        check["argv"].append("$(touch injected); echo bad")
        self.configure([check])
        result = self.invoke("check")
        log = (self.root / result["checks"][0]["log"]).read_text()
        self.assertEqual(log.strip(), "$(touch injected); echo bad")
        self.assertFalse((self.root / "injected").exists())

    def test_missing_documents_and_broken_links_block_execution(self):
        self.initialize()
        self.configure([self.check("marker", "open('executed', 'w').close()")])
        (self.root / "docs/blueprint/quality.md").unlink()
        (self.root / "AGENTS.md").write_text("[missing](absent.md)\n")
        result = self.invoke("check", expected=1)
        self.assertTrue(any("absent.md" in error for error in result["errors"]))
        self.assertFalse((self.root / "executed").exists())

    def test_invalid_config_is_rejected_before_any_command(self):
        self.initialize()
        valid = self.check("marker", "open('executed', 'w').close()")
        for field, value in [
            ("name", "../bad"), ("argv", "echo bad"), ("cwd", ".."),
            ("timeout_seconds", True), ("timeout_seconds", 0),
        ]:
            with self.subTest(field=field, value=value):
                self.configure([valid, {**self.check("invalid", ""), field: value}])
                self.invoke("check", expected=2)
                self.assertFalse((self.root / "executed").exists())
        self.configure([valid, valid])
        self.invoke("doctor", expected=2)
        self.configure(schema_version=True)
        self.invoke("doctor", expected=2)

    def test_malformed_json_has_actionable_error(self):
        self.initialize()
        (self.root / ".blueprint/config.json").write_text("{")
        result = self.invoke("doctor", expected=2)
        self.assertIn("Cannot read .blueprint/config.json", result["errors"][0])

    @unittest.skipUnless(os.name == "posix", "symlink support")
    def test_init_preserves_dangling_local_symlink(self):
        (self.root / "AGENTS.md").symlink_to("instructions-not-created.md")
        result = self.invoke("init")
        self.assertIn("AGENTS.md", result["preserved"])
        self.assertTrue((self.root / "AGENTS.md").is_symlink())
        self.assertFalse((self.root / "instructions-not-created.md").exists())

    @unittest.skipUnless(os.name == "posix", "symlink support")
    def test_init_rejects_symlink_escape_before_writing(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / ".blueprint").symlink_to(outside, target_is_directory=True)
            self.invoke("init", expected=2)
            self.assertEqual(list(Path(outside).iterdir()), [])
            self.assertFalse((self.root / "AGENTS.md").exists())

    def test_document_links_must_stay_in_repository(self):
        self.initialize()
        self.configure()
        (self.root / "AGENTS.md").write_text("[escape](../outside.md)\n")
        result = self.invoke("doctor", expected=1)
        self.assertTrue(any("escapes the repository" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
