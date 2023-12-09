cmake_minimum_required(VERSION 3.15)
project(omni.app)

# DEBUG
message(STATUS "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")
# DEBUG




## ADESSO: scarica le dipendenze necessarie trovando gli URL da packman (tutto quello che c'è in
# kit-extension-py-cpp-deps in target-deps va scaricato e usato, kit-sdk va bene anche così come c'è adesso
# che tanto ci serve solo la var kit-sdk_PACKAGE_FOLDER_RELEASE per symlinkarlo)
# e poi crea la folder structure con la funzione qua sotto.
# Poi,  finalmente, scrivi il VERO cmake add_library per il release/exts/extensionname/bin/libextensionname.plugin.so e tenta di compilare un plugin carbon nativo. Suggerisco iniziare SENZA Pybind.
# Ancora meglio: 3 step e 3 estensioni: una py only, una native only e una pybind. La prima sarà solo da
# far funzionare i symlink. Fregatene di kit kernel sinceramente.. lo spiegherai dopo che gli utenti possono ridistribuire SENZA usare questa robaccia. Farei proprio un repo a parte magari con un submodule git dove metti tutti sti script conan e cmake.
# nice to have: muovere tutta la logica cmake comune in un file cmake (tipo per le cartelle) E le dipendenze in un submodule git che sarà un repo tipo "public_ov_tools" o qualcosa del genere.



##################################### UTILITY STUFF ###########################################################

# A function that creates a symbolic link from source to destination in a working directory
# Works on Linux and Windows (CMake >= 3.13).
#
# Example: create_symlink("/usr/local/bin" "usr" "/home/alex/hello")
function(create_symlink destination symlink_name working_directory)
  if (WIN32)
    # Convert CMake paths to native paths for Windows
    file(TO_NATIVE_PATH "${symlink_name}" symlink_name_native)
    file(TO_NATIVE_PATH "${destination}" destination_native)
    file(TO_NATIVE_PATH "${working_directory}" working_directory_native)
    # Use cmd.exe to create a junction link
    execute_process(COMMAND cmd.exe /c cd "${working_directory_native}" && mklink /J "${symlink_name_native}" "${destination_native}")
  else()
    # Use CMake to create a symlink on Linux
    execute_process(COMMAND "${CMAKE_COMMAND}" -E create_symlink "${destination}" "${symlink_name}" WORKING_DIRECTORY "${working_directory}")
  endif()
endfunction()

function(create_new_folder parent_folder folder_name)
  # Create the full path for the folder
  set(folder_path "${parent_folder}/${folder_name}")
  file(TO_NATIVE_PATH "${folder_path}" folder_path_native)

  # Create the folder if it does not exist
  file(MAKE_DIRECTORY "${folder_path_native}")
endfunction()


# Define a function named get_writing_folder that takes one argument: folder_stack
function(get_writing_folder_from_folder_stack folder_stack)
  # message("get_writing_folder_from_folder_stack called with folder_stack: ${folder_stack}")
  # Get all elements in folder_stack and join them together in a single path
  list(LENGTH folder_stack folder_stack_size)
  set(writing_folder "")

  if(folder_stack_size STREQUAL 0)
    set(writing_folder "${writing_folder}" PARENT_SCOPE)
    return()
  endif()

  message("foreach index RANGE 0 ${folder_stack_size}-1")

  # Iterate through folder_stack to create the path
  math(EXPR count "${folder_stack_size} - 1")
  foreach(index RANGE 0 ${count})
    # message("get item at index ${index}")
    list(GET folder_stack ${index} folder_element)
    if (folder_element)
      # Concatenate folder_element to writing_folder
      set(writing_folder "${writing_folder}/${folder_element}")
    endif()
  endforeach()
  # Remove leading "/" if it exists
  string(REGEX REPLACE "^/" "" writing_folder "${writing_folder}")

  # Return the writing_folder variable
  set(writing_folder "${writing_folder}" PARENT_SCOPE)
  return()
endfunction()




# Creates a folder structure made of new folders and symlinks (Windows or Unix)
#
# Example:
#    create_folder_structure(${CMAKE_CURRENT_SOURCE_DIR}/root_dir
#    "
#    ${some_cmake_folder_name}
#    +-- ${another_folder_name}
#    |   +-- usr -> /usr/local/bin
#    |   +-- usr2 -> ${some_folder_path}
#    +-- include
#    |   +-- usrTEMP -> ${some_other_folder_path}
#    +-- lib
#    |   +-- usr -> /usr/local/lib
#    +-- src
#        +-- ${some_more_folder_name}
#        |   +-- this is a great folder!
#        +-- other_folder
#    ")
#
# Why this function: because programmers should have their fun too.
function(create_folder_structure root_folder ascii_art)
  # Split the ASCII art into lines
  string(REPLACE "\n" ";" ascii_lines "${ascii_art}")
  # message(WARNING "input: ${ascii_lines}")

#   foreach(line IN LISTS ascii_lines)
#       message(WARNING "line: ${line}")
#   endforeach()

  # Keep track of the current indentation level and parent folder
  set(folder_stack "")
  set(last_folder_created "")

  message("---------------------------------------------------------------")

  # Loop through each line of the ASCII art
  foreach(line IN LISTS ascii_lines)
    # Skip empty lines
    if(NOT line STREQUAL "")
      # Count the number of non-useful chars at the beginning of the line
      message("[line analysis start for line ${line}]")

      string(LENGTH "${line}" line_length)
      # Initialize the index of the first non-graphical character
      set(first_non_graphical_pos -1)

      # Loop over each character in the line
      set(i 0)
      while(i LESS line_length)
        # Get the current character
        string(SUBSTRING "${line}" "${i}" "1" current_char)

        # Check if the current character is one of the graphical characters
        if(current_char STREQUAL "+" OR
            current_char STREQUAL " " OR
            current_char STREQUAL "-" OR
            current_char STREQUAL "|")
            # Skip the current character and increment the index
            math(EXPR i "${i} + 1")
        else()
            # Found the first non-graphical character, break the loop
            set(first_non_graphical_pos "${i}")
            break()
        endif()
      endwhile()

      # Check if the first non-graphical character was not found
      if(first_non_graphical_pos EQUAL -1)
        # Maybe it's a useless graphical line, e.g. "|", continue
        message("skipping graphical-only line..")
        continue()
      endif()

      # Extract the useful part of the line
      string(SUBSTRING "${line}" "${first_non_graphical_pos}" "-1" useful_part)



      # Check if the line has the form of a symlink or just a folder name
      set(is_symlink FALSE)
      if(useful_part MATCHES "^(.+)\\s*->\\s*(.+)$")
        message("Detected as a symlink: ${useful_part}..")
        set(is_symlink TRUE)
        # Trim the whitespace from the source and destination
        string(STRIP "${CMAKE_MATCH_1}" symlink_name)
        string(STRIP "${CMAKE_MATCH_2}" symlink_destination)
      else()
        message("Detected as a simple folder name (not symlink): ${useful_part}...")
        # Trim the whitespace from the folder name
        string(STRIP "${useful_part}" folder_name)
      endif()


      string(LENGTH "${useful_part}" useful_part_count)
      math(EXPR indent_count "${line_length} - ${useful_part_count}")

      # Divide the indent count by four to get the indent level
      math(EXPR indent_count "${indent_count} / 4")
      # math(EXPR indent_count "${indent_count} + 1")

      list(LENGTH folder_stack current_indent_level)

      message("indent_count is now ${indent_count} while our current indent_level is ${current_indent_level}")
      if(indent_count GREATER current_indent_level)
        message("INCREASING OUR CURRENT_INDENT_LEVEL  (if this is not a symlink, that is)")

        # Safety: we cannot increase indent_level by more than one at once!
        MATH(EXPR expected_indent_count "${current_indent_level} + 1")
        if (NOT indent_count EQUAL expected_indent_count)
          message(FATAL_ERROR "Trying to create a subfolder with an indentation level of more than once at once!")
        endif()

        # Safety: we cannot insert a sub-element if the last inserted folder was a symlink
        if (last_folder_created STREQUAL "")
          message(FATAL_ERROR "Trying to create a subfolder on a symlink parent!")
        endif()

        list(APPEND folder_stack "${last_folder_created}")

        # get_writing_folder_from_folder_stack("${folder_stack}") # this sets the writing_folder var

        message("Level has been INCREASED")


      elseif(indent_count LESS current_indent_level)
        # Time to go some levels up (could be more than one here!)

        math(EXPR pop_count "${current_indent_level} - ${indent_count}")
        foreach(i RANGE 1 ${pop_count})
          list(POP_BACK folder_stack dropped_folder)
        endforeach()

        # list(GET folder_stack -1 parent_folder)
        # # Set the current indent level to the new indent count
        # set(current_indent_level "${indent_count}")



        message("Level has been DECREASED")
      else()
        # same level, compose whatever's on the stack and use it as it is
        # get_writing_folder_from_folder_stack("${folder_stack}") # this sets the writing_folder var
        message("level has been KEPT THE SAME")
      endif()


      get_writing_folder_from_folder_stack("${folder_stack}") # this sets the writing_folder var
      message(">>>>>->>>>here's where we should write the new element: ${writing_folder}")

      # Finally compose the final writing folder
      if(NOT writing_folder STREQUAL "")
          set(writing_folder_absolute "${root_folder}/${writing_folder}")
      else()
          set(writing_folder_absolute "${root_folder}")
      endif()


      # message("Now operating in this folder for the next operation: ${writing_folder_absolute}, stack is: ${folder_stack}")

      # Drop graphical useless characters
      # string(SUBSTRING ${line} ${indent_count} -1 no_ascii_art_content)


      # message("current_indent_level: ${current_indent_level}, current_folder: ${current_folder}, useful_part: '${useful_part}', useful_part_count: ${useful_part_count}")

      # Extract the folder name or the symlink source and destination from the line
    #   string(REGEX REPLACE "^ *\\|?\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- " "" folder_or_symlink "${line}")

      # list(GET folder_stack -1 parent_folder)

      if(is_symlink)
        # message("Folder name: ${CMAKE_MATCH_1}")
        # message("Symlink destination: ${CMAKE_MATCH_2}")

        # # Split the line by the '->' symbol
        # string(REPLACE "->" ";" symlink_parts "${folder_or_symlink}")

        # # Get the symlink source and destination
        # list(GET symlink_parts 0 symlink_source)
        # list(GET symlink_parts 1 symlink_destination)

        # message("symlink_source: ${symlink_source}")
        # message("symlink_destination: ${symlink_destination}")

        # Create the full path for the symlink destination
        # set(symlink_destination_path "${symlink_destination}")

        # set(symlink_path "\"${parent_folder}/${symlink_name}\"")

        # Create the symlink using the create_symlink function
        message("CREATE_SYMLINK ${symlink_destination} ${symlink_name} in: ${writing_folder_absolute}")
        create_symlink("${symlink_destination}" "${symlink_name}" "${writing_folder_absolute}")

        # Make sure we're not asked to create sub-folders after a symlink..
        set(last_folder_created "")

      else()

        create_new_folder("${writing_folder_absolute}" "${folder_name}")
        set(last_folder_created "${folder_name}")

      endif()

    endif()
  endforeach()
endfunction()

##################################### UTILITY STUFF END ###########################################################


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

# Find dependencies thanks to conan
find_package(kit_sdk REQUIRED)
find_package(nv_usd REQUIRED)

# ${some_cmake_folder_name}
# +-- ${some_cmake_folder_name}
# |   +-- usr -> /usr/local/bin
# |   +-- usr2 -> ${tmp_fol}
# +-- include
# |   +-- usrTEMP -> ${tmp_fol}
# +-- lib
# |   +-- usr -> /usr/local/lib
# +-- src
#     +-- ${some_cmake_folder_name2}
#     |   +-- this is a great folder!
#     +-- other_folder


# Create a _build folders structure
create_folder_structure(${CMAKE_CURRENT_SOURCE_DIR}/_build
"
${OS_AND_ARCHITECTURE}
+-- ${BUILD_CONFIG}
|   +-- apps -> ${CMAKE_CURRENT_SOURCE_DIR}/apps
|   +-- exts
|   +-- kit -> ${kit_sdk_PACKAGE_FOLDER_RELEASE}
target-deps
+-- nv_usd -> ${nv_usd_PACKAGE_FOLDER_RELEASE}
")

# execute_process(COMMAND "${CMAKE_COMMAND}" -E create_symlink "/usr/local/bin" "usr" WORKING_DIRECTORY "/home/alex/conan_cmake_template/temp/my_cmake_folder_name 229/my_cmake_folder_name 229")






# Create the _build

# get a SYMLINK to kit-sdk!

# message(WARNING "Creating symlink in ${CMAKE_CURRENT_SOURCE_DIR}")
# message(WARNING "source_file ${kit-sdk}")

# works!
# create_symlink(${kit-sdk_PACKAGE_FOLDER_RELEASE} ${CMAKE_CURRENT_SOURCE_DIR}/kit)









# Add plugin (the release/exts/extensionname/bin/libextensionname.plugin.so)
# add_library(omni.app SHARED plugin/StartingMainCppFile.cpp)
# target_link_libraries(omni.app PRIVATE kit-sdk::kit-sdk)
