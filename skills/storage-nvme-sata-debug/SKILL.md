---
name: storage-nvme-sata-debug
description: Use when enabling, validating, or debugging storage paths including NVMe over PCIe, SATA/AHCI, eMMC/UFS/SD boot media, firmware boot order, namespace/partition layout, Linux block devices, performance, power states, hotplug, and data-integrity evidence.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [storage, nvme, sata, ahci, emmc, ufs, sd, boot, linux, firmware, pcie, block-layer]
    related_skills: [hardware-firmware-linux-stack, pcie-debug-and-design, linux-kernel-driver-enablement, board-bringup-lab]
---

# Storage NVMe/SATA Debug

## Overview

Use this skill as a focused child of `hardware-firmware-linux-stack`. It handles one deep platform domain while preserving the same evidence-first rule: prove lower layers before changing upper layers, keep board/firmware/kernel versions attached to every claim, and route back to the cross-layer router when the issue crosses domain boundaries.

Do not copy proprietary standards or vendor confidential text. Link official landing pages, cite document/version/section/table where possible, and summarize engineering implications in original wording.

## When to Use

Use when the task involves:
- NVMe/SATA/eMMC/UFS/SD not detected or unstable
- Boot media, partition, firmware boot order, or rootfs failures
- NVMe PCIe link/resource/power state issues
- SATA PHY/AHCI link, hotplug, or performance issues
- Linux block-layer, filesystem, SMART, data-integrity evidence collection

Do not use as the primary skill for:
- Pure PCIe link debug before storage protocol is reached; use pcie-debug-and-design first
- Application database tuning after storage stack is proven

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
dmesg -T | grep -Ei 'nvme|sata|ahci|ata|mmc|sdhci|ufs|block|ext4|xfs|btrfs|i/o error|timeout|reset'
lsblk -o NAME,MODEL,SERIAL,SIZE,TYPE,FSTYPE,MOUNTPOINTS
blkid 2>/dev/null || true
nvme list 2>/dev/null || true
smartctl --scan 2>/dev/null || true
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
