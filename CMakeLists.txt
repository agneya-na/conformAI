cmake_minimum_required(VERSION 3.22)
project(conformAI VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Strict warnings — tapeout-grade quality
add_compile_options(-Wall -Wextra -Werror -Wpedantic -O2 -march=native)

# Options
option(CONFORMAI_BUILD_TESTS "Build unit tests" ON)
option(CONFORMAI_BUILD_SHARED "Build shared library" OFF)

# Core library
add_subdirectory(core)

# Tests
if(CONFORMAI_BUILD_TESTS)
    enable_testing()
    find_package(GTest QUIET)
    if(GTest_FOUND)
        add_subdirectory(tests/cpp)
    else()
        message(STATUS "GTest not found, skipping C++ tests")
    endif()
endif()
