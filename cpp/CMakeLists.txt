cmake_minimum_required(VERSION 3.20)
project(sandbox LANGUAGES CXX)
 
# --- Compiler settings ---
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)   # compile_commands.json, for clangd/editor tooling
 
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()
 
# --- One executable per .cpp file in app/ ---
# Add a new file to app/, reconfigure, and it becomes its own binary
# named after the file (e.g. app/foo.cpp -> executable "foo").
file(GLOB APP_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/*.cpp")
 
foreach(src ${APP_SOURCES})
  get_filename_component(name ${src} NAME_WE)
  add_executable(${name} ${src})
endforeach()
 
