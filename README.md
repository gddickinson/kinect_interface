# Kinect Xbox 360 Camera Interface

A high-performance Python interface for the Kinect Xbox 360 camera, providing real-time access to RGB and depth data streams through a C++ backend with a Cython-based Python API.

## Overview

This project wraps the libfreenect library in a clean, performant pipeline: C++ handles the low-level Kinect communication and frame buffering via pthreads, Cython bridges the C++ layer to Python, and the resulting Python API returns frames as NumPy arrays ready for use with OpenCV, matplotlib, or any other scientific Python library.

### Features

- Real-time 640x480 RGB and 16-bit depth frame capture
- Thread-safe double buffering with pthread mutex/condition variable synchronization
- Automatic Kinect device discovery and initialization
- Depth data in millimeters (hardware native format)
- Frames returned as NumPy arrays (`uint8` RGB, `uint16` depth)
- Clean resource management with automatic cleanup on deallocation

## Architecture

```
kinect_capture.cpp/.h    C++ backend using libfreenect
        |                - Manages device lifecycle
        |                - Runs freenect event loop in background thread
        |                - Thread-safe frame buffering
        v
kinect_wrapper.pyx       Cython bridge
        |                - Wraps C++ KinectCapture class
        |                - Handles memory layout for NumPy conversion
        v
Python API               PyKinectCapture class
                         - init() -> bool
                         - get_frames() -> (rgb_array, depth_array)
```

## Files

| File | Description |
|------|-------------|
| `kinect_capture.cpp` | C++ implementation: freenect init, depth/RGB callbacks, threaded event loop |
| `kinect_capture.h` | C API header exposing create/init/get_frames/destroy functions |
| `kinect_wrapper.pyx` | Cython wrapper defining `PyKinectCapture` class |
| `setup.py` | Build configuration linking against libfreenect and libusb |
| `test_kinect.py` | Example script: captures and displays RGB + JET-colorized depth |
| `quickTest.py` | Minimal test script |

## Prerequisites

- Kinect Xbox 360 camera
- macOS (tested on Apple Silicon with Homebrew)
- libfreenect 0.7.5+
- libusb 1.0
- Python 3.8+
- NumPy
- Cython
- OpenCV (for visualization)

## Installation

1. Install libfreenect and libusb via Homebrew:
   ```bash
   brew install libfreenect libusb
   ```

2. Install Python dependencies:
   ```bash
   pip install numpy cython opencv-python
   ```

3. Build the Cython extension:
   ```bash
   python setup.py build_ext --inplace
   ```
   This compiles `kinect_capture.cpp` and `kinect_wrapper.pyx` into `kinect_wrapper.cpython-*.so`.

   **Note**: The `setup.py` currently hardcodes Homebrew paths for Apple Silicon (`/opt/homebrew/Cellar/...`). If your libfreenect is installed elsewhere, update the `include_dirs` and `library_dirs` in `setup.py`.

## Usage

### Basic Frame Capture

```python
from kinect_wrapper import PyKinectCapture
import cv2
import numpy as np

kinect = PyKinectCapture()
if not kinect.init():
    print("Failed to initialize Kinect")
    exit()

while True:
    rgb, depth = kinect.get_frames()
    if rgb is not None and depth is not None:
        cv2.imshow("RGB", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))

        # Colorize depth for visualization
        depth_display = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        depth_colormap = cv2.applyColorMap(depth_display, cv2.COLORMAP_JET)
        cv2.imshow("Depth", depth_colormap)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
```

### Running the Test Script

```bash
python test_kinect.py
```

Displays two windows (RGB and Depth) and prints frame shape/dtype/min/max info to the console. Press `q` to exit.

## Frame Data Format

| Stream | Shape | dtype | Units |
|--------|-------|-------|-------|
| RGB | (480, 640, 3) | uint8 | 0-255 per channel |
| Depth | (480, 640) | uint16 | millimeters from sensor |

## Related Projects

- [depthEstimation](../depthEstimation/) -- Uses this interface for Kinect-enhanced depth estimation with YOLO and 3D skeleton tracking
