cmake_minimum_required(VERSION 3.16)
project(conformAI VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(conformai_core
    src/engine.cpp
    src/ir.cpp
)

target_include_directories(conformai_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

add_executable(conformai_tests
    tests/test_core.cpp
)

target_link_libraries(conformai_tests PRIVATE conformai_core)

include(CTest)
if(BUILD_TESTING)
    add_test(NAME conformai_core_tests COMMAND conformai_tests)
endif()
