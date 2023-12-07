cmake_minimum_required(VERSION 3.15)
project(omni.example.deps)

message(STATUS "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")


# Find kit-sdk
find_package(kit-sdk REQUIRED)

# Add plugin
add_library(omni.hello.world SHARED plugin/StartingMainCppFile.cpp)
target_link_libraries(omni.hello.world PRIVATE kit-sdk::kit-sdk)
