from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain


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
        "pybind11/2.11.1",
        "python/3.10.13+nv3"
    ]

    # Customize the name of the preset in the _compiler/CMakePresets.json after the
    # "conan-" prefix
    def layout(self):
        self.folders.build_folder_vars = ["settings.os", "settings.build_type"]

    def generate(self):
        # Generate CMake toolchain file to use the local conan with CMake
        tc = CMakeToolchain(self)
        tc.cache_variables["CMAKE_BUILD_TYPE"] = str(self.settings.build_type)
        tc.generate()
        # And all of the dependency-config.cmake stuff
        cmake = CMakeDeps(self)
        cmake.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
