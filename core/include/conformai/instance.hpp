#pragma once

#include "conformai/types.hpp"
#include <string>
#include <unordered_map>

namespace conformai {

struct Instance {
    InstanceId id;
    std::string name;
    ModuleId moduleRef;      // What module type is this?
    ModuleId parentModule;   // Where does it live?

    std::unordered_map<std::string, PinId> pins;

    // UPF annotations
    PowerDomainId powerDomain;
    bool isIsolationCell{false};
    bool isLevelShifter{false};
    bool isRetentionCell{false};
    bool isAlwaysOn{false};
    bool isPowerSwitch{false};

    [[nodiscard]] PinId findPin(std::string_view n) const {
        auto it = pins.find(std::string(n));
        return it != pins.end() ? it->second : PinId{};
    }
};

} // namespace conformai
