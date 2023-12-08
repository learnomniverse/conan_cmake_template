cmake_minimum_required(VERSION 3.15)
project(omni.app)

# DEBUG
message(STATUS "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")
# DEBUG


# Find kit-sdk
find_package(kit-sdk REQUIRED)




## ADESSO: scarica le dipendenze necessarie trovando gli URL da packman (tutto quello che c'è in
# kit-extension-py-cpp-deps in target-deps va scaricato e usato, kit-sdk va bene anche così come c'è adesso
# che tanto ci serve solo la var kit-sdk_PACKAGE_FOLDER_RELEASE per symlinkarlo)
# e poi crea la folder structure con la funzione qua sotto.
# Poi,  finalmente, scrivi il VERO cmake add_library per il release/exts/extensionname/bin/libextensionname.plugin.so e tenta di compilare un plugin carbon nativo. Suggerisco iniziare SENZA Pybind.
# Ancora meglio: 3 step e 3 estensioni: una py only, una native only e una pybind. La prima sarà solo da
# far funzionare i symlink. Fregatene di kit kernel sinceramente.. lo spiegherai dopo che gli utenti possono ridistribuire SENZA usare questa robaccia. Farei proprio un repo a parte magari con un submodule git dove metti tutti sti script conan e cmake.



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
  message(WARNING "input: ${ascii_lines}")

#   foreach(line IN LISTS ascii_lines)
#       message(WARNING "line: ${line}")
#   endforeach()

  # Keep track of the current indentation level and parent folder
  set(indent_level 0)
  set(parent_folder "${root_folder}")
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




    #   string(REGEX MATCH "^[^ \\+|\\-]+" useful_part "${line}")
    #   string(LENGTH "${useful_part}" useful_part_count)
    #   math(EXPR indent_count "${line_length} - ${useful_part_count}")
    #   string(SUBSTRING ${line} ${indent_count} -1 useful_part)



      string(LENGTH "${useful_part}" useful_part_count)
      math(EXPR indent_count "${line_length} - ${useful_part_count}")

      # Divide the indent count by four to get the indent level
      math(EXPR indent_count "${indent_count} / 4")

      # If the indent level is greater than the current level, push the parent folder to a stack
      message("indent_count is now ${indent_count} while our current indent_level is ${indent_level}")
      if(indent_count GREATER indent_level)
        message("APPENDING ${parent_folder} to parent stack ${parent_stack}")
        list(APPEND parent_stack "${parent_folder}")
      # If the indent level is less than the current level, pop the parent folder from the stack
      elseif(indent_count LESS indent_level)
        message("POPPIN from parent stack ${parent_stack}")
        math(EXPR pop_count "${indent_level} - ${indent_count}")
        foreach(i RANGE 1 ${pop_count})
          list(POP_BACK parent_stack parent_folder)
          list(GET parent_stack -1 parent_folder)
        endforeach()
      endif()

      message("new parent_folder: ${parent_folder}")
      message("new parent_stack: ${parent_stack}")

      # Set the current indent level to the indent count
      set(indent_level "${indent_count}")

      # Drop graphical useless characters
      # string(SUBSTRING ${line} ${indent_count} -1 no_ascii_art_content)


      message("indent_count: ${indent_count}, indent_level: ${indent_level}, parent_folder: ${parent_folder}, useful_part: '${useful_part}', useful_part_count: ${useful_part_count}")

      # Extract the folder name or the symlink source and destination from the line
    #   string(REGEX REPLACE "^ *\\|?\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- " "" folder_or_symlink "${line}")

      # Check if the line has the form of a symlink or just a folder name
      if(useful_part MATCHES "^(.+)\\s*->\\s*(.+)$")
        # message("Folder name: ${CMAKE_MATCH_1}")
        # message("Symlink destination: ${CMAKE_MATCH_2}")
        message("Detected as a symlink: ${useful_part}..")
        # # Split the line by the '->' symbol
        # string(REPLACE "->" ";" symlink_parts "${folder_or_symlink}")

        # # Get the symlink source and destination
        # list(GET symlink_parts 0 symlink_source)
        # list(GET symlink_parts 1 symlink_destination)

        # Trim the whitespace from the source and destination
        string(STRIP "${CMAKE_MATCH_1}" symlink_name)
        string(STRIP "${CMAKE_MATCH_2}" symlink_destination)
        # message("symlink_source: ${symlink_source}")
        # message("symlink_destination: ${symlink_destination}")

        # Create the full path for the symlink destination
        # set(symlink_destination_path "${symlink_destination}")

        # set(symlink_path "\"${parent_folder}/${symlink_name}\"")

        # Create the symlink using the create_symlink function
        message("CREATE_SYMLINK ${symlink_destination} ${symlink_name} ${symlink_path} in: ${parent_folder}")
        create_symlink("${symlink_destination}" "${symlink_name}" "${parent_folder}")
      else()
          message("Just a folder name: ${useful_part}...")
          # Trim the whitespace from the folder name
          string(STRIP "${useful_part}" folder_name)

          # Create the full path for the folder
          set(folder_path "${parent_folder}/${folder_name}")

          # Create the folder if it does not exist
          message("MAKE_DIRECTORY ${folder_path}")
          file(MAKE_DIRECTORY "${folder_path}")

          # Set the parent folder to the folder path
          set(parent_folder "${folder_path}")
      endif()

    endif()
  endforeach()
endfunction()



# create_symlink("/usr/local/bin" "usr")
# return()


set(some_cmake_folder_name "my_cmake_folder_name 229")
set(some_cmake_folder_name2 "e8qw8eqwe8qw9eqw.exe")
set(cmake_variable "lulzy thingz")
set(tmp_fol "/tmp")

# Create the desired ASCII art of new folders and symlinks in the directory root_folder
create_folder_structure(${CMAKE_CURRENT_SOURCE_DIR}/temp
"
${some_cmake_folder_name}
+-- ${some_cmake_folder_name}
|   +-- usr -> /usr/local/bin
|   +-- usr2 -> ${tmp_fol}
+-- include
|   +-- usrTEMP -> ${tmp_fol}
+-- lib
|   +-- usr -> /usr/local/lib
+-- src
    +-- ${some_cmake_folder_name2}
    |   +-- this is a great folder!
    +-- other_folder
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
