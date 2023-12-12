import os
from conan.tools.files import get, copy, download, unzip
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan import ConanFile


class PyBind11Conan(ConanFile):
    name = "pybind11"
    version = "2.7.1-0"
    settings = "os", "compiler", "build_type", "arch"
    description = "PyBind11 dependency"
    license = "MIT"

    def build_requirements(self): # windows only unfortunately
        if self.settings.os == "Windows":
            self.tool_requires("7zip/19.00")

    # https://github.com/conan-io/conan/issues/3287#issuecomment-993960784
    # workaround for unsupported proprietary 7z
    def system_requirements(self):
        if self.settings.os == "Linux":
            import importlib.util
            import subprocess
            import sys

            # Check if py7zr is installed
            if importlib.util.find_spec("py7zr") is None:
                # Install py7zr if not installed
                subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])
            else:
                # Skip installation if already installed
                pass

    def build(self):
        download_link = "https://d4i3qtqj3r0z5.cloudfront.net/pybind11%402.7.1-0.7z"
        expected_sha256 = "a44fe1be203d0f55aaf1f926b5578e954c4bf35d84d676f98a109e9b0d6938b9"
        # debug quick download version
        # pybind11 = "http://127.0.0.1:8000/pybind11@2.7.1-0.7z"

        download(self, download_link, filename=self.name, sha256=expected_sha256)

        if self.settings.os == "Windows":
            self.run(f"7z x {self.name}")
        elif self.settings.os == "Linux":
            import py7zr
            with py7zr.SevenZipFile(self.name, mode='r') as z:
                z.extractall(path=".")

        os.unlink(self.name)

    def package(self):
        copy(self, "*", self.build_folder, self.package_folder)

    def package_id(self):
        # This is a header-only library, no need to store any info like architecture, os, etc.
        self.info.clear()

    def package_info(self):
        cmake_base_path = os.path.join("lib", "cmake", "pybind11")
        self.cpp_info.set_property("cmake_target_name", "pybind11_all_do_not_use")
        self.cpp_info.components["headers"].includedirs = ["include"]
        self.cpp_info.components["pybind11_"].set_property("cmake_target_name", "pybind11::pybind11")
        self.cpp_info.components["pybind11_"].set_property("cmake_module_file_name", "pybind11")
        self.cpp_info.components["pybind11_"].builddirs = [cmake_base_path]
        self.cpp_info.components["pybind11_"].requires = ["headers"]
        cmake_file = os.path.join(cmake_base_path, "pybind11Common.cmake")
        # This will allows us to use the shipped cmake modules
        self.cpp_info.set_property("cmake_build_modules", [cmake_file])
        self.cpp_info.components["embed"].requires = ["pybind11_"]
        self.cpp_info.components["module"].requires = ["pybind11_"]
        self.cpp_info.components["python_link_helper"].requires = ["pybind11_"]
        self.cpp_info.components["windows_extras"].requires = ["pybind11_"]
        self.cpp_info.components["lto"].requires = ["pybind11_"]
        self.cpp_info.components["thin_lto"].requires = ["pybind11_"]
        self.cpp_info.components["opt_size"].requires = ["pybind11_"]
        self.cpp_info.components["python2_no_register"].requires = ["pybind11_"]
