#include "kinect_capture.h"
#include "libfreenect.h"
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <vector>
#include <pthread.h>
#include <atomic>

class KinectCapture {
private:
    freenect_context *f_ctx;
    freenect_device *f_dev;

    std::vector<uint8_t> depth_buffer;
    std::vector<uint8_t> rgb_buffer;

    pthread_t freenect_thread;
    std::atomic<bool> die;

    pthread_mutex_t buffer_mutex;
    pthread_cond_t frame_cond;

    static void *freenect_threadfunc(void *arg) {
        KinectCapture *kinect = static_cast<KinectCapture*>(arg);
        while (!kinect->die && freenect_process_events(kinect->f_ctx) >= 0) {}
        return nullptr;
    }

    static void depth_cb(freenect_device *dev, void *v_depth, uint32_t timestamp) {
        KinectCapture *kinect = static_cast<KinectCapture*>(freenect_get_user(dev));
        pthread_mutex_lock(&kinect->buffer_mutex);
        memcpy(kinect->depth_buffer.data(), v_depth, kinect->depth_buffer.size());
        pthread_cond_signal(&kinect->frame_cond);
        pthread_mutex_unlock(&kinect->buffer_mutex);
    }

    static void rgb_cb(freenect_device *dev, void *v_rgb, uint32_t timestamp) {
        KinectCapture *kinect = static_cast<KinectCapture*>(freenect_get_user(dev));
        pthread_mutex_lock(&kinect->buffer_mutex);
        memcpy(kinect->rgb_buffer.data(), v_rgb, kinect->rgb_buffer.size());
        pthread_cond_signal(&kinect->frame_cond);
        pthread_mutex_unlock(&kinect->buffer_mutex);
    }

public:
    KinectCapture() : f_ctx(nullptr), f_dev(nullptr), die(false) {
        pthread_mutex_init(&buffer_mutex, nullptr);
        pthread_cond_init(&frame_cond, nullptr);
        depth_buffer.resize(640 * 480 * 2);  // 16-bit depth
        rgb_buffer.resize(640 * 480 * 3);    // RGB
    }

    ~KinectCapture() {
        die = true;
        pthread_join(freenect_thread, nullptr);
        if (f_dev) {
            freenect_stop_depth(f_dev);
            freenect_stop_video(f_dev);
            freenect_close_device(f_dev);
        }
        if (f_ctx) {
            freenect_shutdown(f_ctx);
        }
        pthread_mutex_destroy(&buffer_mutex);
        pthread_cond_destroy(&frame_cond);
    }

    bool init() {
        if (freenect_init(&f_ctx, nullptr) < 0) {
            std::cerr << "freenect_init() failed" << std::endl;
            return false;
        }

        freenect_select_subdevices(f_ctx, static_cast<freenect_device_flags>(FREENECT_DEVICE_MOTOR | FREENECT_DEVICE_CAMERA));

        if (freenect_open_device(f_ctx, &f_dev, 0) < 0) {
            std::cerr << "Could not open device" << std::endl;
            freenect_shutdown(f_ctx);
            return false;
        }

        freenect_set_user(f_dev, this);
        freenect_set_depth_callback(f_dev, depth_cb);
        freenect_set_video_callback(f_dev, rgb_cb);
        freenect_set_depth_mode(f_dev, freenect_find_depth_mode(FREENECT_RESOLUTION_MEDIUM, FREENECT_DEPTH_MM));
        freenect_set_video_mode(f_dev, freenect_find_video_mode(FREENECT_RESOLUTION_MEDIUM, FREENECT_VIDEO_RGB));

        freenect_start_depth(f_dev);
        freenect_start_video(f_dev);

        pthread_create(&freenect_thread, nullptr, freenect_threadfunc, this);
        return true;
    }

    bool getFrames(uint8_t *rgb, uint16_t *depth) {
        pthread_mutex_lock(&buffer_mutex);
        pthread_cond_wait(&frame_cond, &buffer_mutex);
        memcpy(rgb, rgb_buffer.data(), rgb_buffer.size());
        memcpy(depth, depth_buffer.data(), depth_buffer.size());
        pthread_mutex_unlock(&buffer_mutex);
        return true;
    }
};

KinectCapture* create_kinect_capture() {
    return new KinectCapture();
}

bool init_kinect_capture(KinectCapture* capture) {
    return capture->init();
}

bool get_kinect_frames(KinectCapture* capture, uint8_t *rgb, uint16_t *depth) {
    return capture->getFrames(rgb, depth);
}

void destroy_kinect_capture(KinectCapture* capture) {
    delete capture;
}
