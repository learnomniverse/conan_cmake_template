import os
from conan.tools.files import get, copy, download, unzip
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan import ConanFile


class NvUsdConan(ConanFile):
    name = "nv_usd"
    version = "22.11.nv.0.2.1195"
    settings = "os", "compiler", "build_type", "arch"
    description = "Kit SDK binary dependency"
    license = "MIT"

    # https://github.com/conan-io/conan/issues/3287#issuecomment-993960784
    # workaround for unsupported proprietary 7z
    def system_requirements(self):
        import pip
        pip.main(["install", "py7zr"])

    def build(self):
        # nv_usd = "https://d4i3qtqj3r0z5.cloudfront.net/nv-usd%4022.11.nv.0.2.1195.84b2e524-linux64_py310-centos_release-releases-105-1.7z"
        # debug quick download version
        nv_usd = "http://127.0.0.1:8000/nv-usd@22.11.nv.0.2.1195.84b2e524-linux64_py310-centos_release-releases-105-1.7z"
        local_filename = "nv_usd.7z"

        download(self, nv_usd, filename=local_filename, md5="b8abd8ccf51d42dde52010a898f9dbc2")

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
        # self.cpp_info.names["cmake_find_package"] = "kit-sdk"
        # self.cpp_info.components["kit-sdk"].names["cmake_find_package"] = "kit-sdk"
        # print(f"ZUBAAAAAAAAAAAAAAAAAAAT - {self.cpp_info.components['kit-sdk']}")
        # self.cpp_info.libs = ["kit-sdk"]
        pass

