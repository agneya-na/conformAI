#pragma once

#include <cstdint>
#include <string>
#include <string_view>
#include <functional>
#include <compare>

namespace conformai {

// ─────────────────────────────────────────────────────────────
// Strong ID types — prevents mixing up entity types at compile time
// ─────────────────────────────────────────────────────────────
template <typename Tag>
struct Id {
    uint64_t value{0};

    [[nodiscard]] constexpr bool valid() const noexcept { return value != 0; }
    [[nodiscard]] constexpr bool operator==(const Id&) const noexcept = default;
    [[nodiscard]] constexpr auto operator<=>(const Id&) const noexcept = default;
};

struct ModuleTag {};
struct NetTag {};
struct PinTag {};
struct InstanceTag {};
struct PowerDomainTag {};
struct SupplyNetTag {};

using ModuleId     = Id<ModuleTag>;
using NetId        = Id<NetTag>;
using PinId        = Id<PinTag>;
using InstanceId   = Id<InstanceTag>;
using PowerDomainId = Id<PowerDomainTag>;
using SupplyNetId  = Id<SupplyNetTag>;

// ─────────────────────────────────────────────────────────────
// Enumerations
// ─────────────────────────────────────────────────────────────
enum class PinDirection : uint8_t {
    INPUT, OUTPUT, INOUT, UNKNOWN
};

enum class NetKind : uint8_t {
    WIRE, LOGIC, REG, SUPPLY, UNKNOWN
};

enum class IsolationSense : uint8_t {
    HIGH, LOW
};

enum class RetentionType : uint8_t {
    SAVE_RESTORE, SAVE_ONLY
};

enum class CompareResult : uint8_t {
    EQUIVALENT,
    NON_EQUIVALENT,
    ABORT,
    NOT_COMPARED
};

enum class Verdict : uint8_t {
    ACCEPT, REJECT
};

} // namespace conformai

// Hash support for strong IDs
template <typename Tag>
struct std::hash<conformai::Id<Tag>> {
    std::size_t operator()(const conformai::Id<Tag>& id) const noexcept {
        return std::hash<uint64_t>{}(id.value);
    }
};
