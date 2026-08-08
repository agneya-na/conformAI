#pragma once

#include "conformai/types.hpp"
#include "conformai/module.hpp"
#include "conformai/power_domain.hpp"

#include <memory>
#include <unordered_map>
#include <string>
#include <string_view>
#include <vector>
#include <optional>

namespace conformai {

/// Root container for the entire design + power intent database.
/// All entities are owned here via unique_ptr. External code holds IDs.
class DesignDatabase {
public:
    DesignDatabase() = default;
    ~DesignDatabase() = default;

    // Non-copyable, movable
    DesignDatabase(const DesignDatabase&) = delete;
    DesignDatabase& operator=(const DesignDatabase&) = delete;
    DesignDatabase(DesignDatabase&&) noexcept = default;
    DesignDatabase& operator=(DesignDatabase&&) noexcept = default;

    // ── Factory methods ──────────────────────────────────────
    [[nodiscard]] ModuleId createModule(std::string name);
    [[nodiscard]] NetId    createNet(ModuleId owner, std::string name,
                                     uint32_t width = 1, NetKind kind = NetKind::WIRE);
    [[nodiscard]] PinId    createPin(InstanceId owner, std::string name,
                                     PinDirection dir);
    [[nodiscard]] InstanceId createInstance(ModuleId parent, ModuleId ref,
                                           std::string name);
    [[nodiscard]] PowerDomainId createPowerDomain(std::string name);

    // ── Lookup ───────────────────────────────────────────────
    [[nodiscard]] Module*       getModule(ModuleId id) noexcept;
    [[nodiscard]] const Module* getModule(ModuleId id) const noexcept;
    [[nodiscard]] Module*       findModule(std::string_view name) noexcept;

    [[nodiscard]] Net*          getNet(NetId id) noexcept;
    [[nodiscard]] Pin*          getPin(PinId id) noexcept;
    [[nodiscard]] Instance*     getInstance(InstanceId id) noexcept;
    [[nodiscard]] PowerDomain*  getPowerDomain(PowerDomainId id) noexcept;

    // ── Queries ──────────────────────────────────────────────
    [[nodiscard]] std::size_t moduleCount() const noexcept;
    [[nodiscard]] std::size_t netCount() const noexcept;
    [[nodiscard]] std::size_t instanceCount() const noexcept;
    [[nodiscard]] bool empty() const noexcept;

    // ── Lifecycle ────────────────────────────────────────────
    void clear() noexcept;

private:
    uint64_t nextId_{1};
    [[nodiscard]] uint64_t genId() noexcept { return nextId_++; }

    std::unordered_map<ModuleId, std::unique_ptr<Module>>          modules_;
    std::unordered_map<std::string, ModuleId, std::hash<std::string_view>> moduleIndex_;
    std::unordered_map<NetId, std::unique_ptr<Net>>                nets_;
    std::unordered_map<PinId, std::unique_ptr<Pin>>                pins_;
    std::unordered_map<InstanceId, std::unique_ptr<Instance>>      instances_;
    std::unordered_map<PowerDomainId, std::unique_ptr<PowerDomain>> powerDomains_;
};

} // namespace conformai
