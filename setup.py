"""
Build configuration for the Kinect wrapper Cython extension.

Automatically detects library paths via pkg-config and Homebrew,
falling back to common system locations.
"""

import os
import subprocess
import sys
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np


def find_library_paths():
    """Detect include and library directories for libfreenect and libusb.

    Tries (in order):
      1. pkg-config
      2. Homebrew prefix (macOS)
      3. Common system paths
    """
    include_dirs = [np.get_include(), "."]
    library_dirs = []

    # Try pkg-config first
    for lib in ["libfreenect", "libusb-1.0"]:
        try:
            cflags = subprocess.check_output(
                ["pkg-config", "--cflags", lib], stderr=subprocess.DEVNULL
            ).decode().strip()
            libs = subprocess.check_output(
                ["pkg-config", "--libs-only-L", lib], stderr=subprocess.DEVNULL
            ).decode().strip()

            for flag in cflags.split():
                if flag.startswith("-I"):
                    include_dirs.append(flag[2:])
            for flag in libs.split():
                if flag.startswith("-L"):
                    library_dirs.append(flag[2:])
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    # If pkg-config didn't find anything, try Homebrew (macOS)
    if not library_dirs and sys.platform == "darwin":
        try:
            brew_prefix = subprocess.check_output(
                ["brew", "--prefix"], stderr=subprocess.DEVNULL
            ).decode().strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            brew_prefix = "/opt/homebrew" if os.path.isdir("/opt/homebrew") else "/usr/local"

        for pkg, header_subdir in [("libfreenect", "libfreenect"), ("libusb", "libusb-1.0")]:
            pkg_dir = os.path.join(brew_prefix, "opt", pkg)
            inc = os.path.join(pkg_dir, "include", header_subdir)
            lib = os.path.join(pkg_dir, "lib")
            if os.path.isdir(inc):
                include_dirs.append(inc)
            if os.path.isdir(lib):
                library_dirs.append(lib)

    # Fallback: common system paths (Linux)
    if not library_dirs:
        for path in ["/usr/include", "/usr/local/include"]:
            if os.path.isdir(os.path.join(path, "libfreenect")):
                include_dirs.append(os.path.join(path, "libfreenect"))
            if os.path.isdir(os.path.join(path, "libusb-1.0")):
                include_dirs.append(os.path.join(path, "libusb-1.0"))
        for path in ["/usr/lib", "/usr/local/lib"]:
            if os.path.isdir(path):
                library_dirs.append(path)

    return include_dirs, library_dirs


include_dirs, library_dirs = find_library_paths()

extensions = [
    Extension(
        "kinect_wrapper",
        ["kinect_wrapper.pyx", "kinect_capture.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=["freenect", "usb-1.0"],
        extra_compile_args=["-std=c++11", "-stdlib=libc++"],
        extra_link_args=["-stdlib=libc++"],
        language="c++",
    )
]

setup(
    name="kinect_wrapper",
    ext_modules=cythonize(extensions),
    install_requires=["numpy"],
)
