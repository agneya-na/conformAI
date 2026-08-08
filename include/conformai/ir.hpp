#pragma once

#include <optional>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace conformai {

struct SupplyNet {
    std::string name;
    double nominal_voltage = 0.0;
};

struct PowerDomain {
    std::string name;
    std::string primary_supply;
    std::unordered_set<std::string> instances;
};

struct LogicNode {
    std::string name;
    std::string op;
    std::vector<std::string> fanin;
    std::optional<std::string> power_domain;
};

struct EquivalencePoint {
    std::string golden_signal;
    std::string revised_signal;
};

class DesignIR {
public:
    bool add_supply(const SupplyNet& supply);
    bool add_power_domain(const PowerDomain& domain);
    bool add_logic_node(const LogicNode& node);
    bool add_observation_point(const EquivalencePoint& point);

    [[nodiscard]] bool has_supply(const std::string& name) const;
    [[nodiscard]] bool has_domain(const std::string& name) const;
    [[nodiscard]] bool has_node(const std::string& name) const;

    [[nodiscard]] const std::unordered_map<std::string, SupplyNet>& supplies() const;
    [[nodiscard]] const std::unordered_map<std::string, PowerDomain>& domains() const;
    [[nodiscard]] const std::unordered_map<std::string, LogicNode>& nodes() const;
    [[nodiscard]] const std::vector<EquivalencePoint>& observation_points() const;

    [[nodiscard]] std::vector<std::string> validate() const;

private:
    std::unordered_map<std::string, SupplyNet> supplies_;
    std::unordered_map<std::string, PowerDomain> domains_;
    std::unordered_map<std::string, LogicNode> nodes_;
    std::vector<EquivalencePoint> observation_points_;
};

}  // namespace conformai
