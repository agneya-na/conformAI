#pragma once

#include <vector>

#include "module.hpp"

namespace conformai {
class DesignDatabase {
  public:
    void add_module(const Module& module);
    const std::vector<Module>& modules() const;

  private:
    std::vector<Module> modules_;
};
}  // namespace conformai
