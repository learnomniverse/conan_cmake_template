#  Written by Marco Alesiani, NVIDIA Corp (nvidia.com - malesiani)
#
#  This code is licensed under the MIT License.

#######################################################################
# This module provides OS-aware filesystem manipulation utilities for use
# in Omniverse extensions development.


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


# Expands a list of folders (folder_stack = {'_build', 'linux-x86_64', 'release'}) into a single
# concatenated string, i.e. "_build/linux-x86_64/release" and writes it out in the output "writing_folder"
# variable in the parent scope. This function is a helper to create_folder_structure()
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




# Creates a folder structure made of new folders and symlinks (Windows or Unix) starting
# from a given root_folder base directory and proceeding creating stuff under it.
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
# Spaces are IMPORTANT! Use a padding of 4 characters (they can be all spaces or stuff like
# "+-- " or "----" or whatever you prefer as long as the padding of 4 chars is respected to
# indent each row).
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
