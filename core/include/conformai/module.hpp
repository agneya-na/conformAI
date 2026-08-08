#pragma once

#include "conformai/types.hpp"
#include <string>
#include <vector>
#include <unordered_map>

namespace conformai {

struct Module {
    ModuleId id;
    std::string name;
    bool isTop{false};

    // Owned entities (IDs into DesignDatabase)
    std::vector<PinId>      ports;
    std::vector<NetId>      nets;
    std::vector<InstanceId> instances;

    // Name-based indices for O(1) lookup
    std::unordered_map<std::string, PinId>      portIndex;
    std::unordered_map<std::string, NetId>      netIndex;
    std::unordered_map<std::string, InstanceId> instanceIndex;

    // Hierarchy
    std::vector<InstanceId> children;

    // Power domain assignment (UPF)
    PowerDomainId powerDomain;

    [[nodiscard]] PinId findPort(std::string_view n) const {
        auto it = portIndex.find(std::string(n));
        return it != portIndex.end() ? it->second : PinId{};
    }
    [[nodiscard]] NetId findNet(std::string_view n) const {
        auto it = netIndex.find(std::string(n));
        return it != netIndex.end() ? it->second : NetId{};
    }
};

} // namespace conformai
