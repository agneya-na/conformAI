#include "conformai/ir.hpp"

namespace conformai {

bool DesignIR::add_supply(const SupplyNet& supply) {
    return supplies_.emplace(supply.name, supply).second;
}

bool DesignIR::add_power_domain(const PowerDomain& domain) {
    return domains_.emplace(domain.name, domain).second;
}

bool DesignIR::add_logic_node(const LogicNode& node) {
    return nodes_.emplace(node.name, node).second;
}

bool DesignIR::add_observation_point(const EquivalencePoint& point) {
    observation_points_.push_back(point);
    return true;
}

bool DesignIR::has_supply(const std::string& name) const {
    return supplies_.find(name) != supplies_.end();
}

bool DesignIR::has_domain(const std::string& name) const {
    return domains_.find(name) != domains_.end();
}

bool DesignIR::has_node(const std::string& name) const {
    return nodes_.find(name) != nodes_.end();
}

const std::unordered_map<std::string, SupplyNet>& DesignIR::supplies() const {
    return supplies_;
}

const std::unordered_map<std::string, PowerDomain>& DesignIR::domains() const {
    return domains_;
}

const std::unordered_map<std::string, LogicNode>& DesignIR::nodes() const {
    return nodes_;
}

const std::vector<EquivalencePoint>& DesignIR::observation_points() const {
    return observation_points_;
}

std::vector<std::string> DesignIR::validate() const {
    std::vector<std::string> errors;
    for (const auto& [domain_name, domain] : domains_) {
        if (!has_supply(domain.primary_supply)) {
            errors.push_back("domain '" + domain_name + "' references missing supply '" + domain.primary_supply + "'");
        }
    }

    for (const auto& [node_name, node] : nodes_) {
        if (node.power_domain.has_value() && !has_domain(*node.power_domain)) {
            errors.push_back("node '" + node_name + "' references missing domain '" + *node.power_domain + "'");
        }
        for (const auto& fanin : node.fanin) {
            if (!has_node(fanin)) {
                errors.push_back("node '" + node_name + "' references missing fanin node '" + fanin + "'");
            }
        }
    }
    return errors;
}

}  // namespace conformai
