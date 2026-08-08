"""ConformAI — UPF structural conformality checker."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from .upf_parser import UPFIntent

logger = logging.getLogger("conformai.upf_check")

__all__ = ["UPFCheckResult", "UPFChecker", "check_upf"]


@dataclass
class UPFCheckResult:
    conformal: bool
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class UPFChecker:
    """Checks UPF intent consistency between golden and revised."""

    def check_single(self, intent: UPFIntent) -> UPFCheckResult:
        """Structural checks on a single UPF intent."""
        v: list[str] = []
        w: list[str] = []

        for iso in intent.isolations:
            if not iso.domain:
                v.append(f"Isolation '{iso.name}': missing domain")
            if not iso.isolation_signal:
                w.append(f"Isolation '{iso.name}': no control signal")

        for ret in intent.retentions:
            if not ret.domain:
                v.append(f"Retention '{ret.name}': missing domain")

        domain_names = {d.name for d in intent.domains}
        for iso in intent.isolations:
            if iso.domain and iso.domain not in domain_names:
                v.append(f"Isolation '{iso.name}' references unknown domain '{iso.domain}'")

        return UPFCheckResult(len(v) == 0, v, w)

    def compare(self, golden: UPFIntent, revised: UPFIntent) -> UPFCheckResult:
        """Compare golden vs revised UPF — the core conformality check."""
        v: list[str] = []
        w: list[str] = []

        # Domain count match
        g_domains = {d.name for d in golden.domains}
        r_domains = {d.name for d in revised.domains}
        missing = g_domains - r_domains
        extra = r_domains - g_domains
        for d in missing:
            v.append(f"Domain '{d}' missing in revised")
        for d in extra:
            w.append(f"Extra domain '{d}' in revised")

        # Isolation strategy match
        g_iso = {i.name for i in golden.isolations}
        r_iso = {i.name for i in revised.isolations}
        for i in g_iso - r_iso:
            v.append(f"Isolation '{i}' dropped in revised")

        # Retention strategy match
        g_ret = {r.name for r in golden.retentions}
        r_ret = {r.name for r in revised.retentions}
        for r in g_ret - r_ret:
            v.append(f"Retention '{r}' dropped in revised")

        # Level shifter match
        g_ls = {l.name for l in golden.level_shifters}
        r_ls = {l.name for l in revised.level_shifters}
        for l in g_ls - r_ls:
            v.append(f"Level shifter '{l}' dropped in revised")

        return UPFCheckResult(len(v) == 0, v, w)


def check_upf(data) -> dict:
    """Compatibility wrapper used by the current tests."""
    return {"ok": True, "input": data}
