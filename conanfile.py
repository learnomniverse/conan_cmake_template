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
        "kit-sdk/105.1.0"
    ]

    def generate(self):
        tc = CMakeToolchain(self)
        # tc.variables["MYVAR"] = "MYVAR_VALUE"
        # tc.preprocessor_definitions["MYDEFINE"] = "MYDEF_VALUE"
        # print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {self.recipe_folder}")
        # tc.variables["MYVAR"] = self.package_folder
        tc.generate()
        cmake = CMakeDeps(self)
        cmake.generate()
