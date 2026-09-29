import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("student_registration", sys.argv[1])
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

with tempfile.TemporaryDirectory() as temporary:
    state = Path(temporary)
    (state / "progress.env").write_text("JDU_PROGRESS_ENDPOINT=https://example.test\nJDU_PROGRESS_SERVER_ID=srv-0123456789abcdef\nJDU_PROGRESS_SERVER_TOKEN=" + "t" * 64 + "\n")
    requests = []
    linked = False

    def request(endpoint, route, body, headers):
        global linked
        requests.append((route, body))
        assert headers["Authorization"] == "Bearer " + "t" * 64
        if route == "/link-email":
            assert body["student_email"] == "student@example.test"
            linked = True
            return {"ok": True}
        return {"ok": True, "registered": True, "server_id": "srv-0123456789abcdef", "instance_id": "i-test", "email_linked": linked}

    with patch.dict(os.environ, JDU_STUDENT_STATE_DIR=temporary, JDU_INSTANCE_ID="i-test"), patch.object(app, "request", request), patch.object(sys, "argv", ["jdu-register"]), patch.object(sys.stdin, "isatty", return_value=True), patch.object(app.getpass, "getpass", side_effect=["bad", "Student@Example.test"]) as prompt, patch("sys.stdout", new_callable=io.StringIO) as output:
        app.main()
        assert prompt.call_count == 2
        assert "student@example.test" not in output.getvalue().lower()
        assert "PASS Teacher registration" in output.getvalue()
        assert (state / "student-email.txt").read_text().strip() == "student@example.test"
        assert not any("email" in body for route, body in requests if route == "/status")
        prompt.reset_mock()
        app.main()
        prompt.assert_not_called()
        assert "student@example.test" not in output.getvalue().lower()
        with patch.object(sys, "argv", ["jdu-register", "--change-email"]), patch.object(app.getpass, "getpass", return_value="student@example.test") as correction:
            app.main()
            correction.assert_called_once()
        with patch.dict(os.environ, JDU_INSTANCE_ID="i-other"):
            try:
                app.main()
                raise AssertionError("Mismatched instance should fail")
            except ValueError:
                pass
        with patch.object(app, "request", return_value={"registered": False}):
            try:
                app.main()
                raise AssertionError("Unconfirmed registration should fail")
            except ValueError:
                pass
    if os.name != "nt":
        assert (state / "student-email.txt").stat().st_mode & 0o777 == 0o600
print("PASS student email prompt, reuse, privacy, and teacher registration readback")
