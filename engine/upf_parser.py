"""ConformAI — IEEE 1801 UPF parser using embedded Tcl interpreter."""

from __future__ import annotations

import tkinter as tk
import logging
from dataclasses import dataclass, field

logger = logging.getLogger("conformai.upf")

__all__ = [
    "UPFPowerDomain", "UPFIsolation", "UPFRetention",
    "UPFLevelShifter", "UPFSupplyNet", "UPFIntent", "UPFParser",
]


@dataclass
class UPFPowerDomain:
    name: str
    elements: list[str] = field(default_factory=list)


@dataclass
class UPFSupplyNet:
    name: str
    domain: str = ""


@dataclass
class UPFIsolation:
    name: str
    domain: str = ""
    clamp_value: str = "0"
    applies_to: str = "outputs"
    isolation_signal: str = ""
    isolation_sense: str = "high"


@dataclass
class UPFRetention:
    name: str
    domain: str = ""
    save_signal: str = ""
    restore_signal: str = ""


@dataclass
class UPFLevelShifter:
    name: str
    domain: str = ""
    applies_to: str = "both"


@dataclass
class UPFIntent:
    domains: list[UPFPowerDomain] = field(default_factory=list)
    supply_nets: list[UPFSupplyNet] = field(default_factory=list)
    isolations: list[UPFIsolation] = field(default_factory=list)
    retentions: list[UPFRetention] = field(default_factory=list)
    level_shifters: list[UPFLevelShifter] = field(default_factory=list)


class UPFParser:
    """Parses UPF by registering Tcl commands that capture intent."""

    __slots__ = ("_intent", "_tcl")

    def __init__(self):
        self._intent = UPFIntent()
        self._tcl = tk.Tcl()
        self._register()

    def parse(self, path: str) -> UPFIntent:
        self._intent = UPFIntent()
        self._register()
        try:
            self._tcl.eval(f"source {{{path}}}")
        except Exception as e:
            logger.error("UPF parse error: %s", e)
            raise
        logger.info(
            "UPF parsed: %d domains, %d iso, %d ret, %d ls",
            len(self._intent.domains),
            len(self._intent.isolations),
            len(self._intent.retentions),
            len(self._intent.level_shifters),
        )
        return self._intent

    # ── Tcl command registration ─────────────────────────────

    def _register(self):
        t = self._tcl
        i = self._intent

        def _flag(args: tuple, flag: str) -> str:
            a = list(args)
            if flag in a:
                idx = a.index(flag)
                if idx + 1 < len(a):
                    return str(a[idx + 1])
            return ""

        def create_power_domain(name, *a):
            i.domains.append(UPFPowerDomain(
                name=name,
                elements=_flag(a, "-elements").split(),
            ))

        def create_supply_net(name, *a):
            i.supply_nets.append(UPFSupplyNet(name=name, domain=_flag(a, "-domain")))

        def set_isolation(name, *a):
            i.isolations.append(UPFIsolation(
                name=name,
                domain=_flag(a, "-domain"),
                clamp_value=_flag(a, "-clamp_value"),
                applies_to=_flag(a, "-applies_to") or "outputs",
                isolation_signal=_flag(a, "-isolation_signal"),
                isolation_sense=_flag(a, "-isolation_sense") or "high",
            ))

        def set_retention(name, *a):
            i.retentions.append(UPFRetention(
                name=name,
                domain=_flag(a, "-domain"),
                save_signal=_flag(a, "-save_signal"),
                restore_signal=_flag(a, "-restore_signal"),
            ))

        def set_level_shifter(name, *a):
            i.level_shifters.append(UPFLevelShifter(
                name=name,
                domain=_flag(a, "-domain"),
                applies_to=_flag(a, "-applies_to") or "both",
            ))

        t.createcommand("create_power_domain", create_power_domain)
        t.createcommand("create_supply_net", create_supply_net)
        t.createcommand("set_isolation", set_isolation)
        t.createcommand("set_retention", set_retention)
        t.createcommand("set_level_shifter", set_level_shifter)

        # Stub remaining UPF commands
        for cmd in [
            "create_supply_port", "create_supply_set", "create_power_switch",
            "add_port_state", "create_pst", "add_pst_state",
            "set_domain_supply_net", "set_isolation_control",
            "set_retention_control", "map_power_switch",
            "set_port_attributes", "set_design_attributes",
        ]:
            t.createcommand(cmd, lambda *a, **k: None)
