set(CONFORMAI_CORE_SOURCES
    src/design_db.cpp
    src/module.cpp
    src/net.cpp
    src/pin.cpp
    src/instance.cpp
    src/power_domain.cpp
    src/upf_intent.cpp
)

if(CONFORMAI_BUILD_SHARED)
    add_library(conformai_core SHARED ${CONFORMAI_CORE_SOURCES})
else()
    add_library(conformai_core STATIC ${CONFORMAI_CORE_SOURCES})
endif()

target_include_directories(conformai_core PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

target_compile_features(conformai_core PUBLIC cxx_std_20)

# Install
install(TARGETS conformai_core
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)
install(DIRECTORY include/ DESTINATION include)
