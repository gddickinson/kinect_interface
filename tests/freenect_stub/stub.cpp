// Stub libfreenect + a test driver for kinect_capture.cpp's lifecycle. Usage: stub <scenario>
//   no-init     freenect_init fails      -> create, init (false), destroy
//   no-device   freenect_open_device fails -> create, init (false), destroy
//   never-init  create and destroy without calling init
//   ok          init succeeds (fake device), destroy
// Prints the number of freenect_shutdown calls and "done" if destruction returned normally.
#include <cstdio>
#include <cstring>
#include <string>
#include "libfreenect.h"
#include "../../kinect_capture.h"

static std::string scenario;
static int shutdowns = 0, events = 0;
static char ctx_obj[8], dev_obj[8];
static void *user = nullptr;

int freenect_init(freenect_context **ctx, void *) {
  if (scenario == "no-init") return -1;
  *ctx = (freenect_context *)ctx_obj; return 0;
}
int freenect_shutdown(freenect_context *) { shutdowns++; return 0; }
void freenect_select_subdevices(freenect_context *, freenect_device_flags) {}
int freenect_open_device(freenect_context *, freenect_device **dev, int) {
  if (scenario == "no-device") return -1;
  *dev = (freenect_device *)dev_obj; return 0;
}
int freenect_close_device(freenect_device *) { return 0; }
void freenect_set_user(freenect_device *, void *u) { user = u; }
void *freenect_get_user(freenect_device *) { return user; }
void freenect_set_depth_callback(freenect_device *, freenect_depth_cb) {}
void freenect_set_video_callback(freenect_device *, freenect_video_cb) {}
freenect_frame_mode freenect_find_depth_mode(freenect_resolution, freenect_depth_format) { return {0}; }
freenect_frame_mode freenect_find_video_mode(freenect_resolution, freenect_video_format) { return {0}; }
int freenect_set_depth_mode(freenect_device *, const freenect_frame_mode) { return 0; }
int freenect_set_video_mode(freenect_device *, const freenect_frame_mode) { return 0; }
int freenect_start_depth(freenect_device *) { return 0; }
int freenect_start_video(freenect_device *) { return 0; }
int freenect_stop_depth(freenect_device *) { return 0; }
int freenect_stop_video(freenect_device *) { return 0; }
int freenect_process_events(freenect_context *) { events++; return events > 1000000 ? -1 : 0; }

int main(int argc, char **argv) {
  scenario = argc > 1 ? argv[1] : "ok";
  KinectCapture *k = create_kinect_capture();
  if (scenario != "never-init") std::printf("init %d\n", (int)init_kinect_capture(k));
  destroy_kinect_capture(k);
  std::printf("shutdowns %d\ndone\n", shutdowns);
  return 0;
}
