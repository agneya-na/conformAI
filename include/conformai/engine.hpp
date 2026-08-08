#pragma once

#include <memory>
#include <string>
#include <vector>

#include "conformai/backends.hpp"

namespace conformai {

struct AgentDirective {
    std::string goal;
    std::vector<std::string> priority_metrics;
};

struct EngineReport {
    EquivalenceResult lec;
    UpfVerificationResult upf;
    std::vector<std::string> orchestration_trace;
};

class VerificationEngine {
public:
    VerificationEngine(std::unique_ptr<EquivalenceBackend> lec_backend,
                       std::unique_ptr<UpfBackend> upf_backend);

    [[nodiscard]] EngineReport verify(const AgentDirective& directive,
                                      const EquivalenceRequest& request) const;

private:
    std::unique_ptr<EquivalenceBackend> lec_backend_;
    std::unique_ptr<UpfBackend> upf_backend_;
};

}  // namespace conformai
