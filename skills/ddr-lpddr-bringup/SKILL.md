---
name: ddr-lpddr-bringup
description: Use when designing, validating, bringing up, or debugging DDR/LPDDR memory subsystems across schematic/layout, power sequencing, clocks, resets, SPD/straps, firmware memory training, BIOS/UEFI handoff, Linux stability, ECC, margining, and stress-test evidence.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [ddr, lpddr, memory, dram, firmware, bios, uefi, signal-integrity, board-bringup, linux, ecc]
    related_skills: [hardware-firmware-linux-stack, board-bringup-lab, power-thermal-validation, linux-kernel-driver-enablement]
---

# DDR/LPDDR Bring-Up

## Overview

Use this skill as a focused child of `hardware-firmware-linux-stack`. It handles one deep platform domain while preserving the same evidence-first rule: prove lower layers before changing upper layers, keep board/firmware/kernel versions attached to every claim, and route back to the cross-layer router when the issue crosses domain boundaries.

Do not copy proprietary standards or vendor confidential text. Link official landing pages, cite document/version/section/table where possible, and summarize engineering implications in original wording.

## When to Use

Use when the task involves:
- DDR4/DDR5/LPDDR4/LPDDR5 schematic/layout review
- DRAM initialization or memory training failure in firmware/BIOS/UEFI/SPL
- Intermittent boot, data corruption, ECC/MCE, memtest, stress-ng, or suspend/resume memory issues
- Memory topology, impedance, ODT, Vref, DQ/DQS/CA/CK routing, SPD, straps, PMIC, or power sequencing review

Do not use as the primary skill for:
- Storage or PCIe errors after memory stability is proven
- Pure application memory leak debugging

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
dmesg -T | grep -Ei 'edac|ecc|mce|machine check|memory|dram|ddr|ras|oom|segfault|page allocation'
free -h
sudo dmidecode -t memory 2>/dev/null || true
numactl -H 2>/dev/null || true
memtester 1024M 1
stress-ng --vm 2 --vm-bytes 75% --timeout 10m --verify
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
