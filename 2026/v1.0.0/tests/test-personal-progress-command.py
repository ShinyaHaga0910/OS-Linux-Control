import base64
import contextlib
import importlib.machinery
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import types

app = types.ModuleType("personal_command")
exec(compile(Path(sys.argv[1]).read_text(), sys.argv[1], "exec"), app.__dict__)
with tempfile.TemporaryDirectory() as temporary:
    state = Path(temporary)
    os.environ["JDU_STUDENT_STATE_DIR"] = temporary
    secret = "private-server-token-" + "x" * 48
    (state / "progress.env").write_text("JDU_PROGRESS_ENDPOINT=https://example.test\nJDU_PROGRESS_SERVER_ID=srv-12345678\nJDU_PROGRESS_SERVER_TOKEN=" + secret)
    sys.argv = ["jdu-my-progress"]
    payload = {"url": "https://example.test/student/progress?session=short-lived-token", "expires_in_seconds": 900}
    calls = []
    def fake_open(request, timeout):
        calls.append(request)
        return io.StringIO(json.dumps(payload))
    app.urlopen = fake_open
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        app.main()
    assert output.getvalue() == payload["url"] + "\n"
    assert secret not in output.getvalue()
    assert calls[0].full_url == "https://example.test/student/session"
    assert calls[0].get_header("Authorization") == "Bearer " + secret
    assert json.loads(calls[0].data) == {"server_id": "srv-12345678"}
    class TerminalOutput(io.StringIO):
        def isatty(self):
            return True
    terminal_output = TerminalOutput()
    with contextlib.redirect_stdout(terminal_output):
        app.main()
    assert terminal_output.getvalue() == f"\x1b]8;;{payload['url']}\x1b\\{payload['url']}\x1b]8;;\x1b\\\n"
    for bad_url in ["https://evil.test/student/progress?session=x", "https://example.test/dashboard?session=x", "http://example.test/student/progress?session=x", "https://example.test/student/progress?session=x\x1b\\"]:
        payload["url"] = bad_url
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                app.main()
        except ValueError:
            pass
        else:
            raise AssertionError("Unexpected personal URL accepted")
    # The Ubuntu host stores the same server credentials in base64-encoded fields.
    ubuntu_config = state / "ubuntu-progress.env"
    ubuntu_config.write_text(
        "JDU_PROGRESS_ENDPOINT_B64=" + base64.b64encode(b"https://example.test").decode() + "\n"
        "JDU_PROGRESS_SERVER_ID=srv-12345678\n"
        "JDU_PROGRESS_SERVER_TOKEN_B64=" + base64.b64encode(secret.encode()).decode() + "\n"
    )
    os.environ["JDU_STUDENT_STATE_DIR"] = str(state / "no-cloudshell-state")
    os.environ["JDU_UBUNTU_PROGRESS_CONFIG"] = str(ubuntu_config)
    payload["url"] = "https://example.test/student/progress?session=ubuntu-token"
    calls.clear()
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        app.main()
    assert output.getvalue() == payload["url"] + "\n"
    assert secret not in output.getvalue()
    assert calls[0].get_header("Authorization") == "Bearer " + secret
    assert json.loads(calls[0].data) == {"server_id": "srv-12345678"}
    ubuntu_config.write_text("JDU_PROGRESS_ENDPOINT_B64=invalid!\nJDU_PROGRESS_SERVER_ID=srv-12345678\nJDU_PROGRESS_SERVER_TOKEN_B64=invalid!\n")
    try:
        app.load_config()
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid Ubuntu progress credentials accepted")
print("PASS CloudShell and Ubuntu personal helper authorization, private output, and URL validation")
