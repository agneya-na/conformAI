#include <cassert>
#include <memory>

#include "conformai/engine.hpp"
#include "conformai/mock_backends.hpp"

using namespace conformai;

static DesignIR build_design(bool include_domain_error) {
    DesignIR d;
    d.add_supply(SupplyNet{"VDD", 0.8});
    d.add_power_domain(PowerDomain{"PD_TOP", "VDD", {"u_top"}});

    d.add_logic_node(LogicNode{"n0", "INPUT", {}, "PD_TOP"});
    if (include_domain_error) {
        d.add_logic_node(LogicNode{"n1", "BUF", {"n0"}, "PD_MISSING"});
    } else {
        d.add_logic_node(LogicNode{"n1", "BUF", {"n0"}, "PD_TOP"});
    }
    d.add_observation_point(EquivalencePoint{"n1", "n1"});
    return d;
}

int main() {
    {
        auto golden = build_design(false);
        auto revised = build_design(false);

        VerificationEngine engine(std::make_unique<StructuralLecBackend>(),
                                  std::make_unique<BasicUpfBackend>());
        const auto report = engine.verify(AgentDirective{"tapeout-lowpower-check", {"equivalence", "upf"}},
                                          EquivalenceRequest{golden, revised});

        assert(report.lec.equivalent);
        assert(report.upf.pass);
        assert(report.orchestration_trace.size() == 3);
    }

    {
        auto golden = build_design(true);
        auto revised = build_design(false);

        VerificationEngine engine(std::make_unique<StructuralLecBackend>(),
                                  std::make_unique<BasicUpfBackend>());
        const auto report = engine.verify(AgentDirective{"detect-upf-violations", {"upf"}},
                                          EquivalenceRequest{golden, revised});

        assert(!report.upf.pass);
        assert(!report.upf.violations.empty());
    }

    return 0;
}
