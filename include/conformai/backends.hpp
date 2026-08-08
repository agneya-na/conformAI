#pragma once

#include <string>
#include <vector>

#include "conformai/ir.hpp"

namespace conformai {

struct EquivalenceRequest {
    DesignIR golden;
    DesignIR revised;
};

struct EquivalenceResult {
    bool equivalent = false;
    std::vector<std::string> counterexamples;
};

class EquivalenceBackend {
public:
    virtual ~EquivalenceBackend() = default;
    [[nodiscard]] virtual std::string name() const = 0;
    virtual EquivalenceResult run(const EquivalenceRequest& request) const = 0;
};

struct UpfViolation {
    std::string message;
};

struct UpfVerificationResult {
    bool pass = false;
    std::vector<UpfViolation> violations;
};

class UpfBackend {
public:
    virtual ~UpfBackend() = default;
    [[nodiscard]] virtual std::string name() const = 0;
    virtual UpfVerificationResult run(const DesignIR& design) const = 0;
};

}  // namespace conformai
