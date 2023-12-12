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

        # Note: we don't pull debug deps for this package
        if self.settings.arch == "x86_64" and self.settings.os == "Linux":
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/carb_sdk%2Bplugins%2Elinux-x86_64%40158%2E2%2Brelease158%2Etc9429%2E489984ef%2E7z"
            expected_sha256 = "937e737f886e2c5f92d4f8f824f83d0e0ae55935b73c744ce2d2a91ffdb1a69a"
        elif self.settings.arch == "x86_64" and self.settings.os == "Windows":
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/carb_sdk%2Bplugins%2Ewindows-x86_64%40158%2E2%2Brelease158%2Etc9429%2E489984ef%2E7z"
            expected_sha256 = "1cdc98208686991f96d36c09651ace3faa8e241afad43031ced30755ee753bc4"
        else:
            raise ConanInvalidConfiguration(f"Unsupported triple {self.settings.arch}-{self.settings.os}")

        # debug quick download version
        # file_to_download = "http://127.0.0.1:8000/carb_sdk+plugins.linux-x86_64@158.2+release158.tc9429.489984ef.7z"

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

        self.cpp_info.libs = ['carb']

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
