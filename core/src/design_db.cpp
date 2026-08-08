#include "conformai/design_db.hpp"

namespace conformai {
void DesignDatabase::add_module(const Module& module) { modules_.push_back(module); }

const std::vector<Module>& DesignDatabase::modules() const { return modules_; }
}  // namespace conformai
