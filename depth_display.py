"""Depth-frame display helpers, free of the Kinect driver (no kinect_wrapper / libfreenect import), so they can be
used and tested without the hardware. test_kinect.py uses them for its Depth window; the web interface reuses them.

colorize_depth(depth) does what the capture demo always did: stretch the frame's own min..max to 0..255
(cv2.normalize, NORM_MINMAX, 8-bit) and apply OpenCV's JET colour map. The result is BGR, ready for cv2.imshow.
Note that pixels the Kinect could not measure are 0 mm, so they set the minimum whenever they are present.
"""
import cv2
import numpy as np


def normalize_depth(depth: np.ndarray) -> np.ndarray:
    """uint16 depth (mm) -> uint8, the frame's minimum mapped to 0 and its maximum to 255."""
    return cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)


def colorize_depth(depth: np.ndarray) -> np.ndarray:
    """uint16 depth (mm) -> BGR uint8 image with the JET colour map (blue = nearest, red = farthest)."""
    return cv2.applyColorMap(normalize_depth(depth), cv2.COLORMAP_JET)


def jet_lut() -> list:
    """OpenCV's JET colour map as 256 [r, g, b] rows (index = normalised depth value)."""
    bgr = cv2.applyColorMap(np.arange(256, dtype=np.uint8).reshape(1, 256), cv2.COLORMAP_JET)[0]
    return [[int(b[2]), int(b[1]), int(b[0])] for b in bgr]
