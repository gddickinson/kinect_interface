"""
Kinect Xbox 360 test and demo script.

Initializes the Kinect sensor, captures RGB and depth frames,
and displays them in OpenCV windows. Press 'q' to quit.

Consolidates the former test_kinect.py and quickTest.py.
"""

import sys
import numpy as np

try:
    import cv2
except ImportError:
    print("ERROR: opencv-python is required. Install with: pip install opencv-python")
    sys.exit(1)

try:
    from kinect_wrapper import PyKinectCapture
except ImportError:
    print(
        "ERROR: kinect_wrapper module not found.\n"
        "Build it first with: python setup.py build_ext --inplace\n"
        "Make sure libfreenect is installed (brew install libfreenect on macOS)."
    )
    sys.exit(1)


def main():
    """Run the Kinect capture demo."""
    kinect = PyKinectCapture()

    if not kinect.init():
        print(
            "Failed to initialize Kinect.\n"
            "Check that:\n"
            "  - The Kinect is plugged in (USB + power)\n"
            "  - You have permission to access USB devices\n"
            "  - libfreenect is installed correctly"
        )
        return

    print("Kinect initialized successfully")
    print("Press 'q' to quit")

    cv2.namedWindow("RGB", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Depth", cv2.WINDOW_NORMAL)

    try:
        while True:
            rgb, depth = kinect.get_frames()

            if rgb is not None and depth is not None:
                rgb_display = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)

                depth_display = cv2.normalize(
                    depth, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
                )
                depth_colormap = cv2.applyColorMap(depth_display, cv2.COLORMAP_JET)

                cv2.imshow("RGB", rgb_display)
                cv2.imshow("Depth", depth_colormap)

                print(
                    f"RGB: {rgb.shape} {rgb.dtype} [{rgb.min()}-{rgb.max()}]  "
                    f"Depth: {depth.shape} {depth.dtype} [{depth.min()}-{depth.max()}]"
                )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user")

    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
