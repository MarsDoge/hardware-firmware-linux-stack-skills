---
name: bmc-ec-platform-control
description: Use when enabling, integrating, or debugging BMC/EC platform-control paths including board management, power sequencing, sensors, fans, GPIO/I2C/SMBus, IPMI/Redfish, host-BMC/EC handoff, firmware update, Linux/OpenBMC evidence, and cross-layer ownership boundaries.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [bmc, ec, openbmc, embedded-controller, ipmi, redfish, platform-control, sensors, fans, power, firmware, linux]
    related_skills: [hardware-firmware-linux-stack, power-thermal-validation, board-bringup-lab, linux-kernel-driver-enablement]
---

# BMC/EC Platform Control

## Overview

Use this skill as a focused child of `hardware-firmware-linux-stack`. It handles one deep platform domain while preserving the same evidence-first rule: prove lower layers before changing upper layers, keep board/firmware/kernel versions attached to every claim, and route back to the cross-layer router when the issue crosses domain boundaries.

Do not copy proprietary standards or vendor confidential text. Link official landing pages, cite document/version/section/table where possible, and summarize engineering implications in original wording.

## When to Use

Use when the task involves:
- BMC/EC controls power sequencing, reset, fans, LEDs, sensors, GPIO, or board policy
- Host-BMC/EC communication via IPMI, Redfish, KCS, BT, MCTP, SMBus/I2C, PECI, LPC/eSPI, UART, or mailbox
- OpenBMC service/device-tree/platform integration
- Firmware update, recovery, ownership, watchdog, or manufacturing-control workflow

Do not use as the primary skill for:
- Pure host Linux driver issue with no BMC/EC ownership
- Cloud management API work unrelated to platform control

## First Response Workflow

1. Identify platform, board revision/BOM, firmware stack, kernel version, component part numbers, target interface, and known-good comparison.
2. Classify the failing layer: hardware design, lab measurement, firmware policy/training/table handoff, Linux enumeration/driver, userspace service, or production validation.
3. Collect evidence before changing code: logs, schematics snippets, measurements, register dumps, sysfs/debugfs, firmware settings, and exact repro commands.
4. Make one reversible change per test. Record result, rollback, and confidence.
5. If another child skill owns the lower layer, switch to it before continuing.

## Evidence Commands

```bash
uname -a
dmesg -T | grep -Ei 'bmc|ipmi|kcs|bt|mctp|peci|lpc|espi|i2c|smbus|watchdog|hwmon|fan|thermal'
ipmitool mc info 2>/dev/null || true
ipmitool sensor list 2>/dev/null || true
curl -k https://<bmc>/redfish/v1/ 2>/dev/null || true
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
