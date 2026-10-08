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
            assert body["student_email"] in {"student@jdu.uz", "updated@jdu.uz"}
            linked_email = body["student_email"]
            return {"ok": True}
        return {"ok": True, "registered": True, "server_id": "srv-0123456789abcdef", "instance_id": "i-test", "email_linked": linked_email is not None}

    with patch.dict(os.environ, JDU_STUDENT_STATE_DIR=temporary, JDU_INSTANCE_ID="i-test"), patch.object(app, "request", request), patch.object(sys, "argv", ["jdu-register"]), patch.object(sys.stdin, "isatty", return_value=True), patch("builtins.input", side_effect=["", "bad", "student@example.test", "student@jdu.uz.evil", "Student@JDU.UZ", "", "Student@JDU.UZ", "Yes"]) as prompt, patch("sys.stdout", new_callable=io.StringIO) as output:
        app.main()
        assert prompt.call_count == 8
        assert "Email is required." in output.getvalue()
        assert "Use your @jdu.uz email." in output.getvalue()
        assert "Not confirmed" in output.getvalue()
        assert "PASS Teacher registration" in output.getvalue()
        assert "Enter your Google Classroom email" not in output.getvalue()
        assert prompt.call_args_list[0].args == ("Enter your university email (visible): ",)
        assert prompt.call_args_list[-1].args == ("Confirm student@jdu.uz? Type Yes: ",)
        assert (state / "student-email.txt").read_text().strip() == "student@jdu.uz"
        assert linked_email == "student@jdu.uz"
        assert [route for route, _ in requests].count("/link-email") == 1
        assert not any("email" in body for route, body in requests if route == "/status")
        prompt.reset_mock()
        app.main()
        prompt.assert_not_called()
        with patch.object(sys, "argv", ["jdu-register", "--change-email"]), patch("builtins.input", side_effect=["Updated@JDU.UZ", "Yes"]) as correction:
            app.main()
            assert correction.call_count == 2
        assert linked_email == "updated@jdu.uz"
        assert (state / "student-email.txt").read_text().strip() == "updated@jdu.uz"
        (state / "student-email.txt").write_text("legacy@example.test\n")
        with patch("builtins.input", side_effect=["Updated@JDU.UZ", "Yes"]) as replace_legacy:
            app.main()
            assert replace_legacy.call_count == 2
        assert (state / "student-email.txt").read_text().strip() == "updated@jdu.uz"
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
