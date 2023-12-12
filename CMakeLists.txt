#  Written by Marco Alesiani, NVIDIA Corp (nvidia.com - malesiani)
#
#  This code is licensed under the MIT License.

#######################################################################
# Sets up an Omniverse mixed/hybrid extension project (one that uses both
# native C++ code and Python code through pybind11 bindings).

cmake_minimum_required(VERSION 3.15)
project(omni.app)

# Find required dependencies thanks to conan
# <gather_dependencies>
find_package(kit_sdk REQUIRED)
find_package(nv_usd REQUIRED)
find_package(carb_sdk REQUIRED)
find_package(python REQUIRED)
# Make totally sure that we're using the python distro shipped by conan instead of one that pybind11 _might_
# be getting from the host system (and that it could mismatch compared to the carbonite python plugin that the
# conan kit is using - see https://github.com/pybind/pybind11/issues/2154)
set(PYTHON_EXECUTABLE "${python_PACKAGE_FOLDER_RELEASE}/python")
find_package(pybind11 REQUIRED)
# </gather_dependencies>

# Just some helper functions to create symlinks, set up the folder structure in _build,
# create folders, etc.
include(tools/OVFilesystemHelper.cmake)


# Get OS_AND_ARCHITECTURE and BUILD_CONFIG variables
# <get_os_and_config_variables>
if(CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
  set(OS_AND_ARCHITECTURE "linux-x86_64")

  if(NOT CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(FATAL_ERROR "Unsupported architecture! This project requires x64 architecture.")
  endif()

elseif(CMAKE_HOST_SYSTEM_NAME STREQUAL "Windows")
  set(OS_AND_ARCHITECTURE "windows-x86_64")

  if(NOT CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(FATAL_ERROR "Unsupported architecture! This project requires x64 architecture.")
  endif()

else()
  message(FATAL_ERROR "Unsupported operating system")
endif()

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  set(BUILD_CONFIG "debug")
elseif(CMAKE_BUILD_TYPE STREQUAL "Release")
  set(BUILD_CONFIG "release")
else()
    message(FATAL_ERROR "Unsupported build type. Use Debug or Release.")
endif()
# </get_os_and_config_variables>

# Create a _build folders structure that mimicks the one that kit-extension-template sample repositories
# from NVIDIA always set up. Read create_folder_structure() to learn more.
# This will also symlink the "python/scripts" folder so that the python code of the extension will automatically
# be present in the final build directory to be executed.
# <create_build_folder_structure>
set(OMNI_HELLO_WORLD_DIR "${CMAKE_CURRENT_SOURCE_DIR}/omni.hello.world")
set(OMNI_HELLO_WORLD_BUILD_DIR "${CMAKE_CURRENT_SOURCE_DIR}/_build/${OS_AND_ARCHITECTURE}/${BUILD_CONFIG}/exts/omni.hello.world")

create_folder_structure(${CMAKE_CURRENT_SOURCE_DIR}/_build
"
${OS_AND_ARCHITECTURE}
+-- ${BUILD_CONFIG}
|   +-- apps -> ${CMAKE_CURRENT_SOURCE_DIR}/apps
|   +-- exts
|   |   +-- omni.hello.world
|   |       +-- bin
|   |       +-- config -> ${OMNI_HELLO_WORLD_DIR}/config
|   |       +-- data -> ${OMNI_HELLO_WORLD_DIR}/data
|   |       +-- docs -> ${OMNI_HELLO_WORLD_DIR}/docs
|   |       +-- omni
|   |           +-- hello
|   |               +-- world
|   |                   +-- bindings
|   |                   +-- scripts -> ${OMNI_HELLO_WORLD_DIR}/python/scripts
|   +-- kit -> ${kit_sdk_PACKAGE_FOLDER_RELEASE}
target-deps
+-- nv_usd -> ${nv_usd_PACKAGE_FOLDER_RELEASE}
+-- carb_sdk -> ${carb_sdk_PACKAGE_FOLDER_RELEASE}
+-- pybind11 -> ${pybind11_PACKAGE_FOLDER_RELEASE}
+-- python -> ${python_PACKAGE_FOLDER_RELEASE}
")
# </create_build_folder_structure>



# Generate the native C++ Carbonite plugin
# <native_carb_plugin>

# Gather all the C++ sources
set(SOURCES ${OMNI_HELLO_WORLD_DIR}/plugins/ExampleExtension.cpp)


# Add the native plugin (the release/exts/extensionname/bin/libextensionname.plugin.so)
add_library(omni.hello.world.plugin SHARED ${SOURCES})

# Set the right output folder for the binary
set(OUTPUT_DIR_FOR_NATIVE_CPP_CARB_PLUGIN "${OMNI_HELLO_WORLD_BUILD_DIR}/bin")
file(TO_NATIVE_PATH "${OUTPUT_DIR_FOR_NATIVE_CPP_CARB_PLUGIN}" OUTPUT_DIR_FOR_NATIVE_CPP_CARB_PLUGIN_NATIVE)
set_target_properties(omni.hello.world.plugin PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY $<1:${OUTPUT_DIR_FOR_NATIVE_CPP_CARB_PLUGIN_NATIVE}>
  RUNTIME_OUTPUT_DIRECTORY $<1:${OUTPUT_DIR_FOR_NATIVE_CPP_CARB_PLUGIN_NATIVE}>
  ARCHIVE_OUTPUT_DIRECTORY $<1:${OUTPUT_DIR_FOR_NATIVE_CPP_CARB_PLUGIN_NATIVE}>
)

target_include_directories(omni.hello.world.plugin PRIVATE
  ${OMNI_HELLO_WORLD_DIR}/include
)

# Link libraries from Conan packages. This also adds the include directories!
target_link_libraries(omni.hello.world.plugin PRIVATE
  nv_usd::nv_usd
  carb_sdk::carb_sdk
)

# Create a custom target to copy the __init__.py file (the only one we don't symlink)
set(SOURCE_FILE "${OMNI_HELLO_WORLD_DIR}/python/__init__.py")
set(DESTINATION_DIR "${OMNI_HELLO_WORLD_BUILD_DIR}/omni/hello/world")
file(TO_NATIVE_PATH "${SOURCE_FILE}" SOURCE_FILE_NATIVE)
file(TO_NATIVE_PATH "${DESTINATION_DIR}" DESTINATION_DIR_NATIVE)
add_custom_target(CopyPythonInitFile
    COMMAND ${CMAKE_COMMAND} -E copy "${SOURCE_FILE_NATIVE}" "${DESTINATION_DIR_NATIVE}"
    DEPENDS ${SOURCE_FILE_NATIVE}
    COMMENT "Copying main python module __init__.py to ${DESTINATION_DIR_NATIVE}"
)

# Add the custom target to the build process
add_dependencies(omni.hello.world.plugin CopyPythonInitFile)
# </native_carb_plugin>


# Now generate the python bindings project
# <pybind_plugin>

set(SOURCES ${OMNI_HELLO_WORLD_DIR}/bindings/ExampleBindings.cpp)

# add_library(omni.hello.world.python SHARED ${SOURCES})
pybind11_add_module(_example_carb_bindings SHARED ${SOURCES})

set(OUTPUT_DIR_FOR_BINDINGS_CARB_PLUGIN "${OMNI_HELLO_WORLD_BUILD_DIR}/omni/hello/world/bindings")
file(TO_NATIVE_PATH "${OUTPUT_DIR_FOR_BINDINGS_CARB_PLUGIN}" OUTPUT_DIR_FOR_BINDINGS_CARB_PLUGIN_NATIVE)
set_target_properties(_example_carb_bindings PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY $<1:${OUTPUT_DIR_FOR_BINDINGS_CARB_PLUGIN_NATIVE}>
  RUNTIME_OUTPUT_DIRECTORY $<1:${OUTPUT_DIR_FOR_BINDINGS_CARB_PLUGIN_NATIVE}>
  ARCHIVE_OUTPUT_DIRECTORY $<1:${OUTPUT_DIR_FOR_BINDINGS_CARB_PLUGIN_NATIVE}>
)

target_include_directories(_example_carb_bindings PRIVATE
  ${OMNI_HELLO_WORLD_DIR}/include
)

target_link_libraries(_example_carb_bindings PRIVATE
  nv_usd::nv_usd
  carb_sdk::carb_sdk
  pybind11::pybind11
  python::python
)

# </pybind_plugin>
