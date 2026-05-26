---
name: acpi-platform-enablement
description: Use when enabling, debugging, reviewing, or documenting ACPI platform support across firmware and Linux, including DSDT/SSDT authoring, _CRS/_DSD/_STA device description, OS handoff, AML/ASL diagnostics, and spec/source-grounded firmware-to-kernel debugging.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [acpi, firmware, linux, uefi, edk2, platform-enablement, aml, asl]
    related_skills: [hardware-firmware-linux-stack, uefi-firmware, linux-kernel-driver-enablement]
---

# ACPI Platform Enablement

## Overview

Use this skill for ACPI-centered platform enablement: describing hardware to the OS, debugging firmware/kernel handoff, reviewing DSDT/SSDT changes, and mapping symptoms back to ACPI namespace objects, AML execution, resource descriptors, and Linux driver binding.

Treat ACPI as a contract between firmware and the OS. Separate ACPI spec requirements, platform firmware policy, edk2/vendor implementation details, Linux ACPI behavior, and board/silicon errata.

Do not copy spec text. Link official specs and cite section pointers such as “ACPI 6.x Device Configuration Objects `_CRS`” or “UEFI 2.x configuration table handoff”.

## When to Use

Use when the task involves:
- DSDT/SSDT design, review, extraction, decompilation, or patching
- ACPI namespace devices, methods, operation regions, fields, resources, power objects, dependencies
- `_HID`, `_CID`, `_UID`, `_STA`, `_CRS`, `_DSD`, `_DEP`, `_PR0`, `_PR3`, `_PS0`, `_PS3`, `_ADR`, `_OSC`, `_DSM`, `_PRW`
- Linux `ACPI BIOS Error`, `AE_NOT_FOUND`, `AE_AML_*`, IRQ/resource conflicts, GPIO lookup failures, or devices not binding
- Firmware handoff involving RSDP/XSDT/FADT/DSDT/SSDT, UEFI configuration tables, boot-loader/kernel table override

Do not use for pure UEFI app/protocol work with no ACPI/OS handoff impact, or DT-only enablement unless comparing ACPI vs DT.

## First Triage

Classify the failure:
1. Table discovery: expected RSDP/XSDT/FADT/DSDT/SSDT loaded? checksum/OEM/revision sane?
2. Namespace shape: device node exists? `_HID`/`_CID`/`_UID`/`_ADR` matches driver? `_STA` present/enabled/functioning?
3. Resource description: `_CRS` exposes expected MMIO, IRQ, DMA, GPIO, I2C, SPI, UART resources?
4. Properties and bindings: `_DSD` UUID, names, and types match Linux driver/fwnode expectations?
5. Power and dependencies: `_DEP`, power resources, GPIOs and wake methods correct?
6. AML execution: parse, lookup, method execution, field access, or region handler failure?

## Object Quick Reference

| Object | Meaning | Common Mistakes |
| --- | --- | --- |
| DSDT/SSDT | Base and secondary AML namespace | duplicate names, wrong override assumptions |
| `_HID`/`_CID` | Driver matching IDs | wrong PNP/vendor ID or missing fallback |
| `_UID`/`_ADR` | instance ID / bus address | unstable ID or wrong addressing model |
| `_STA` | presence/enabled/functioning | returns zero, dynamic status without notify |
| `_CRS` | current resources | wrong IRQ, MMIO, GPIO/I2C/SPI descriptors |
| `_DSD` | supplemental properties | using as resource replacement, malformed package |
| `_DEP` | operation dependency | missing provider ordering |
| `_PR0`/`_PR3`/`_PS0`/`_PS3` | power resources/methods | broad side effects, resume failures |
| `_OSC` | OS capability negotiation | denied capability not understood |

## Workflows

### Dump and decompile tables

```bash
sudo acpidump -o acpi.dat
acpixtract -a acpi.dat
iasl -d *.dat
iasl -e ssdt*.dat -d dsdt.dat
```

### Linux ACPI debug

```bash
dmesg -T | grep -Ei 'acpi|aml|dsdt|ssdt|gpio|irq|i2c|spi|uart|resource'
ls /sys/firmware/acpi/tables
ls /sys/firmware/acpi/tables/dynamic 2>/dev/null || true
find /sys/bus/acpi/devices -maxdepth 2 -type f \( -name hid -o -name modalias -o -name path -o -name status \) -print -exec cat {} \;
```

### Review `_CRS`

Verify resource type, MMIO base/size, IRQ polarity/trigger/share, GPIO controller/pin/polarity, I2C/SPI/UART descriptors, address width, producer/consumer role, and Linux driver resource consumption.

### Review `_DSD`

Verify UUID, package nesting, documented property names, expected types, references, and that hardware resources remain in `_CRS`.

### Review `_STA`

Remember common returns: `0x0F` = present/enabled/visible/functioning; `0x00` = absent. Check dynamic changes and notification.

## Firmware Handoff Model

```text
firmware source/config -> AML/table build -> firmware installs ACPI tables -> UEFI configuration table exposes RSDP -> boot loader preserves/passes tables -> kernel loads tables -> ACPICA parses namespace -> Linux ACPI core creates devices/fwnodes -> driver probes
```

Find divergence: source table generation, AML compile/decompile, table installation, kernel table load, namespace parse, method execution, driver match/probe, runtime PM.

## Common Pitfalls

1. Guessing from ASL names alone. Connect namespace path, AML object, Linux log, and driver code.
2. Fixing Linux symptoms in `_DSD` when `_CRS` is wrong.
3. Decompiling DSDT without external SSDTs.
4. Treating OS table override as product firmware.
5. Overclaiming ACPI spec behavior instead of separating spec vs Linux implementation.
6. Ignoring `_STA` when device never binds.
7. Copying Device Tree bindings blindly into `_DSD`.
8. Assuming correct ASL source means Linux loaded that table.

## Verification Checklist

- [ ] Original ACPI tables captured or firmware source located
- [ ] DSDT/SSDT decompiled with externals and `iasl` warnings reviewed
- [ ] Device path and `_HID`/`_CID`/`_UID`/`_ADR` verified
- [ ] `_STA`, `_CRS`, `_DSD`, dependencies and power resources checked
- [ ] Linux logs/sysfs evidence collected
- [ ] Firmware handoff path identified
- [ ] Result distinguishes spec, firmware policy, vendor code, and Linux behavior

## References

See `references/spec-map.md`, `references/linux-acpi-debugging.md`, `references/asl-review-checklists.md`, and `references/firmware-handoff.md`. Also consult https://github.com/MarsDoge/uefi-firmware-skill for broader UEFI firmware patterns.
