import os
from conan.tools.files import get, copy, download, unzip
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan import ConanFile


class PythonConan(ConanFile):
    name = "python"
    version = "3.10.13+nv3"
    settings = "os", "compiler", "build_type", "arch"
    description = "Python binary dependency"
    license = "MIT"

    # https://github.com/conan-io/conan/issues/3287#issuecomment-993960784
    # workaround for unsupported proprietary 7z
    def system_requirements(self):
        import subprocess
        import sys
        import importlib.util
        # Check if py7zr is installed
        if importlib.util.find_spec("py7zr") is None:
            # Install py7zr if not installed
            subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])
        else:
            # Skip installation if already installed
            pass

    def build(self):
        # python = "https://d4i3qtqj3r0z5.cloudfront.net/python%403.10.13%2Bnv3-linux-x86_64.7z"
        # debug quick download version
        python = "http://127.0.0.1:8000/python@3.10.13+nv3-linux-x86_64.7z"
        local_filename = "python.7z"

        download(self, python, filename=local_filename, md5="e468b302ba6dcfd3ec72187072a8f252")

        import py7zr
        with py7zr.SevenZipFile(local_filename, mode='r') as z:
            z.extractall(path=".")
        os.unlink(local_filename)

    def package(self):
        copy(self, "*", self.build_folder, self.package_folder)
        # copy(self, "*.lib", self.build_folder, os.path.join(self.package_folder, "lib"))
        # copy(self, "*.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        # print(f"BBBBBBBBBBBBBBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {self.package_folder}")

    def package_info(self):
        self.cpp_info.bindirs = ['bin']
        self.cpp_info.includedirs = ['include/python3.10']
        self.cpp_info.libdirs = ['lib']
        # self.cpp_info.names["cmake_find_package"] = "kit-sdk"
        # self.cpp_info.components["kit-sdk"].names["cmake_find_package"] = "kit-sdk"
        # print(f"ZUBAAAAAAAAAAAAAAAAAAAT - {self.cpp_info.components['kit-sdk']}")
        # self.cpp_info.libs = ["kit-sdk"]
        pass

