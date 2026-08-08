#include "conformai/engine.hpp"

#include <stdexcept>

namespace conformai {

VerificationEngine::VerificationEngine(std::unique_ptr<EquivalenceBackend> lec_backend,
                                       std::unique_ptr<UpfBackend> upf_backend)
    : lec_backend_(std::move(lec_backend)), upf_backend_(std::move(upf_backend)) {
    if (!lec_backend_ || !upf_backend_) {
        throw std::invalid_argument("VerificationEngine requires both LEC and UPF backends");
    }
}

EngineReport VerificationEngine::verify(const AgentDirective& directive,
                                        const EquivalenceRequest& request) const {
    EngineReport report;
    report.orchestration_trace.push_back("goal=" + directive.goal);
    report.orchestration_trace.push_back("lec_backend=" + lec_backend_->name());
    report.orchestration_trace.push_back("upf_backend=" + upf_backend_->name());

    report.upf = upf_backend_->run(request.golden);
    report.lec = lec_backend_->run(request);
    return report;
}

}  // namespace conformai
