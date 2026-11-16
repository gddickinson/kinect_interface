// Stand-in for libfreenect.h with just the declarations kinect_capture.cpp uses, so the capture class can be
// compiled and its error paths tested without a Kinect or libfreenect. stub.cpp implements them and counts calls.
#pragma once
#include <cstdint>
typedef struct _freenect_context freenect_context;
typedef struct _freenect_device freenect_device;
typedef struct { int dummy; } freenect_frame_mode;
typedef enum { FREENECT_DEVICE_MOTOR = 1, FREENECT_DEVICE_CAMERA = 2 } freenect_device_flags;
typedef enum { FREENECT_RESOLUTION_MEDIUM = 1 } freenect_resolution;
typedef enum { FREENECT_DEPTH_MM = 5 } freenect_depth_format;
typedef enum { FREENECT_VIDEO_RGB = 0 } freenect_video_format;
typedef void (*freenect_depth_cb)(freenect_device *dev, void *depth, uint32_t timestamp);
typedef void (*freenect_video_cb)(freenect_device *dev, void *video, uint32_t timestamp);
int freenect_init(freenect_context **ctx, void *usb_ctx);
int freenect_shutdown(freenect_context *ctx);
void freenect_select_subdevices(freenect_context *ctx, freenect_device_flags subdevs);
int freenect_open_device(freenect_context *ctx, freenect_device **dev, int index);
int freenect_close_device(freenect_device *dev);
void freenect_set_user(freenect_device *dev, void *user);
void *freenect_get_user(freenect_device *dev);
void freenect_set_depth_callback(freenect_device *dev, freenect_depth_cb cb);
void freenect_set_video_callback(freenect_device *dev, freenect_video_cb cb);
freenect_frame_mode freenect_find_depth_mode(freenect_resolution res, freenect_depth_format fmt);
freenect_frame_mode freenect_find_video_mode(freenect_resolution res, freenect_video_format fmt);
int freenect_set_depth_mode(freenect_device *dev, const freenect_frame_mode mode);
int freenect_set_video_mode(freenect_device *dev, const freenect_frame_mode mode);
int freenect_start_depth(freenect_device *dev);
int freenect_start_video(freenect_device *dev);
int freenect_stop_depth(freenect_device *dev);
int freenect_stop_video(freenect_device *dev);
int freenect_process_events(freenect_context *ctx);
