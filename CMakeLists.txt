cmake_minimum_required(VERSION 3.15)
project(omni.app)

# DEBUG
message(STATUS "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")
# DEBUG


# Find kit-sdk
find_package(kit-sdk REQUIRED)







# A function that creates a symbolic link from source to destination
# Works on Linux and Windows (CMake >= 3.13)
function(create_symlink source destination)
  if (WIN32)
    # Convert CMake paths to native paths for Windows
    file(TO_NATIVE_PATH "${source}" source_native)
    file(TO_NATIVE_PATH "${destination}" destination_native)
    # Use cmd.exe to create a junction link
    execute_process(COMMAND cmd.exe /c mklink /J "${destination_native}" "${source_native}")
  else()
    # Use CMake to create a symlink on Linux
    execute_process(COMMAND "${CMAKE_COMMAND}" -E create_symlink "${source}" "${destination}")
  endif()
endfunction()












# Create the _build

# get a SYMLINK to kit-sdk!

message(WARNING "Creating symlink in ${CMAKE_CURRENT_SOURCE_DIR}")
message(WARNING "source_file ${kit-sdk}")

# execute_process(
#     COMMAND ${CMAKE_COMMAND} -E create_symlink
#         ${kit-sdk_PACKAGE_FOLDER_RELEASE}
#         ${CMAKE_CURRENT_SOURCE_DIR}/kit
#     WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
# )

create_symlink(${kit-sdk_PACKAGE_FOLDER_RELEASE} ${CMAKE_CURRENT_SOURCE_DIR}/kit)









# Add plugin (the release/exts/extensionname/bin/libextensionname.plugin.so)
# add_library(omni.app SHARED plugin/StartingMainCppFile.cpp)
# target_link_libraries(omni.app PRIVATE kit-sdk::kit-sdk)
