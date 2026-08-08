# conformAI

`conformAI` is an architecture-first, C++20 core engine for low-power equivalence checking (LEC) and UPF verification.

## Design goals

- Core verification logic is represented in a native Intermediate Representation (`DesignIR`) and not tied to any single backend format.
- Yosys/SAT tools are treated as backend plug-ins behind stable C++ interfaces (`EquivalenceBackend`, `UpfBackend`).
- An orchestration layer (`VerificationEngine`) captures agentic directives and coordinates backend execution.

## Repository layout

- `/include/conformai/ir.hpp`: tape-out oriented IR for supplies, power domains, logic graph, and observation points.
- `/include/conformai/backends.hpp`: backend contracts for LEC and UPF checks.
- `/include/conformai/engine.hpp`: agent-driven orchestration interface.
- `/include/conformai/mock_backends.hpp`: reference backend implementations for local testing.
- `/tests/test_core.cpp`: focused tests for IR validation and backend-agnostic orchestration.

## Build and test

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```
