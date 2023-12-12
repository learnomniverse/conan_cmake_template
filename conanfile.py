import os
from conan.tools.files import get, copy
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan import ConanFile


class OmniverseApp(ConanFile):
    name = "omniapp"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    description = "Omniverse extension application"
    license = "MIT"
    requires = [
        "kit_sdk/105.1.0",
        "nv_usd/22.11.nv.0.2.1195",
        "carb_sdk/158.2+release158",
        "pybind11/2.7.1-0",
        "python/3.10.13+nv3"
    ]

    def generate(self):
        # Generate CMake toolchain file to use the local conan with CMake
        tc = CMakeToolchain(self)
        tc.generate()
        # And all of the dependency-config.cmake stuff
        cmake = CMakeDeps(self)
        cmake.generate()
