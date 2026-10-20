#!/usr/bin/env python3
"""Exercise recovery against fake AWS, SSH and API boundaries; never contact AWS."""
import argparse
import base64
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError


source = Path(__file__).resolve().parents[1] / "scripts/recover-existing-registration.py"
spec = importlib.util.spec_from_file_location("registration_recovery", source)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
SID = "srv-test-only-1234"
IID = "i-0123456789abcdef0"
TOKEN = "test-only-token-not-a-real-credential-123456"
ENDPOINT = "https://teacher.example.test"
STATUS = {"registered": True, "server_id": SID, "instance_id": IID}


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state = Path(self.tmp.name) / "state"
        self.args = argparse.Namespace(region="us-east-1", stack_name="test-lab",
                                       ssh_host="jdu-ubuntu", progress_endpoint=ENDPOINT)
        self.stack = {"StackStatus": "CREATE_COMPLETE", "Outputs": [
            {"OutputKey": "InstanceId", "OutputValue": IID}], "Parameters": [
            {"ParameterKey": "ProgressServerId", "ParameterValue": SID}]}
        self.remote = {"hostname": "test-host", "version": "test-version", "config":
            f"JDU_PROGRESS_SERVER_ID={SID}\nJDU_PROGRESS_ENDPOINT_B64="
            + base64.b64encode(ENDPOINT.encode()).decode()
            + "\nJDU_PROGRESS_SERVER_TOKEN_B64=" + base64.b64encode(TOKEN.encode()).decode() + "\n"}
        self.ssh_config = f"hostname {IID}\nuser ssm-user\n"
        self.env = patch.dict(os.environ, {"JDU_STUDENT_STATE_DIR": str(self.state)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def fake_aws(self, region, *args):
        self.assertEqual(region, "us-east-1")
        if args[:2] == ("cloudformation", "describe-stacks"):
            return {"Stacks": [self.stack]}
        self.assertEqual(args, ("sts", "get-caller-identity"))
        return {"Account": "000000000000"}

    def fake_run(self, args, source=None):
        self.assertEqual(args[0], "ssh")
        if args[1] == "-G":
            return self.ssh_config
        self.assertEqual(source, app.REMOTE_READ)
        self.assertNotIn("sudo", args)
        return json.dumps(self.remote)

    def seed(self, token=TOKEN, sid=SID, endpoint=ENDPOINT):
        self.state.mkdir()
        body = f"JDU_PROGRESS_ENDPOINT={endpoint}\nJDU_PROGRESS_SERVER_ID={sid}\nJDU_PROGRESS_SERVER_TOKEN={token}\n"
        (self.state / "progress.env").write_text(body)
        (self.state / "student-email.txt").write_text("student@example.test\n")
        return body

    def call(self, effects):
        output = io.StringIO()
        with patch.object(app, "aws", side_effect=self.fake_aws), \
             patch.object(app, "run", side_effect=self.fake_run), \
             patch.object(app, "api", side_effect=effects) as api_mock, \
             patch.object(app.getpass, "getpass", return_value="a" * 64) as prompt, \
             patch.object(app.sys.stdin, "isatty", return_value=True), \
             contextlib.redirect_stdout(output):
            app.recover(self.args)
        self.assertNotIn(TOKEN, output.getvalue())
        return api_mock, prompt, output.getvalue()

    def test_missing_local_config_recovers_without_registration_key(self):
        api, prompt, output = self.call([STATUS])
        self.assertEqual(api.call_count, 1)
        prompt.assert_not_called()
        saved = app.config((self.state / "progress.env").read_text())
        self.assertEqual(saved["JDU_PROGRESS_SERVER_TOKEN"], TOKEN)
        if os.name == "posix":
            self.assertEqual((self.state / "progress.env").stat().st_mode & 0o777, 0o600)
            self.assertEqual(self.state.stat().st_mode & 0o777, 0o700)

    def test_local_token_repaired_only_after_teacher_accepts_ubuntu(self):
        original = self.seed(token="old-local-token")
        self.call([STATUS])
        backups = list(self.state.glob("progress.env.backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), original)
        if os.name == "posix":
            self.assertEqual(backups[0].stat().st_mode & 0o777, 0o600)
        self.assertEqual((self.state / "student-email.txt").read_text(), "student@example.test\n")

    def test_same_config_is_idempotent(self):
        original = self.seed()
        self.call([STATUS])
        self.assertEqual(list(self.state.glob("progress.env.backup-*")), [])
        self.assertEqual((self.state / "progress.env").read_text(), original)

    def test_missing_teacher_registration_reuses_existing_identity(self):
        api, prompt, output = self.call([
            HTTPError(ENDPOINT, 401, "unauthorized", {}, None),
            {"ok": True, "server_id": SID}, STATUS])
        self.assertEqual(prompt.call_count, 1)
        body = api.call_args_list[1].args[2]
        self.assertEqual(body["server_id"], SID)
        self.assertEqual(body["server_token"], TOKEN)
        self.assertEqual(body["instance_id"], IID)
        self.assertNotIn("a" * 64, output)

    def test_teacher_token_conflict_does_not_overwrite_local_config(self):
        original = self.seed()
        with self.assertRaisesRegex(app.RecoveryError, "another token"):
            self.call([HTTPError(ENDPOINT, 401, "", {}, None), HTTPError(ENDPOINT, 409, "", {}, None)])
        self.assertEqual((self.state / "progress.env").read_text(), original)
        self.assertEqual(list(self.state.glob("progress.env.backup-*")), [])

    def test_forbidden_or_missing_route_does_not_register(self):
        for code in (403, 404, 500, 302):
            with self.subTest(code=code), self.assertRaises(HTTPError):
                self.call([HTTPError(ENDPOINT, code, "", {}, None)])
            self.assertFalse(self.state.exists())

    def test_network_failure_preserves_config(self):
        original = self.seed()
        with self.assertRaises(URLError):
            self.call([URLError("unavailable")])
        self.assertEqual((self.state / "progress.env").read_text(), original)

    def test_wrong_ssh_target_stops_before_api(self):
        self.ssh_config = "hostname i-aaaaaaaaaaaaaaaaa\nuser ssm-user\n"
        with self.assertRaisesRegex(app.RecoveryError, "SSH"):
            self.call([])
        self.assertFalse(self.state.exists())

    def test_different_local_server_id_is_not_replaced(self):
        original = self.seed(sid="srv-another-student")
        with self.assertRaisesRegex(app.RecoveryError, "another Server ID"):
            self.call([])
        self.assertEqual((self.state / "progress.env").read_text(), original)

    def test_wrong_teacher_ec2_does_not_write(self):
        with self.assertRaisesRegex(app.RecoveryError, "does not match"):
            self.call([{**STATUS, "instance_id": "i-aaaaaaaaaaaaaaaaa"}])
        self.assertFalse(self.state.exists())

    def test_stack_identity_mismatch_does_not_write(self):
        self.stack["Parameters"][0]["ParameterValue"] = "srv-another-student"
        with self.assertRaisesRegex(app.RecoveryError, "differs from the stack"):
            self.call([])
        self.assertFalse(self.state.exists())

    def test_changed_endpoint_is_not_followed(self):
        self.args.progress_endpoint = "https://other.example.test"
        with self.assertRaisesRegex(app.RecoveryError, "another endpoint"):
            self.call([])
        self.assertFalse(self.state.exists())

    def test_session_url_is_rejected_before_ssh(self):
        self.args.progress_endpoint += "/dashboard?session=test"
        with self.assertRaisesRegex(app.RecoveryError, "without a session"):
            self.call([])

    def test_unready_stack_is_not_changed(self):
        self.stack["StackStatus"] = "ROLLBACK_COMPLETE"
        with self.assertRaisesRegex(app.RecoveryError, "not ready"):
            self.call([])
        self.assertFalse(self.state.exists())

    def test_main_does_not_expose_api_error_details(self):
        error = HTTPError(ENDPOINT + "/?secret=test", 403, TOKEN, {}, None)
        output = io.StringIO()
        with patch.object(app.sys, "argv", [str(source), "--region", "us-east-1", "--progress-endpoint", ENDPOINT]), \
             patch.object(app, "recover", side_effect=error), contextlib.redirect_stderr(output):
            self.assertEqual(app.main(), 1)
        self.assertIn("403", output.getvalue())
        self.assertNotIn(TOKEN, output.getvalue())
        self.assertNotIn("secret=test", output.getvalue())


if __name__ == "__main__":
    unittest.main()
