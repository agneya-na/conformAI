#pragma once

#include "conformai/types.hpp"
#include <string>

namespace conformai {

struct Pin {
    PinId id;
    std::string name;
    PinDirection direction{PinDirection::UNKNOWN};
    uint32_t msb{0};
    uint32_t lsb{0};
    bool isSigned{false};

    NetId connectedNet;
    InstanceId ownerInstance;

    [[nodiscard]] uint32_t width() const noexcept {
        return msb >= lsb ? (msb - lsb + 1) : (lsb - msb + 1);
    }
};

} // namespace conformai
