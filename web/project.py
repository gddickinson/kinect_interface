"""Project-specific content for the kinect_interface showcase: excludes, tiles, the "How it works" sections (claims
cited to a file + a text that must occur on the cited line; resolved and checked by the tests), About, and the demo
endpoints (OpenCV's JET table via depth_display.py, and SYNTHETIC depth frames). Nothing here imports the Kinect
driver (kinect_wrapper / libfreenect).
"""
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import depth_display  # noqa: E402  (the module test_kinect.py uses)

from .synthetic import SCENES, H, W  # noqa: E402

TITLE = "Kinect Xbox 360 Interface"
REPO = "kinect_interface"
PORT = 8261
KICKER = "C++ · Cython · libfreenect · NumPy"
DESCRIPTION = ("Access to the RGB and depth streams of a Kinect Xbox 360 from Python: a C++ libfreenect backend with a "
               "capture thread, a Cython bridge, and frames returned as NumPy arrays.")
DEMO = {"title": "Depth colouring demo",
        "blurb": "The depth display of test_kinect.py (min-max to 8 bits, then OpenCV's JET map), ported to JS and "
                 "matched pixel for pixel, on SYNTHETIC depth frames: no Kinect needed."}

EXCLUDE = ("web/*", "scripts/*", "tests/*", "run_web.py", "requirements-web.txt", ".github/*", "docs/*",
           "SESSION_LOG.md", "INTERFACE.md", ".gitignore", ".gitattributes")
VENDORED = ()
NOT_CODE = ("Markdown", "Text")


def tiles(shown):
    return [[640 * 480, "pixels per frame"], [2, "streams (RGB, depth)"],
            [sum(f["lang"] in ("C++", "Python") for f in shown), "source files"]]


CPP = "kinect_capture.cpp"
SVG = """<svg viewBox="0 0 780 170" role="img" aria-label="Data flow: the Kinect over USB to libfreenect; a capture thread
runs freenect_process_events and the depth and RGB callbacks copy frames into buffers under a mutex; get_frames waits
on a condition variable and copies both buffers into NumPy arrays through the Cython wrapper">
<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
<path class="arh" d="M0 0L10 5L0 10z"/></marker></defs>
<rect class="bx3" x="5" y="55" width="105" height="60" rx="6"/><text class="t" x="57" y="82" text-anchor="middle">Kinect</text><text class="tm" x="57" y="100" text-anchor="middle">USB</text>
<path class="ar" d="M110 85H135"/>
<rect class="bx" x="138" y="20" width="250" height="130" rx="6"/><text class="t" x="263" y="44" text-anchor="middle">kinect_capture.cpp</text>
<text class="tm" x="263" y="68" text-anchor="middle">thread: freenect_process_events</text>
<text class="tm" x="263" y="88" text-anchor="middle">depth_cb / rgb_cb: memcpy</text><text class="tm" x="263" y="106" text-anchor="middle">under mutex, signal cond</text>
<text class="tm" x="263" y="126" text-anchor="middle">getFrames: wait, copy both</text>
<path class="ar" d="M388 85H413"/>
<rect class="bx2" x="416" y="45" width="160" height="80" rx="6"/><text class="t" x="496" y="72" text-anchor="middle">kinect_wrapper</text>
<text class="tm" x="496" y="92" text-anchor="middle">Cython: PyKinectCapture</text><text class="tm" x="496" y="110" text-anchor="middle">init(), get_frames()</text>
<path class="ar" d="M576 85H601"/>
<rect class="bx3" x="604" y="35" width="170" height="100" rx="6"/><text class="t" x="689" y="60" text-anchor="middle">NumPy</text>
<text class="tm" x="689" y="84" text-anchor="middle">rgb (480,640,3) uint8</text><text class="tm" x="689" y="104" text-anchor="middle">depth (480,640) uint16 mm</text>
</svg>"""

HOW = [
    {"id": "layers", "title": "Three layers: C++, Cython, NumPy", "svg": SVG,
     "caption": "From the USB device to two NumPy arrays.",
     "body": """<p><code>kinect_capture.cpp</code> owns the libfreenect context and device. <code>init()</code> opens
device 0 (motor and camera sub-devices), registers a depth and a video callback, selects medium resolution with depth
in millimetres and RGB video, starts both streams and launches a thread that loops on
<code>freenect_process_events</code>. Each callback copies the new frame into its buffer (640×480×2 bytes for depth,
640×480×3 for RGB) while holding a mutex and signals a condition variable. A small <code>extern "C"</code> API wraps the
class, and the Cython class <code>PyKinectCapture</code> calls it, allocating the NumPy arrays that
<code>get_frames()</code> fills.</p>""",
     "cites": [
         {"file": CPP, "find": "freenect_select_subdevices(f_ctx"},
         {"file": CPP, "find": "freenect_find_depth_mode(FREENECT_RESOLUTION_MEDIUM, FREENECT_DEPTH_MM)"},
         {"file": CPP, "find": "while (!kinect->die && freenect_process_events(kinect->f_ctx) >= 0) {}"},
         {"file": CPP, "find": "memcpy(kinect->depth_buffer.data(), v_depth, kinect->depth_buffer.size());"},
         {"file": CPP, "find": "depth_buffer.resize(640 * 480 * 2);"},
         {"file": "kinect_capture.h", "find": 'extern "C" {'},
         {"file": "kinect_wrapper.pyx", "find": "cdef np.ndarray[np.uint16_t, ndim=2] depth = np.empty((480, 640), dtype=np.uint16)"},
     ]},
    {"id": "handoff", "title": "Getting a frame pair",
     "body": """<p><code>getFrames()</code> locks the mutex, waits on the condition variable until the <b>next</b> callback
of either stream arrives, then copies both buffers out. A call therefore blocks until something new arrives and returns
the latest depth and the latest RGB frame, which can come from slightly different moments (the two streams are not
synchronised). The Python method returns <code>(None, None)</code> only if the C++ call reports failure, which the
current code never does.</p>""",
     "cites": [
         {"file": CPP, "find": "pthread_cond_wait(&frame_cond, &buffer_mutex);"},
         {"file": CPP, "find": "memcpy(rgb, rgb_buffer.data(), rgb_buffer.size());"},
         {"file": CPP, "find": "bool getFrames(uint8_t *rgb, uint16_t *depth) {"},
         {"file": "kinect_wrapper.pyx", "find": "return None, None"},
     ]},
    {"id": "display", "title": "Showing depth: min-max and JET",
     "body": """<p><code>test_kinect.py</code> shows the RGB frame and a colourised depth frame side by side. The depth
colouring, now in <code>depth_display.py</code>, stretches each frame's own minimum..maximum to 0..255 and applies
OpenCV's JET map (blue near, red far). Because the stretch is per frame, the colours are relative: the same distance
can change colour from frame to frame. Pixels with no measurement are 0 mm, so whenever any are present they become the
minimum and the rest of the scene is squeezed towards the red end; the demo shows this with a synthetic frame.</p>""",
     "cites": [
         {"file": "depth_display.py", "find": "cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)"},
         {"file": "depth_display.py", "find": "cv2.applyColorMap(normalize_depth(depth), cv2.COLORMAP_JET)"},
         {"file": "test_kinect.py", "find": "depth_colormap = colorize_depth(depth)"},
         {"file": "test_kinect.py", "find": 'cv2.imshow("Depth", depth_colormap)'},
     ]},
    {"id": "build", "title": "Building, and a cleanup fix",
     "body": """<p><code>setup.py</code> finds libfreenect and libusb through <code>pkg-config</code>, then the Homebrew
prefix on macOS, then common Linux paths, and compiles <code>kinect_wrapper.pyx</code> with
<code>kinect_capture.cpp</code> as C++11 against libc++ (the <code>-stdlib=libc++</code> flag is a clang option, so a
GCC build on Linux would need it removed). <code>kinect_wrapper.cpp</code> is the file Cython generates.</p>
<p>Fixed in this branch: when the device could not be opened, <code>init()</code> shut libfreenect down but the
destructor did it again on the freed context, and the destructor joined a capture thread that had never been started.
Both are now guarded; a stub libfreenect in <code>tests/</code> lets the lifecycle be tested without a Kinect.</p>""",
     "cites": [
         {"file": "setup.py", "find": '["pkg-config", "--cflags", lib]'},
         {"file": "setup.py", "find": 'extra_compile_args=["-std=c++11", "-stdlib=libc++"]'},
         {"file": CPP, "find": "f_ctx = nullptr;  // already shut down"},
         {"file": CPP, "find": "if (thread_started) {"},
     ]},
]

ABOUT = {
    "port": PORT,
    "what": """<p>A small, fast Python interface to the original Kinect for Xbox 360: C++ handles libfreenect and frame
buffering in a background thread, Cython bridges it to Python, and frames come back as NumPy arrays ready for OpenCV
or matplotlib. It is used by George's <a href="https://github.com/gddickinson/depthEstimation">depthEstimation</a>
project.</p><p class="small">The repo contains no recorded frames, so the demo uses synthetic depth frames generated
for it and labelled as such.</p>""",
    "needs": ["A Kinect for Xbox 360 with its USB/power adapter.",
              "libfreenect 0.7.5+ and libusb 1.0 (e.g. <code>brew install libfreenect libusb</code>).",
              "Python 3.8+, NumPy, Cython, OpenCV (for the viewer)."],
    "run": ["<code>python setup.py build_ext --inplace</code> builds <code>kinect_wrapper</code>.",
            "<code>python test_kinect.py</code> opens RGB and Depth windows; press q to quit."],
    "credits": ["George Dickinson.", "Built on libfreenect."],
    "licence": "MIT (see LICENSE).",
}

EXTRA_ENDPOINTS = ["/jet_lut", "/synthetic"] + [f"/synthetic/{n}" for n in SCENES]


def register(app: FastAPI):
    @app.get("/api/jet_lut")
    def jet_lut():
        """OpenCV's JET table, from depth_display.jet_lut()."""
        return depth_display.jet_lut()

    @app.get("/api/synthetic")
    def synthetic_list():
        return [{"name": n, "doc": " ".join(fn.__doc__.split())} for n, fn in SCENES.items()]

    @app.get("/api/synthetic/{name}")
    def synthetic(name: str):
        """One SYNTHETIC depth frame (uint16 mm, row-major) and its colouring by depth_display.py."""
        if name not in SCENES:
            raise HTTPException(404, "no such scene")
        d = SCENES[name]()
        return {"name": name, "synthetic": True, "width": W, "height": H, "depth": d.ravel().tolist(),
                "min": int(d.min()), "max": int(d.max())}
