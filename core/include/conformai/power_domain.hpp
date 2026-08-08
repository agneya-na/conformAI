#pragma once

#include "conformai/types.hpp"
#include <string>
#include <vector>

namespace conformai {

struct IsolationStrategy {
    std::string name;
    PowerDomainId domain;
    std::string isolationSignal;
    IsolationSense sense{IsolationSense::HIGH};
    std::string clampValue{"0"};
    bool appliesToOutputs{true};
};

struct RetentionStrategy {
    std::string name;
    PowerDomainId domain;
    std::string saveSignal;
    std::string restoreSignal;
    RetentionType type{RetentionType::SAVE_RESTORE};
};

struct LevelShifterStrategy {
    std::string name;
    PowerDomainId domain;
    std::string appliesTo{"both"}; // "inputs", "outputs", "both"
};

struct PowerDomain {
    PowerDomainId id;
    std::string name;
    std::string primarySupply;   // e.g., "VDD"
    std::string groundSupply;    // e.g., "VSS"

    std::vector<InstanceId> elements;
    std::vector<IsolationStrategy> isolationStrategies;
    std::vector<RetentionStrategy> retentionStrategies;
    std::vector<LevelShifterStrategy> levelShifterStrategies;

    [[nodiscard]] bool hasIsolation() const noexcept {
        return !isolationStrategies.empty();
    }
    [[nodiscard]] bool hasRetention() const noexcept {
        return !retentionStrategies.empty();
    }
};

} // namespace conformai
