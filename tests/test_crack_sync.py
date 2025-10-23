# tests/test_crack_sync.py (import safe)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app
import json

def test_crack_password_found(tmp_path):
    tmp = tmp_path / "tmpdico.txt"
    tmp.write_text("123456\npassword\n")
    client = app.test_client()
    payload = {
        "hash": "e10adc3949ba59abbe56e057f20f883e",
        "algo": "md5",
        "mode": "sync",
        "wordlist": str(tmp)
    }
    resp = client.post("/api/v1/crack", json=payload)
    assert resp.status_code == 200
    j = resp.get_json()
    assert j["found"] is True
    assert j["plaintext"] == "123456"
