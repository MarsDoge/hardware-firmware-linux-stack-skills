---
name: usb-typec-pd-debug
description: Use when designing, enabling, or debugging USB2/USB3/USB4, USB Type-C, USB Power Delivery, alt modes, orientation, role swap, xHCI/DWC controllers, PHYs, retimers, muxes, CC logic, firmware policy, and Linux USB/Type-C evidence.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [usb, type-c, power-delivery, pd, xhci, dwc, usb4, thunderbolt, firmware, linux, board-bringup]
    related_skills: [hardware-firmware-linux-stack, board-bringup-lab, linux-kernel-driver-enablement, power-thermal-validation]
---

# USB Type-C and PD Debug

## Overview

Use this skill as a focused child of `hardware-firmware-linux-stack`. It handles one deep platform domain while preserving the same evidence-first rule: prove lower layers before changing upper layers, keep board/firmware/kernel versions attached to every claim, and route back to the cross-layer router when the issue crosses domain boundaries.

Do not copy proprietary standards or vendor confidential text. Link official landing pages, cite document/version/section/table where possible, and summarize engineering implications in original wording.

## When to Use

Use when the task involves:
- USB device/host/OTG enumeration failures
- Type-C orientation, CC, VBUS, VCONN, role swap, or PD negotiation issues
- USB3/USB4 signal path with mux/retimer/redriver/PHY problems
- Linux xHCI/DWC/typec/tcpm/ucsi driver binding and runtime failures

Do not use as the primary skill for:
- Pure userspace USB app issues after kernel/device are proven
- Pure battery charging policy without USB-C/PD involvement

## First Response Workflow

1. Identify platform, board revision/BOM, firmware stack, kernel version, component part numbers, target interface, and known-good comparison.
2. Classify the failing layer: hardware design, lab measurement, firmware policy/training/table handoff, Linux enumeration/driver, userspace service, or production validation.
3. Collect evidence before changing code: logs, schematics snippets, measurements, register dumps, sysfs/debugfs, firmware settings, and exact repro commands.
4. Make one reversible change per test. Record result, rollback, and confidence.
5. If another child skill owns the lower layer, switch to it before continuing.

## Evidence Commands

```bash
uname -a
cat /proc/cmdline
dmesg -T | grep -Ei 'usb|xhci|dwc|typec|tcpm|ucsi|pd|role|altmode|thunderbolt|usb4|phy'
lsusb
lsusb -t
find /sys/class/typec -maxdepth 3 -type f -print -exec cat {} \; 2>/dev/null || true
```

## Common Pitfalls

See `references/pitfalls.md` for domain-specific pitfalls. General rules:

1. Do not debug Linux first when lower-layer electrical/firmware evidence is missing.
2. Do not treat a workaround as root-cause fix without explaining remaining risk.
3. Do not change multiple variables at once.
4. Do not lose board revision, firmware version, kernel commit, or component identity.
5. Do not quote proprietary spec text; cite and summarize.

## Verification Checklist

- [ ] Board revision/BOM/component identity recorded
- [ ] Firmware/BIOS/BMC/EC version recorded where relevant
- [ ] Kernel version/config and boot args captured where relevant
- [ ] Required physical measurements or explicit limitation captured
- [ ] Logs and command outputs archived
- [ ] Known-good comparison attempted or documented as unavailable
- [ ] Fix verified across cold boot and warm reboot where relevant
- [ ] Remaining risk and next measurement stated

## References

See `references/workflows.md`, `references/evidence-checklist.md`, and `references/pitfalls.md`. If present, also consult `references/spec-map.md` for official standards/source routing.
