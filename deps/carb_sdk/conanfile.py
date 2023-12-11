import os
from conan.tools.files import get, copy, download, unzip
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan import ConanFile


class CarbSDKConan(ConanFile):
    name = "carb_sdk"
    version = "158.2+release158"
    settings = "os", "compiler", "build_type", "arch"
    description = "Carb SDK binary dependency"
    license = "MIT"
    # exports_sources = "*"

    # https://github.com/conan-io/conan/issues/3287#issuecomment-993960784
    # workaround for unsupported proprietary 7z
    def system_requirements(self):
        import subprocess
        import sys
        # pip.main(["install", "py7zr"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])

    # def build_requirements(self): # windows only unfortunately
    #     self.tool_requires("7zip/19.00")

    # def source(self):
    #     tools.download(self.url, "kit-sdk.7z")
    #     tools.unzip("kit-sdk.7z", destination="_deps")
    def build(self):
        local_filename = "carb_sdk.7z"
        # carb_sdk = "https://d4i3qtqj3r0z5.cloudfront.net/carb_sdk%2Bplugins.linux-x86_64%40158.2%2Brelease158.tc9429.489984ef.7z"
        # debug quick download version
        carb_sdk = "http://127.0.0.1:8000/carb_sdk+plugins.linux-x86_64@158.2+release158.tc9429.489984ef.7z"

        # https://docs.conan.io/2/tutorial/creating_packages/other_types_of_packages/package_prebuilt_binaries.html?highlight=binary
        # _os = {"Windows": "win", "Linux": "linux", "Macos": "macos"}.get(str(self.settings.os))
        # _arch = str(self.settings.arch).lower()
        #  url = "{}/{}_{}.tgz".format(base_url, _os, _arch)
        # get(self, kit_sdk, filename="kit-sdk.7z", md5="2382ac114b2d91c4cd07b51a7e2272f0")
        download(self, carb_sdk, filename=local_filename, md5="77d6b08bf6b71fafd2bb9d60fef15c0f")
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
        self.cpp_info.includedirs = ['include']

        # Add carb_sdk/_build/[os]/[config] as a linking directory
        if self.settings.os == "Linux":
            os_folder = "linux-x86_64"
        elif self.settings.os == "Windows":
            os_folder = "windows-x86_64"
        else:
            raise ConanInvalidConfiguration("Unsupported OS")

        config_folder = str(self.settings.build_type).lower()
        build_folder = os.path.join("_build", os_folder, config_folder)
        self.cpp_info.libdirs.append(build_folder)

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
