#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "apriltag::apriltag" for configuration "Debug"
set_property(TARGET apriltag::apriltag APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(apriltag::apriltag PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/apriltagd.lib"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/apriltagd.dll"
  )

list(APPEND _cmake_import_check_targets apriltag::apriltag )
list(APPEND _cmake_import_check_files_for_apriltag::apriltag "${_IMPORT_PREFIX}/lib/apriltagd.lib" "${_IMPORT_PREFIX}/bin/apriltagd.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
