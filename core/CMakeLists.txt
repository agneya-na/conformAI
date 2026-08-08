add_library(conformai_core
    src/design_db.cpp
    src/module.cpp
    src/net.cpp
    src/pin.cpp
    src/instance.cpp
    src/power_domain.cpp
    src/upf_intent.cpp
)

target_include_directories(conformai_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
