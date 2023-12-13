Example mixed/hybrid Omniverse extension based on [`ov_utils`](https://github.com/learnomniverse/ov_utils) using Conan/CMake for dependencies handling and build system generation. This repo is a starting point for developing NVIDIA Omniverse extensions using both native C++ and Python code.

Your extension's code lives in `omni.hello.world/`. The `ov_utils` git submodule contains the necessary Conan recipes and CMake helpers to download the required dependencies to compile and link your Omniverse extension along with some CMake helpers to recreate a useful local `_build/` directory hierarchy (that includes symlinks to find stuff and have python code hot-reloading work when developing extensions).

## Building the extension from scratch

Linux
```bash
# Make sure you clone this repo with the ov_utils submodule as well
conan_cmake_template$ git clone --recursive git@github.com:learnomniverse/conan_cmake_template.git
# (otherwise use '$ git submodule update --init --recursive' if you already cloned)
conan_cmake_template$ ./ov_utils/deps/install_all_deps.sh # Download and locally install all dependencies via Conan
# Create the CMake build files that will reference Conan dependencies automatically in a _compiler/ directory
conan_cmake_template$ conan install . --output-folder _compiler
conan_cmake_template$ cd _compiler
# Execute CMake configure to generate the final Makefiles. Use the conan-linux-release preset (so that deps
# will be visible) and use the CMakeLists.txt file in the parent '..' folder.
# This will also generate the _build/ folder hierarchy of directories and symlinks.
conan_cmake_template/_compiler$ cmake --preset conan-linux-release ..
# Build the project. This is equivalent to just calling `make`
conan_cmake_template/_compiler$ cmake --build . --config Release
conan_cmake_template/_compiler$ cd ..
# Enjoy your fully-built Kit app based on your omni.hello.world extension!
conan_cmake_template$ ./_build/linux-x86_64/release/kit/kit ./_build/linux-x86_64/release/apps/omni.app.kit.dev.kit
# Create a new empty stage from the File menu and observe the console warnings!
```

Windows
```shell
# Make sure you clone this repo with the ov_utils submodule as well
conan_cmake_template> git clone --recursive git@github.com:learnomniverse/conan_cmake_template.git
# (otherwise use '$ git submodule update --init --recursive' if you already cloned)
conan_cmake_template> .\ov_utils\deps\install_all_deps.cmd # Download and locally install all dependencies via Conan
# Create the CMake build files that will reference Conan dependencies automatically in a _compiler/ directory
conan_cmake_template> conan install . --output-folder _compiler
conan_cmake_template> cd _compiler\
# Execute CMake configure to generate the final Makefiles. Use the conan-linux-release preset (so that deps
# will be visible) and use the CMakeLists.txt file in the parent '..' folder.
# This will also generate the _build/ folder hierarchy of directories and symlinks.
conan_cmake_template\_compiler> cmake --preset conan-linux-release ..
# Build the project. This is equivalent to just calling `make`
conan_cmake_template\_compiler> cmake --build . --config Release
conan_cmake_template\_compiler> cd ..
# Enjoy your fully-built Kit app based on your omni.hello.world extension!
conan_cmake_template> .\_build\windows-x86_64\release\kit\kit.exe .\_build\windows-x86_64\release\apps\omni.app.kit.dev.kit
# Create a new empty stage from the File menu and observe the console warnings!
```