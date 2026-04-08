from kinect_wrapper import PyKinectCapture
import cv2

kinect = PyKinectCapture()
kinect.init()

while True:
    rgb, depth = kinect.get_frames()
    if rgb is not None and depth is not None:
        # Convert RGB from BGR to RGB color space
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)

        # Normalize depth for display
        depth_display = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        depth_colormap = cv2.applyColorMap(depth_display, cv2.COLORMAP_JET)

        # Display the images
        cv2.imshow("RGB", rgb)
        cv2.imshow("Depth", depth_colormap)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
