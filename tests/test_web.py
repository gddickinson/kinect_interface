"""Web interface tests: every exported endpoint answers, the static build is complete, and the JS engine tests pass.

Run: python -m pytest -q tests/test_web.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from web.app import STATIC, STATIC_ENDPOINTS, app  # noqa: E402

client = TestClient(app)


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200 and "static/main.js" in r.text


@pytest.mark.parametrize("path", STATIC_ENDPOINTS)
def test_endpoint(path):
    r = client.get("/api" + path)
    assert r.status_code == 200, r.text
    assert r.json() is not None


def test_static_build(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert (tmp_path / "site" / "index.html").read_text().count("APP_STATIC") == 1
    for path in STATIC_ENDPOINTS:
        assert (tmp_path / "site" / "api" / (path.strip("/") + ".json")).exists()


def test_static_assets_referenced_exist():
    html = (STATIC / "index.html").read_text()
    for name in ("style.css", "main.js"):
        assert f"static/{name}" in html and (STATIC / name).exists()


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_js_engine():
    tests = sorted(STATIC.glob("*.test.mjs"))
    for t in tests:
        r = subprocess.run(["node", str(t)], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


# --- showcase-specific -------------------------------------------------------------------------------------------
from web import project  # noqa: E402


def test_how_citations_resolve():
    secs = client.get("/api/how").json()
    assert len(secs) == len(project.HOW)
    for s in secs:
        for c in s["cites"]:
            assert c["line"] > 0 and c["find"] in c["code"]


def test_tree_excludes_vendored_and_web_files():
    paths = [f["path"] for f in client.get("/api/tree").json()["files"]]
    assert paths and not any(p.startswith(("libraries/", "web/", "tests/", "scripts/")) for p in paths)
    f = client.get("/api/tree").json()["files"][0]
    body = client.get("/api/file/" + f["id"]).json()
    assert body["path"] == f["path"] and isinstance(body["text"], str)
    assert client.get("/api/file/nope").status_code == 404


def test_info_counts_are_real():
    info = client.get("/api/info").json()
    tree = client.get("/api/tree").json()
    assert info["files"] == len(tree["files"]) and info["lines"] > 0
    assert info["vendored"] == len(project.VENDORED)


def test_vendored_licences_come_from_the_folder():
    rows = client.get("/api/vendored").json()
    assert len(rows) == len(project.VENDORED)
    for r in rows:
        assert (ROOT / r["path"]).exists()
        if r["licence"]:
            assert r["source"] and (ROOT / r["source"]).is_file()




def test_depth_fixture_is_current():
    """depth_engine.test.mjs checks the JS against this file; it must still be what depth_display.py produces."""
    import json
    sys.path.insert(0, str(ROOT / "scripts"))
    import make_depth_fixture
    saved = json.loads((ROOT / "tests" / "fixtures" / "depth_cases.json").read_text())
    new = make_depth_fixture.make()
    assert new["lut"] == saved["lut"]
    for a, b in zip(new["cases"], saved["cases"]):
        assert a["depth"] == b["depth"]
        diff = sum(x != y for x, y in zip(a["norm"], b["norm"]))
        assert diff <= len(a["norm"]) // 1000      # OpenCV builds may round a rare tie differently


def test_web_app_does_not_import_the_driver():
    assert "kinect_wrapper" not in sys.modules and "freenect" not in sys.modules


def test_synthetic_frames_are_labelled():
    s = client.get("/api/synthetic/with_no_reading").json()
    assert s["synthetic"] is True and s["min"] == 0 and len(s["depth"]) == s["width"] * s["height"]
