from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "kinect_wrapper",
        ["kinect_wrapper.pyx", "kinect_capture.cpp"],
        include_dirs=[
            np.get_include(),
            "/opt/homebrew/Cellar/libfreenect/0.7.5/include/libfreenect",
            "/opt/homebrew/Cellar/libusb/1.0.27/include/libusb-1.0",
            "."  # Include current directory for kinect_capture.h
        ],
        library_dirs=["/opt/homebrew/Cellar/libfreenect/0.7.5/lib", "/opt/homebrew/Cellar/libusb/1.0.27/lib"],
        libraries=["freenect", "usb-1.0"],
        extra_compile_args=["-std=c++11", "-stdlib=libc++"],
        extra_link_args=["-stdlib=libc++"],
        language="c++"
    )
]

setup(
    name="kinect_wrapper",
    ext_modules=cythonize(extensions),
    install_requires=['numpy'],
)
