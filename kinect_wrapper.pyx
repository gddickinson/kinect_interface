# cython: language_level=3
import numpy as np
cimport numpy as np
from libcpp cimport bool
from libc.stdint cimport uint8_t, uint16_t

cdef extern from "kinect_capture.h":
    cdef cppclass KinectCapture:
        pass

    KinectCapture* create_kinect_capture()
    bool init_kinect_capture(KinectCapture* capture)
    bool get_kinect_frames(KinectCapture* capture, uint8_t *rgb, uint16_t *depth)
    void destroy_kinect_capture(KinectCapture* capture)

cdef class PyKinectCapture:
    """Python wrapper for the Kinect Xbox 360 capture interface.

    Provides thread-safe access to RGB and depth frames via a C++
    backend using libfreenect with double buffering.

    Usage:
        kinect = PyKinectCapture()
        if kinect.init():
            rgb, depth = kinect.get_frames()
    """
    cdef KinectCapture* _capture

    def __cinit__(self):
        """Create the underlying C++ KinectCapture object."""
        self._capture = create_kinect_capture()

    def __dealloc__(self):
        """Release the C++ KinectCapture and close the Kinect device."""
        if self._capture is not NULL:
            destroy_kinect_capture(self._capture)

    def init(self):
        """Initialize the Kinect sensor.

        Returns:
            bool: True if the Kinect was opened successfully, False otherwise.
        """
        return init_kinect_capture(self._capture)

    def get_frames(self):
        """Capture the latest RGB and depth frames.

        Returns:
            tuple: (rgb, depth) where rgb is a (480, 640, 3) uint8 ndarray
                   and depth is a (480, 640) uint16 ndarray, or (None, None)
                   if capture failed.
        """
        cdef np.ndarray[np.uint8_t, ndim=3] rgb = np.empty((480, 640, 3), dtype=np.uint8)
        cdef np.ndarray[np.uint16_t, ndim=2] depth = np.empty((480, 640), dtype=np.uint16)

        success = get_kinect_frames(self._capture, &rgb[0,0,0], &depth[0,0])

        if success:
            return rgb, depth
        else:
            return None, None
