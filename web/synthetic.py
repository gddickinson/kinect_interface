"""SYNTHETIC depth frames for the demo page and tests. They are made up here (simple geometry in millimetres), not
recorded from a Kinect: the repo contains no captured frames. Same layout and dtype as PyKinectCapture.get_frames()
depth (rows x columns, uint16 mm), at a quarter of the 640 x 480 resolution.
"""
import numpy as np

W, H = 160, 120


def _grid():
    y, x = np.mgrid[0:H, 0:W].astype(np.float64)
    return x, y


def wall_and_sphere():
    """A back wall 3000-3600 mm away (further to the right) with a ball 1100 mm away in front of it."""
    x, y = _grid()
    d = 3000 + 600 * x / (W - 1)
    r2 = (x - 70) ** 2 + (y - 60) ** 2
    ball = r2 < 30 ** 2
    d[ball] = 1100 - 300 * np.sqrt(1 - r2[ball] / 30 ** 2) + 300
    return np.round(d).astype(np.uint16)


def floor_and_box():
    """A floor receding from 800 mm (bottom row) to 4000 mm (top row) with a box 1500 mm away."""
    x, y = _grid()
    d = 4000 - 3200 * y / (H - 1)
    box = (x > 95) & (x < 135) & (y > 35) & (y < 80)
    d[box] = 1500
    return np.round(d).astype(np.uint16)


def with_no_reading():
    """The wall-and-sphere frame with a band of 0 mm pixels (the value the driver gives where it measured nothing),
    as in the shadow beside a near object."""
    d = wall_and_sphere()
    d[30:90, 104:112] = 0
    d[:, :4] = 0
    return d


SCENES = {"wall_and_sphere": wall_and_sphere, "floor_and_box": floor_and_box, "with_no_reading": with_no_reading}
