import numpy as np
import cv2
from kinect_wrapper import PyKinectCapture

def main():
    # Create an instance of PyKinectCapture
    kinect = PyKinectCapture()

    # Initialize the Kinect
    if not kinect.init():
        print("Failed to initialize Kinect")
        return

    print("Kinect initialized successfully")

    # Create windows for displaying RGB and depth images
    cv2.namedWindow("RGB", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Depth", cv2.WINDOW_NORMAL)

    try:
        while True:
            # Get frames from the Kinect
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

                # Print some information about the frames
                print(f"RGB shape: {rgb.shape}, Depth shape: {depth.shape}")
                print(f"RGB dtype: {rgb.dtype}, Depth dtype: {depth.dtype}")
                print(f"RGB min: {rgb.min()}, max: {rgb.max()}")
                print(f"Depth min: {depth.min()}, max: {depth.max()}")

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        # Close all OpenCV windows
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
