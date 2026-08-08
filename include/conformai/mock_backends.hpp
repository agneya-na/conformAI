#pragma once

#include <algorithm>
#include <string>

#include "conformai/backends.hpp"

namespace conformai {

class StructuralLecBackend final : public EquivalenceBackend {
public:
    [[nodiscard]] std::string name() const override { return "structural-lec"; }

    EquivalenceResult run(const EquivalenceRequest& request) const override {
        EquivalenceResult result;
        const auto& g_nodes = request.golden.nodes();
        const auto& r_nodes = request.revised.nodes();
        result.equivalent = g_nodes.size() == r_nodes.size() &&
                            request.golden.observation_points().size() ==
                                request.revised.observation_points().size();
        if (!result.equivalent) {
            result.counterexamples.push_back("node or observation-point mismatch");
        }
        return result;
    }
};

class BasicUpfBackend final : public UpfBackend {
public:
    [[nodiscard]] std::string name() const override { return "basic-upf"; }

    UpfVerificationResult run(const DesignIR& design) const override {
        UpfVerificationResult result;
        const auto errors = design.validate();
        result.pass = errors.empty();
        std::transform(errors.begin(), errors.end(), std::back_inserter(result.violations), [](const auto& e) {
            return UpfViolation{e};
        });
        return result;
    }
};

}  // namespace conformai
