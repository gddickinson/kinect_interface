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
    cdef KinectCapture* _capture

    def __cinit__(self):
        self._capture = create_kinect_capture()

    def __dealloc__(self):
        if self._capture is not NULL:
            destroy_kinect_capture(self._capture)

    def init(self):
        return init_kinect_capture(self._capture)

    def get_frames(self):
        cdef np.ndarray[np.uint8_t, ndim=3] rgb = np.empty((480, 640, 3), dtype=np.uint8)
        cdef np.ndarray[np.uint16_t, ndim=2] depth = np.empty((480, 640), dtype=np.uint16)

        success = get_kinect_frames(self._capture, &rgb[0,0,0], &depth[0,0])

        if success:
            return rgb, depth
        else:
            return None, None
