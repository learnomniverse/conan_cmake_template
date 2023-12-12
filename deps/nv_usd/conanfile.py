import os
from conan.tools.files import get, copy, download, unzip
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan import ConanFile


class NvUsdConan(ConanFile):
    name = "nv_usd"
    version = "22.11.nv.0.2.1195"
    settings = "os", "compiler", "build_type", "arch"
    description = "NVIDIA OpenUSD dependency"
    license = "MIT"

    # def build_requirements(self): # windows only unfortunately
    #     self.tool_requires("7zip/19.00")
    # https://github.com/conan-io/conan/issues/3287#issuecomment-993960784
    # workaround for unsupported proprietary 7z
    def system_requirements(self):
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

        if self.settings.arch == "x86_64" and self.settings.os == "Linux" and self.settings.build_type == "Release":
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/nv-usd@22.11.nv.0.2.1195.84b2e524-linux64_py310-centos_release-releases-105-1.7z"
            expected_sha256 = "36e5dcf974d48f801aa4684b824ae99808db9cacf8c7cd1ee724847bac82aa0a"
        elif self.settings.arch == "x86_64" and self.settings.os == "Linux" and self.settings.build_type == "Debug":
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/nv-usd@22.11.nv.0.2.1195.84b2e524-linux64_py310-centos_debug-releases-105-1.7z"
            expected_sha256 = "4b6381f5ca79edb9213759ad06220d2eafd3f97c386e3a190c851d75fe3661c9"
        elif self.settings.arch == "x86_64" and self.settings.os == "Windows" and self.settings.build_type == "Release":
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/nv-usd%4022.11.nv.0.2.1195.84b2e524-win64_py310_release-releases-105-1.7z"
            expected_sha256 = "bc9eca8637df59bbfc7b34be788e7f47f8beacdb4e32ed4eff0b12eaa2a93004"
        elif self.settings.arch == "x86_64" and self.settings.os == "Windows" and self.settings.build_type == "Debug":
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/nv-usd%4022.11.nv.0.2.1195.84b2e524-win64_py310_debug-releases-105-1.7z"
            expected_sha256 = "8a00d33ee33366087012d6aa559dd1b11b13ef89a11b850d5e068f99615b69df"
        else:
            raise ConanInvalidConfiguration(f"Unsupported triple {self.settings.arch}-{self.settings.os}")

        # debug quick download version
        # nv_usd = "http://127.0.0.1:8000/nv-usd@22.11.nv.0.2.1195.84b2e524-linux64_py310-centos_release-releases-105-1.7z"

        download(self, download_link, filename=self.name, sha256=expected_sha256)

        import py7zr
        with py7zr.SevenZipFile(self.name, mode='r') as z:
            z.extractall(path=".")
        os.unlink(self.name)

    def package(self):
        copy(self, "*", self.build_folder, self.package_folder)

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib']
