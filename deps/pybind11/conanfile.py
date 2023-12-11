import os
from conan.tools.files import get, copy, download, unzip
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan import ConanFile


class PyBind11Conan(ConanFile):
    name = "pybind11"
    version = "2.7.1-0"
    settings = "os", "compiler", "build_type", "arch"
    description = "PyBind11 binary dependency"
    license = "MIT"

    # https://github.com/conan-io/conan/issues/3287#issuecomment-993960784
    # workaround for unsupported proprietary 7z
    def system_requirements(self):
        import subprocess
        import sys
        # pip.main(["install", "py7zr"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])

    def build(self):
        # pybind11 = "https://d4i3qtqj3r0z5.cloudfront.net/pybind11%402.7.1-0.7z"
        # debug quick download version
        pybind11 = "http://127.0.0.1:8000/pybind11@2.7.1-0.7z"
        local_filename = "pybind11.7z"

        download(self, pybind11, filename=local_filename, md5="7e13af10d18fc7a19f10a2633432b633")

        import py7zr
        with py7zr.SevenZipFile(local_filename, mode='r') as z:
            z.extractall(path=".")
        os.unlink(local_filename)

    def package(self):
        copy(self, "*.*", self.build_folder, self.package_folder)
        # copy(self, "*.lib", self.build_folder, os.path.join(self.package_folder, "lib"))
        # copy(self, "*.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        # print(f"BBBBBBBBBBBBBBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {self.package_folder}")

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib']
        # self.cpp_info.names["cmake_find_package"] = "kit-sdk"
        # self.cpp_info.components["kit-sdk"].names["cmake_find_package"] = "kit-sdk"
        # print(f"ZUBAAAAAAAAAAAAAAAAAAAT - {self.cpp_info.components['kit-sdk']}")
        # self.cpp_info.libs = ["kit-sdk"]
        pass

