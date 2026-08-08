#include "conformai/design_db.hpp"
#include <stdexcept>

namespace conformai {

ModuleId DesignDatabase::createModule(std::string name) {
    if (moduleIndex_.count(name)) {
        throw std::runtime_error("Duplicate module: " + name);
    }
    ModuleId id{genId()};
    auto mod = std::make_unique<Module>();
    mod->id = id;
    mod->name = name;
    moduleIndex_[name] = id;
    modules_[id] = std::move(mod);
    return id;
}

NetId DesignDatabase::createNet(ModuleId owner, std::string name,
                                uint32_t width, NetKind kind) {
    NetId id{genId()};
    auto net = std::make_unique<Net>();
    net->id = id;
    net->name = name;
    net->width = width;
    net->kind = kind;
    nets_[id] = std::move(net);

    if (auto* mod = getModule(owner)) {
        mod->nets.push_back(id);
        mod->netIndex[name] = id;
    }
    return id;
}

PinId DesignDatabase::createPin(InstanceId owner, std::string name,
                                PinDirection dir) {
    PinId id{genId()};
    auto pin = std::make_unique<Pin>();
    pin->id = id;
    pin->name = name;
    pin->direction = dir;
    pin->ownerInstance = owner;
    pins_[id] = std::move(pin);

    if (auto* inst = getInstance(owner)) {
        inst->pins[name] = id;
    }
    return id;
}

InstanceId DesignDatabase::createInstance(ModuleId parent, ModuleId ref,
                                          std::string name) {
    InstanceId id{genId()};
    auto inst = std::make_unique<Instance>();
    inst->id = id;
    inst->name = name;
    inst->moduleRef = ref;
    inst->parentModule = parent;
    instances_[id] = std::move(inst);

    if (auto* mod = getModule(parent)) {
        mod->instances.push_back(id);
        mod->instanceIndex[name] = id;
        mod->children.push_back(id);
    }
    return id;
}

PowerDomainId DesignDatabase::createPowerDomain(std::string name) {
    PowerDomainId id{genId()};
    auto pd = std::make_unique<PowerDomain>();
    pd->id = id;
    pd->name = name;
    powerDomains_[id] = std::move(pd);
    return id;
}

Module* DesignDatabase::getModule(ModuleId id) noexcept {
    auto it = modules_.find(id);
    return it != modules_.end() ? it->second.get() : nullptr;
}

const Module* DesignDatabase::getModule(ModuleId id) const noexcept {
    auto it = modules_.find(id);
    return it != modules_.end() ? it->second.get() : nullptr;
}

Module* DesignDatabase::findModule(std::string_view name) noexcept {
    auto it = moduleIndex_.find(std::string(name));
    return it != moduleIndex_.end() ? getModule(it->second) : nullptr;
}

Net* DesignDatabase::getNet(NetId id) noexcept {
    auto it = nets_.find(id);
    return it != nets_.end() ? it->second.get() : nullptr;
}

Pin* DesignDatabase::getPin(PinId id) noexcept {
    auto it = pins_.find(id);
    return it != pins_.end() ? it->second.get() : nullptr;
}

Instance* DesignDatabase::getInstance(InstanceId id) noexcept {
    auto it = instances_.find(id);
    return it != instances_.end() ? it->second.get() : nullptr;
}

PowerDomain* DesignDatabase::getPowerDomain(PowerDomainId id) noexcept {
    auto it = powerDomains_.find(id);
    return it != powerDomains_.end() ? it->second.get() : nullptr;
}

std::size_t DesignDatabase::moduleCount() const noexcept { return modules_.size(); }
std::size_t DesignDatabase::netCount() const noexcept { return nets_.size(); }
std::size_t DesignDatabase::instanceCount() const noexcept { return instances_.size(); }
bool DesignDatabase::empty() const noexcept { return modules_.empty(); }

void DesignDatabase::clear() noexcept {
    modules_.clear();
    moduleIndex_.clear();
    nets_.clear();
    pins_.clear();
    instances_.clear();
    powerDomains_.clear();
    nextId_ = 1;
}

} // namespace conformai
