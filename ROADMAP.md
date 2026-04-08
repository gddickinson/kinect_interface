# Kinect Xbox 360 Camera Interface -- Roadmap

## Current State
A high-performance Kinect interface with a C++ backend (`kinect_capture.cpp`, 120 lines), Cython bridge (`kinect_wrapper.pyx`), and Python API returning NumPy arrays. Thread-safe double buffering with pthreads. Two test scripts (`test_kinect.py` 55 lines, `quickTest.py`). The `setup.py` (27 lines) has hard-coded Homebrew paths for Apple Silicon. The compiled `.so` file is committed to the repo. Clean, minimal, and functional.

## Short-term Improvements
- [ ] Remove `kinect_wrapper.cpython-311-darwin.so` from the repo -- it should be built locally; add to `.gitignore`
- [ ] Make `setup.py` detect library paths automatically instead of hard-coding `/opt/homebrew/Cellar/` paths
- [ ] Add error messages for common failures: Kinect not connected, permission denied, libfreenect not found
- [ ] Consolidate `test_kinect.py` and `quickTest.py` into a single test/demo script
- [ ] Add a `requirements.txt` (numpy, cython, opencv-python)
- [ ] Add docstrings to the Cython wrapper class methods
- [ ] Add a `.gitignore` for `*.so`, `build/`, `__pycache__/`

## Feature Enhancements
- [ ] Add tilt motor control through the Python API (libfreenect supports this)
- [ ] Implement depth-to-point-cloud conversion returning (N,3) float array
- [ ] Add IR camera stream support (libfreenect provides IR data)
- [ ] Implement frame rate control and configurable resolution
- [ ] Add depth colorization utilities (jet, turbo, grayscale) in Python
- [ ] Implement simple background subtraction for object detection
- [ ] Add calibration routine for RGB-depth alignment
- [ ] Create a recording mode that saves synchronized RGB+depth streams to disk (e.g., .npz)

## Long-term Vision
- [ ] Add support for Kinect v2 (Xbox One) via libfreenect2
- [ ] Implement real-time skeleton/pose tracking using the depth stream
- [ ] Create a high-level `KinectApp` class with built-in visualization window
- [ ] Add ROS 2 publisher node for integration with robotics projects
- [ ] Implement gesture recognition pipeline on top of the depth stream
- [ ] Cross-platform build support (Linux, Windows) beyond current macOS-only setup

## Technical Debt
- [ ] `setup.py` hard-codes Homebrew paths -- will break on any non-Apple-Silicon Mac or Linux
- [ ] The `build/` directory is committed to the repo -- add to `.gitignore`
- [ ] No graceful shutdown if Kinect is disconnected during capture
- [ ] Thread cleanup in C++ destructor should be verified for edge cases (signal interrupts)
- [ ] No CI/CD pipeline -- hard to test without hardware, but build verification is possible
- [ ] Missing `LICENSE` file
