import os, sys
import pytest
import smtplib
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to the project root, then into config/.env
env_path = os.path.join(current_dir, "..", "config", ".env")
if not os.path.exists(env_path):
    raise FileNotFoundError(f"Environment file {env_path} not found.")
else:
    print(f"Loading environment variables from {env_path}")
load_dotenv(dotenv_path=env_path)


from src.send_email import build_html_report, send_report


class DummySMTP:
    def __init__(self, *args, **kwargs):
        # capture parameters if needed
        pass
    def set_debuglevel(self, level):
        pass
    def connect(self, host, port, source_address=None):
        return (220, b"OK")
    def ehlo(self):
        return (250, b"OK")
    def starttls(self):
        return (220, b"OK")
    def login(self, user, passwd):
        return (235, b"Logged in")
    def sendmail(self, from_addr, to_addrs, msg):
        # simulate successful send
        return {}
    def quit(self):
        pass

@pytest.fixture(autouse=True)
def patch_smtp(monkeypatch):
    # replace smtplib.SMTP with our dummy class
    monkeypatch.setattr(smtplib, 'SMTP', DummySMTP)
    yield


def test_build_html_report_contains_items():
    items = [{"title": "Foo", "url": "http://a", "summary": "Bar"}]
    html = build_html_report(items)
    assert "http://a'" in html
    assert "Bar" in html


def test_send_report_runs_without_error(tmp_path, monkeypatch):
    # configure env vars for SMTP
    monkeypatch.setenv('EMAIL_SMTP_HOST', 'localhost')
    monkeypatch.setenv('EMAIL_SMTP_PORT', '587')
    monkeypatch.setenv('EMAIL_SMTP_USER', 'user')
    monkeypatch.setenv('EMAIL_SMTP_PASS', 'pass')
    monkeypatch.setenv('TO_EMAIL', 'to@example.com')

    items = [{"title": "Foo", "url": "http://a", "summary": "Bar"}]
    # Should not raise any exceptions
    send_report(items)
