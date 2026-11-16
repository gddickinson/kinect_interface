"""kinect_capture.cpp compiled against a stub libfreenect (tests/freenect_stub): the capture object must clean up
correctly when the Kinect cannot be opened. Regression test for freenect_shutdown being called twice."""
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CXX = shutil.which("c++") or shutil.which("g++") or shutil.which("clang++")
pytestmark = pytest.mark.skipif(not CXX, reason="no C++ compiler")


@pytest.fixture(scope="module")
def exe(tmp_path_factory):
    out = tmp_path_factory.mktemp("stub") / "kstub"
    subprocess.run([CXX, "-std=c++11", "-w", "-I", str(ROOT / "tests" / "freenect_stub"),
                    str(ROOT / "tests" / "freenect_stub" / "stub.cpp"), str(ROOT / "kinect_capture.cpp"),
                    "-o", str(out), "-lpthread"], check=True)
    return out


def run(exe, scenario):
    r = subprocess.run([str(exe), scenario], capture_output=True, text=True, timeout=30)
    assert r.returncode == 0 and "done" in r.stdout, r.stdout + r.stderr
    return dict(ln.split() for ln in r.stdout.splitlines() if ln.startswith(("init", "shutdowns")))


@pytest.mark.parametrize("scenario,init,shutdowns", [
    ("ok", "1", "1"), ("no-init", "0", "0"), ("no-device", "0", "1"), ("never-init", None, "0")])
def test_shutdown_called_once(exe, scenario, init, shutdowns):
    got = run(exe, scenario)
    assert got.get("init") == init and got["shutdowns"] == shutdowns
