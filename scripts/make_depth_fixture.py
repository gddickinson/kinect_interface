"""Write tests/fixtures/depth_cases.json: the SYNTHETIC frames (web/synthetic.py) and what depth_display.py makes of
them (normalised values and JET colours), for web/static/depth_engine.test.mjs.

Run: python scripts/make_depth_fixture.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import depth_display  # noqa: E402
from web.synthetic import SCENES  # noqa: E402

OUT = ROOT / "tests" / "fixtures" / "depth_cases.json"


def make():
    cases = []
    for name, fn in SCENES.items():
        d = fn()[::2, ::2]          # half size keeps the fixture small; same code path
        bgr = depth_display.colorize_depth(d)
        cases.append({"name": name, "shape": list(d.shape), "depth": d.ravel().tolist(),
                      "norm": depth_display.normalize_depth(d).ravel().tolist(),
                      "rgb": bgr[..., ::-1].reshape(-1, 3).tolist()})
    return {"lut": depth_display.jet_lut(), "cases": cases}


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(make(), separators=(",", ":")) + "\n")
    print("wrote", OUT.relative_to(ROOT), round(OUT.stat().st_size / 1e3), "KB")
