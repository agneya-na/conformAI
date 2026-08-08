#pragma once

#include "conformai/types.hpp"
#include <string>
#include <vector>

namespace conformai {

struct Net {
    NetId id;
    std::string name;
    uint32_t width{1};
    NetKind kind{NetKind::WIRE};

    // Hypergraph connectivity
    PinId driver;
    std::vector<PinId> loads;

    // UPF annotations
    PowerDomainId powerDomain;
    bool isIsolationOutput{false};
    bool isLevelShifterNet{false};
    bool isRetentionNet{false};

    [[nodiscard]] bool isBus() const noexcept { return width > 1; }
    [[nodiscard]] bool hasDriver() const noexcept { return driver.valid(); }
    [[nodiscard]] std::size_t fanout() const noexcept { return loads.size(); }
};

} // namespace conformai
