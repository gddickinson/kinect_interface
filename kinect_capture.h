#ifndef KINECT_CAPTURE_H
#define KINECT_CAPTURE_H

#include <cstdint>

class KinectCapture;

extern "C" {
    KinectCapture* create_kinect_capture();
    bool init_kinect_capture(KinectCapture* capture);
    bool get_kinect_frames(KinectCapture* capture, uint8_t *rgb, uint16_t *depth);
    void destroy_kinect_capture(KinectCapture* capture);
}

#endif // KINECT_CAPTURE_H
