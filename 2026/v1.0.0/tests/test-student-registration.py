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
    linked_email = None

    def request(endpoint, route, body, headers):
        global linked_email
        requests.append((route, body))
        assert headers["Authorization"] == "Bearer " + "t" * 64
        if route == "/link-email":
            assert body["student_email"] in {"student@example.test", "updated@example.test"}
            linked_email = body["student_email"]
            return {"ok": True}
        return {"ok": True, "registered": True, "server_id": "srv-0123456789abcdef", "instance_id": "i-test", "email_linked": linked_email is not None}

    with patch.dict(os.environ, JDU_STUDENT_STATE_DIR=temporary, JDU_INSTANCE_ID="i-test"), patch.object(app, "request", request), patch.object(sys, "argv", ["jdu-register"]), patch.object(sys.stdin, "isatty", return_value=True), patch("builtins.input", side_effect=["", "bad", "Student@Example.test", "", "Student@Example.test", "YES"]) as prompt, patch("sys.stdout", new_callable=io.StringIO) as output:
        app.main()
        assert prompt.call_count == 6
        assert "An email address is required" in output.getvalue()
        assert "Not confirmed" in output.getvalue()
        assert "PASS Teacher registration" in output.getvalue()
        assert (state / "student-email.txt").read_text().strip() == "student@example.test"
        assert linked_email == "student@example.test"
        assert [route for route, _ in requests].count("/link-email") == 1
        assert not any("email" in body for route, body in requests if route == "/status")
        prompt.reset_mock()
        app.main()
        prompt.assert_not_called()
        with patch.object(sys, "argv", ["jdu-register", "--change-email"]), patch("builtins.input", side_effect=["Updated@Example.test", "YES"]) as correction:
            app.main()
            assert correction.call_count == 2
        assert linked_email == "updated@example.test"
        assert (state / "student-email.txt").read_text().strip() == "updated@example.test"
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
with patch.object(sys.stdin, "isatty", return_value=False):
    try:
        app.prompt_email()
        raise AssertionError("Noninteractive email registration should fail")
    except ValueError:
        pass
print("PASS visible email prompt rejects blanks, confirms entry, and supports correction")
