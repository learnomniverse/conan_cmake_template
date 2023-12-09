import os
from conan.tools.files import get, copy, download, unzip
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan import ConanFile


class KitSDKConan(ConanFile):
    name = "kit_sdk"
    version = "105.1.0"
    settings = "os", "compiler", "build_type", "arch"
    description = "Kit SDK binary dependency"
    license = "MIT"
    # exports_sources = "*"

    # https://github.com/conan-io/conan/issues/3287#issuecomment-993960784
    # workaround for unsupported proprietary 7z
    def system_requirements(self):
        import pip
        pip.main(["install", "py7zr"])

    # def build_requirements(self): # windows only unfortunately
    #     self.tool_requires("7zip/19.00")

    # def source(self):
    #     tools.download(self.url, "kit-sdk.7z")
    #     tools.unzip("kit-sdk.7z", destination="_deps")
    def build(self):
        local_filename = "kit_sdk.7z"
        # kit_sdk = "https://d4i3qtqj3r0z5.cloudfront.net/kit-sdk%40105.1.0%2Brelease.51.a7407fb5.tc.linux-x86_64.release.7z"
        # debug quick download version
        kit_sdk = "http://127.0.0.1:8000/kit-sdk@105.1.0+release.51.a7407fb5.tc.linux-x86_64.release.7z"
        # kit_kernel = "https://d4i3qtqj3r0z5.cloudfront.net/kit-kernel%40105.1%2Brelease.127680.dd92291b.tc.linux-x86_64.release.zip"

        # https://docs.conan.io/2/tutorial/creating_packages/other_types_of_packages/package_prebuilt_binaries.html?highlight=binary
        # _os = {"Windows": "win", "Linux": "linux", "Macos": "macos"}.get(str(self.settings.os))
        # _arch = str(self.settings.arch).lower()
        #  url = "{}/{}_{}.tgz".format(base_url, _os, _arch)
        # get(self, kit_sdk, filename="kit-sdk.7z", md5="2382ac114b2d91c4cd07b51a7e2272f0")
        download(self, kit_sdk, filename=local_filename, md5="2382ac114b2d91c4cd07b51a7e2272f0")
        # get(self, kit_kernel, filename="kit_kernel.zip", md5="0363bf9d19dc9b3585a6e5b4f2bf8440")

        # self.run("7z x kit-sdk.7z")

        # unzip(self, "kit-sdk.7z")

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

    # def generate(self):
    #     tc = CMakeToolchain(self)
    #     # tc.variables["MYVAR"] = "MYVAR_VALUE"
    #     # tc.preprocessor_definitions["MYDEFINE"] = "MYDEF_VALUE"
    #     # print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {self.recipe_folder}")
    #     # tc.variables["MYVAR"] = self.package_folder
    #     tc.generate()
    #     cmake = CMakeDeps(self)
    #     cmake.generate()
