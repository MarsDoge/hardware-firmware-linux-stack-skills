---
name: pcie-debug-and-design
description: Use when designing, reviewing, bringing up, or debugging PCIe links, endpoints, root ports, retimers, NVMe devices, hot-plug, AER, ASPM, firmware resource allocation, or Linux PCI enumeration across hardware, firmware, BIOS/UEFI, ACPI/device tree, and kernel layers.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pcie, pci-express, hardware, firmware, bios, uefi, linux, kernel, board-bringup, signal-integrity, aer, aspm]
    related_skills: [hardware-firmware-linux-stack, acpi-platform-enablement, board-bringup-lab, linux-kernel-driver-enablement]
---

# PCIe Debug and Design

## Overview

Use this skill for PCI Express design, bring-up, and debug across schematic/layout, reference clock, reset, power sequencing, lane routing, retimers/redrivers, firmware resource allocation, ACPI/device tree, Linux PCI core, endpoint drivers, AER, ASPM, hot-plug, and performance validation.

Core rule: PCIe failures are usually cross-layer. Do not treat `lspci` absence as “Linux problem” until power, refclk, PERST#, endpoint straps, LTSSM/link state, and firmware resource windows are proven.

This skill summarizes engineering implications only. Do not copy PCI-SIG specification text. Use official PCI-SIG landing pages and cite spec name/version/section where available.

## When to Use

Use when the task involves:
- PCIe root port, endpoint, switch, bridge, retimer, redriver, or add-in card design
- Link does not train, trains at wrong speed/width, or drops under load
- Device missing from `lspci`, intermittent enumeration, or boot-time resource failure
- NVMe, Wi-Fi, Ethernet, GPU, FPGA, accelerator, or custom endpoint over PCIe
- PERST#, REFCLK, CLKREQ#, WAKE#, hot-plug, PRSNT#, sideband signal debug
- AER, DPC, completion timeout, malformed TLP, ACS/ARI/ATS/PASID/SR-IOV
- ASPM/L1 Substates, runtime PM, suspend/resume, wake failures
- BIOS/UEFI PCI resource allocation, ACPI `_CRS`, MCFG, `_OSC`, `_PRT`

Do not use as the primary skill for:
- Pure NVMe protocol issues after PCIe link/enumeration are stable
- Pure SI simulation without firmware/Linux bring-up context
- Generic Linux driver debugging where PCIe transport is already proven

## Layer Model

| Layer | Evidence | Common Failure Modes |
| --- | --- | --- |
| Requirements | speed/width, topology, endpoint datasheet | unsupported generation, lane count mismatch |
| Schematic | power tree, refclk, PERST#, CLKREQ#, WAKE# | wrong reset polarity, refclk mismatch, missing pull |
| Layout/SI | impedance, insertion loss, lane polarity, retimer placement | poor margin, bad return path, skew, connector loss |
| Board bring-up | rails, scope, LA, LTSSM register | rail late, PERST# early, no refclk, endpoint held reset |
| Firmware/BIOS/UEFI | setup, ACPI/MCFG, resource windows | port disabled, resource exhaustion, bad ECAM, `_OSC` mismatch |
| Linux PCI core | `dmesg`, `lspci`, sysfs, AER logs | no bus scan, config read failure, BAR assignment fail |
| Endpoint driver | driver bind, MSI/MSI-X, DMA/IOMMU | ID mismatch, DMA mask, interrupt failure |
| Power management | ASPM, L1SS, PME, runtime PM | link drops, wake failure, latency mismatch |

## First Response Workflow

1. Identify topology: root complex, root port, lane map, endpoint/switch/retimer, target Gen/width, board rev, connector/riser.
2. Collect evidence: full `dmesg`, `lspci -nnvvxxxx`, firmware version/settings, ACPI dump or running DT, schematic snippets, scope captures, known-good comparison.
3. Classify symptom: no link, wrong width/speed, link but no device, device visible but driver fails, or works then drops.
4. Verify lower layers before changing upper layers.
5. Make one reversible change per test and record board/firmware/kernel/BIOS state.

## Evidence Commands

```bash
uname -a
cat /proc/cmdline
dmesg -T | tee dmesg.txt
lspci -nn
lspci -tv
lspci -nnvv | tee lspci-nnvv.txt
lspci -xxxx | tee lspci-xxxx.txt
dmesg -T | grep -Ei 'pci|pcie|aer|dpc|aspm|mcfg|ecam|msi|iommu|bar|resource|link'
```

If endpoint is visible:

```bash
DEV=<bus:dev.fn>
sudo lspci -s "$DEV" -nnvvxxxx
cat /sys/bus/pci/devices/0000:$DEV/current_link_speed 2>/dev/null
cat /sys/bus/pci/devices/0000:$DEV/current_link_width 2>/dev/null
cat /sys/bus/pci/devices/0000:$DEV/max_link_speed 2>/dev/null
cat /sys/bus/pci/devices/0000:$DEV/max_link_width 2>/dev/null
```

ACPI:
```bash
sudo acpidump -o acpi.dat
iasl -d acpi.dat
grep -R "MCFG\|_OSC\|_CRS\|_PRT\|_HPX" -n *.dsl
dmesg -T | grep -Ei 'acpi|mcfg|ecam|osc|pci'
```

Device tree:
```bash
dtc -I fs -O dts /sys/firmware/devicetree/base > running.dts
grep -ni "pcie\|pci" running.dts
dmesg -T | grep -Ei 'of:|dt|pcie|pci'
```

## One-Shot Recipes

### Device missing from lspci

Check root port logs, then hardware: endpoint rails, REFCLK, PERST# timing, straps, root port enablement, lane map, retimer/redriver, cable/riser.

### Wrong speed or width

Check sysfs link speed/width, `lspci -vv`, BIOS generation limits, bifurcation, endpoint straps, retimer mode, SI/equalization, cable/riser rating.

### AER or DPC errors

Classify corrected vs uncorrected/fatal, requester/completer, completion timeout, surprise down, bad TLP/DLLP. Use AER as a symptom map, not the root cause.

### BAR/resource assignment failure

Check above-4G decoding, 64-bit BARs, bridge windows, ACPI `_CRS`, MCFG/ECAM, and use `pci=realloc` only as a diagnostic.

## Common Pitfalls

1. Debugging Linux first when the link never trained. Prove rails, REFCLK, PERST#, straps, LTSSM/link state first.
2. Assuming `lspci` absence means endpoint failure. Check root port enablement, bus scan, ACPI/DT, and bridge windows.
3. Treating REFCLK as yes/no. Check architecture, source, timing, spread-spectrum, CLKREQ#.
4. Masking SI problems by forcing Gen1. Use Gen1 only as diagnostic.
5. Disabling ASPM permanently without root cause. Investigate CLKREQ#, L1SS, PME, endpoint errata.
6. Forgetting ACPI/MCFG/resource handoff. Dump running tables and compare firmware source/config.
7. Changing multiple variables at once. One test, one change, one evidence record.

## Verification Checklist

- [ ] Board revision, endpoint, root complex, firmware and kernel version recorded
- [ ] Expected and actual Gen/width captured
- [ ] Full boot `dmesg`, `lspci -nnvv`, topology captured
- [ ] Power rails, REFCLK, PERST#, CLKREQ#/WAKE#/PRSNT# checked as applicable
- [ ] Firmware/BIOS PCIe settings recorded
- [ ] ACPI/DT PCIe description captured from running system
- [ ] AER/DPC and ASPM/L1SS checked when relevant
- [ ] Cold boot, warm reboot, suspend/resume tested when applicable
- [ ] Known-good comparison performed where possible

## References

See `references/spec-map.md`, `references/workflows.md`, `references/evidence-checklist.md`, and `references/pitfalls.md`.
