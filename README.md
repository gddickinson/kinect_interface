# Kinect Xbox 360 Camera Interface

## Introduction

This project provides a high-performance interface for the Kinect Xbox 360 camera, allowing easy access to both RGB and depth data streams in Python. The Kinect Xbox 360 is a motion sensing input device originally developed for Xbox 360 gaming consoles. It features an RGB camera, an infrared projector and camera for depth sensing, and a multi-array microphone.

## Project Overview

This implementation uses libfreenect for low-level communication with the Kinect device, with a C++ backend for performance and a Cython wrapper for Python accessibility. The project aims to provide a simple, efficient way to capture and process Kinect data for various applications such as computer vision, robotics, and interactive installations.

### Features

- Real-time access to RGB and depth data streams
- High-performance C++ backend
- Python-friendly interface via Cython
- Easy-to-use Python API for capturing frames
- Example script for visualizing RGB and depth data

## Technical Implementation

The project is structured as follows:

1. C++ Backend (`kinect_capture.cpp`, `kinect_capture.h`):
   - Handles direct communication with the Kinect using libfreenect
   - Manages frame capture and data buffering
   - Provides a clean C interface for the Cython wrapper

2. Cython Wrapper (`kinect_wrapper.pyx`):
   - Bridges the C++ backend with Python
   - Handles memory management and type conversions

3. Python Interface:
   - Provides a simple, object-oriented API for Python users
   - Allows easy access to RGB and depth frames as NumPy arrays

4. Build System (`setup.py`):
   - Manages compilation of C++ and Cython code
   - Handles linking with libfreenect and other dependencies

## Setup and Installation

### Prerequisites

- Kinect Xbox 360 camera
- libfreenect
- Python 3.6+
- NumPy
- OpenCV (for visualization)

### Installation Steps

1. Install libfreenect:
   ```
   brew install libfreenect
   ```

2. Clone this repository:
   ```
   git clone https://github.com/yourusername/kinect-xbox360-interface.git
   cd kinect-xbox360-interface
   ```

3. Install Python dependencies:
   ```
   pip install numpy opencv-python Cython
   ```

4. Compile the Cython extension:
   ```
   python setup.py build_ext --inplace
   ```

## Usage

Here's a simple example of how to use the Kinect interface:

```python
from kinect_wrapper import PyKinectCapture
import cv2

kinect = PyKinectCapture()
kinect.init()

while True:
    rgb, depth = kinect.get_frames()
    if rgb is not None and depth is not None:
        cv2.imshow("RGB", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
        cv2.imshow("Depth", cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
```

For a more detailed example, see `test_kinect.py` in the repository.


