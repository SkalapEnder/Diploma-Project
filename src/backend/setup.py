import os
import shutil
import glob
from setuptools import setup, Extension
import pybind11

def cleanup_build():
    if os.path.exists("build"):
        print("Cleaning up: removing 'build' folder...")
        shutil.rmtree("build")

    pyd_files = glob.glob("backend_module*.pyd")
    for pyd in pyd_files:
        try:
            print(f"Cleaning up: removing {pyd}...")
            os.remove(pyd)
        except OSError as e:
            print(f"Warning: Could not remove {pyd}. Ensure it is not in use by another app. Error: {e}")

cleanup_build()

opencv_path = r"C:/CV/install"

ext_modules = [
    Extension(
        "backend_module",
        ["backend.cpp"],
        include_dirs=[
            pybind11.get_include(),
            opencv_path + r"/include", 
        ],
        library_dirs=[
            opencv_path + r"/x64/vc17/lib",
        ],
        libraries=[
            "opencv_world4120"
        ],
        language="c++",
        extra_compile_args=['/std:c++17'],
    ),
]

setup(
    name="backend",
    ext_modules=ext_modules,
)