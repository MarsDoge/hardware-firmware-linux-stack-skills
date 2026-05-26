---
name: hardware-firmware-linux-stack
description: Use when designing, debugging, or integrating cross-layer hardware/software systems spanning schematics, PCB constraints, board bring-up, firmware/BIOS/UEFI, bootloaders, Linux kernel drivers, device tree/ACPI, and userspace validation. Provides an evidence-first workflow from requirements through lab verification, with command recipes, pitfalls, and checklists for hardware-firmware-Linux co-debugging.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hardware, firmware, bios, uefi, linux, kernel, board-bringup, device-tree, acpi, embedded, debugging]
    related_skills: [uefi-firmware, systematic-debugging, test-driven-development, codebase-inspection, linux-desktop-apps]
---

# Hardware-Firmware-Linux Stack Engineering

## Overview

Use this skill for end-to-end soft/hardware work where the failure may cross boundaries: hardware design, PCB/layout constraints, board power-up, boot ROM/SPL/BIOS/UEFI, bootloader, ACPI/device tree, Linux kernel, drivers, userspace services, and manufacturing tests.

Core principle: never debug a layer in isolation until you have proven the layer below it is stable enough. Power, clocks, reset, straps, pinmux, buses, firmware tables, kernel binding, and userspace permissions all form one chain.

Prefer evidence-first engineering:
- Start from requirements and interfaces.
- Capture reproducible symptoms.
- Split the system into layers.
- Verify each layer with concrete measurements, logs, register reads, and tests.
- Keep a traceable artifact trail: schematic notes, register dumps, boot logs, kernel config, firmware revision, board revision, probe screenshots, and test commands.

## When to Use

Use when the task involves any of:

- Hardware architecture, schematic review, PCB constraints, connector/interface definition
- Board bring-up: power rails, clocks, reset sequencing, straps, boot mode, serial console
- Firmware/BIOS/UEFI/bootloader development or debug
- ACPI, SMBIOS, device tree, U-Boot, coreboot, EDK II, TF-A, OP-TEE, SPL, BMC, EC
- Linux kernel enablement: defconfig, drivers, pinctrl, regulator, clk, reset, GPIO, I2C/SPI/UART/PCIe/USB/Ethernet
- Userspace integration: udev, systemd, firmware blobs, permissions, diagnostics, HAL services
- Cross-layer failures: device not enumerating, boot hang, intermittent bus errors, suspend/resume failures, thermal/power problems
- Lab validation, manufacturing tests, board revision handoff, or regression matrices

Do not use as the primary skill for:
- Pure application logic with no hardware/kernel/firmware dependency
- Generic web/backend debugging
- Pure UEFI architecture questions where `uefi-firmware` alone is sufficient
- Pure Linux desktop packaging issues where `linux-desktop-apps` alone is sufficient

## Reference Map and Skill Links

Use this skill as the cross-layer orchestrator. When a task narrows into a formal specification or a specialized domain, load or consult the narrower reference instead of duplicating all details here.

### Related Skills and Repositories

- Local Hermes skill: `uefi-firmware` — use for UEFI architecture, EDK II, firmware package structure, PEI/DXE/BDS, protocols, HOBs, NVRAM, and firmware-specific review.
- External reference repo: https://github.com/MarsDoge/uefi-firmware-skill — MarsDoge's UEFI firmware skill repository; consult for UEFI/ACPI-oriented references and keep this skill focused on cross-layer hardware/firmware/Linux handoff and lab debugging.
- This skill should link outward to domain skills rather than becoming a giant monolith. As new skills are created for PCIe, USB, DDR, storage, BMC, EC, power, thermal, board design, or Linux kernel subsystems, add them here as focused references.
- Skill-building method reference: `references/skill-development-method.md` — optional Nuwa-inspired technical distillation method adapted from https://github.com/alchaincyf/nuwa-skill. Use it only when it improves class-level hardware/firmware/Linux skills; skip it if it adds overhead or persona-like baggage.

### Standards and Specification Landing Pages

Prefer official specification landing pages or vendor datasheets. Do not paste copyrighted spec text into the skill; record section numbers, table names, and interpretation notes instead.

| Domain | Reference Source | Use For |
| --- | --- | --- |
| PCIe Base / CEM / ECN | PCI-SIG official specifications: https://pcisig.com/specifications | PCIe 3.0/4.0/5.0/6.0/7.0 link training, LTSSM, equalization, config space, AER, ASPM, CEM timing, PERST#, CLKREQ#, lane polarity/reversal |
| ACPI | UEFI Forum ACPI specs: https://uefi.org/specifications | DSDT/SSDT, `_CRS`, `_DSD`, `_STA`, power resources, GPIO/I2C/SPI descriptors, sleep states |
| UEFI | UEFI Forum UEFI specs: https://uefi.org/specifications | Boot services, runtime services, device path, variables, Secure Boot, EFI memory map, OS handoff |
| SMBIOS | DMTF SMBIOS specs: https://www.dmtf.org/standards/smbios | DMI/SMBIOS tables, board/system inventory, firmware-reported product data |
| USB | USB-IF documents: https://www.usb.org/documents | USB2/USB3/USB4, Type-C, PD, xHCI behavior, descriptors, compliance vocabulary |
| NVMe | NVM Express specifications: https://nvmexpress.org/specifications/ | NVMe controller behavior, namespaces, admin commands, firmware activation, PCIe storage debug |
| SATA | SATA-IO specifications: https://sata-io.org/developers/sata-specifications | SATA link, power states, PHY and connector requirements |
| Ethernet | IEEE 802.3 / vendor PHY datasheets | MAC/PHY interface, RGMII/SGMII/MDIO, link training, strap pins, delays |
| DDR/LPDDR | JEDEC standards plus memory vendor datasheets | DRAM topology, training, timing, power sequencing, SI/PI constraints |
| Linux DT Bindings | Linux kernel `Documentation/devicetree/bindings/` | Device tree schema, `compatible`, supplies, clocks, resets, pinctrl, interrupts |
| Linux Kernel APIs | Linux kernel docs: https://docs.kernel.org/ | Driver model, runtime PM, firmware loading, GPIO, regulator, clk, reset, pinctrl subsystems |

### Reference Handling Rules

- For PCIe generation-specific work, explicitly name the target generation: PCIe 3.0, 4.0, 5.0, 6.0, etc. Electrical margin, equalization, retimers/redrivers, and CEM timing differ by generation.
- For ACPI/UEFI work, load `uefi-firmware` and consult https://github.com/MarsDoge/uefi-firmware-skill when available; keep this skill focused on evidence collection and layer boundaries.
- For Linux enablement, prefer upstream kernel docs and bindings from the exact kernel tree under test, not random web snippets.
- For hardware interfaces, pair the protocol spec with the exact component datasheet, reference schematic, layout guide, and board revision.
- Capture citations as: spec name/version, section/table, URL or file path, and the engineering decision it supports.

## Layer Model

Always classify the issue by layer before changing code:

| Layer | Typical Evidence | Common Failure Modes |
| --- | --- | --- |
| Requirements | Datasheets, interface matrix, power budget, timing budget | Missing constraints, wrong voltage domain, invalid boot assumptions |
| Hardware design | Schematic, layout, BOM, DRC/ERC, SI/PI reports | Wrong pull-up, swapped pins, missing termination, rail sequencing |
| Board bring-up | DMM/scope/LA/JTAG/UART logs | Dead rail, bad clock, reset held, wrong strap, brownout |
| ROM/SPL/firmware | Serial logs, JTAG trace, firmware map | DRAM init fail, wrong boot source, corrupt image, bad handoff |
| BIOS/UEFI/bootloader | UEFI shell, dmesg handoff, ACPI/DT dump | Bad ACPI/DT, Secure Boot, PCI resource, variable store |
| Linux kernel | dmesg, config, driver probe logs, tracepoints | Missing driver, bad binding, pinctrl/regulator/clock mismatch |
| Userspace | systemd logs, udev, permissions, service config | Missing firmware, wrong device node, policy/permission issue |
| Production | test logs, manufacturing fixtures, telemetry | Flaky tolerances, untracked board rev, incomplete test coverage |

## First Response Workflow

For any cross-layer request:

1. Identify the target platform:
   - SoC/CPU/chipset
   - Board name and revision
   - Firmware stack
   - Kernel version
   - Boot path
   - Interface/device under test
   - Available lab tools

2. Ask for or inspect hard evidence:
   - Schematic/layout snippets when hardware is involved
   - Datasheet sections for the interface
   - Full boot log, not just the last error
   - Kernel `.config`, device tree, ACPI dump, firmware version
   - Exact command that fails
   - Known-good board or previous revision comparison

3. Build a layer hypothesis:
   - “This is likely below Linux because the rail/clock/reset is not proven.”
   - “This is likely firmware table/pinmux because hardware enumerates but driver probe lacks resources.”
   - “This is likely userspace because the kernel device node exists and the driver is bound.”

4. Verify lower layers before fixing upper layers.

5. Make the smallest reversible change and record it.

## Cross-Layer Debugging Rules

Follow these rules strictly:

- Do not patch a Linux driver until power, reset, clock, strap, and bus visibility are verified.
- Do not blame hardware until firmware tables/pinmux/regulators/clocks have been inspected.
- Do not trust “it boots” as proof. Capture the full boot log and check warnings.
- Do not trust a single successful boot. Test cold boot, warm reset, power cycle, and suspend/resume when relevant.
- Do not assume board revisions are equivalent. Record PCB revision, BOM variant, rework wires, and firmware build.
- Do not conflate standard behavior with vendor policy. Mark which facts come from datasheet/spec, firmware implementation, board design, or Linux behavior.
- Prefer comparing known-good vs bad:
  - board A vs board B
  - old firmware vs new firmware
  - old kernel vs new kernel
  - old PCB revision vs new PCB revision

## Hardware Design Review Workflow

Use this when asked to review or design hardware interfaces.

### 1. Requirements and Interfaces

Create or request an interface matrix:

| Interface | Voltage | Direction | Pulls | Boot Strap? | Driver/Firmware Owner | Test Method |
| --- | --- | --- | --- | --- | --- | --- |
| UART0 TX/RX | 1.8V | SoC ↔ debug header | pull-up? | maybe | boot ROM/Linux | serial console |
| I2C1 | 1.8V/3.3V | SoC ↔ PMIC/sensor | required | no | firmware/kernel | i2cdetect/register read |
| SPI NOR | 1.8V/3.3V | SoC ↔ flash | per datasheet | yes | ROM/SPL/Linux MTD | JEDEC ID/readback |
| PCIe | high speed | SoC ↔ endpoint | reset/clkreq | no | firmware/kernel | lspci/AER logs |

Check:
- Voltage domain compatibility
- Absolute maximum ratings
- Pull-up/pull-down values and boot strap effects
- Reset polarity and sequencing
- Clock source, frequency, ppm, enable timing
- Power rail current, margin, transient load
- Signal integrity constraints for high-speed links
- Firmware/Linux ownership of each resource

### 2. Schematic Checks

For every peripheral:
- Power pins connected to correct rail
- Decoupling follows datasheet placement and value guidance
- Reset and enable pins have deterministic states
- Interrupt pins have correct polarity and pull
- Address select pins are set and documented
- Boot mode straps match desired boot order
- Debug access exists: UART, JTAG/SWD, test points, recovery pins
- Programming path exists for flash/EEPROM/MCU/EC/BMC

### 3. PCB/Layout Checks

For layout-sensitive designs:
- Differential pair impedance and length matching
- Return paths and reference plane continuity
- Crystal/oscillator placement and guard rules
- Power rail width/current capacity
- Thermal vias and heat spreading
- Analog/digital separation where required
- Antenna/RF keepouts
- Test points accessible in fixture
- Rework feasibility for early prototypes

### 4. Hardware Review Output

Produce:
- Critical blockers
- Risk items
- Firmware/Linux dependencies
- Required measurements during bring-up
- Manufacturing test hooks
- Open questions tied to datasheet sections

## Board Bring-Up Workflow

Never start with the kernel. Bring up the board in this order.

### 1. Pre-Power Checks

With power off:
- Visual inspection under microscope
- Confirm PCB revision and BOM variant
- Check shorts on major rails
- Check diode mode or resistance to ground
- Confirm jumpers/straps/boot mode
- Confirm current limit on bench supply

Useful commands for artifact capture:
```bash
mkdir -p bringup/$(date +%Y%m%d)-board-revA
date -Is | tee bringup/session.txt
uname -a | tee -a bringup/session.txt
```

### 2. First Power

Use a current-limited supply. Measure:
- Input current
- All always-on rails
- PMIC enable chain
- Reset lines
- Oscillators/clocks
- Boot strap pins at reset sampling time

Record:
```text
Board:
Revision:
BOM variant:
Power source:
Current limit:
Observed input current:
Rails:
Clocks:
Reset state:
Boot mode:
Serial output:
```

### 3. Serial Console

Find the earliest console:
- Boot ROM UART
- SPL/U-Boot UART
- UEFI serial
- Linux earlycon
- BMC/EC console

Common serial commands:
```bash
# Replace device and baud rate as appropriate.
sudo picocom -b 115200 /dev/ttyUSB0
sudo minicom -D /dev/ttyUSB0 -b 115200
stty -F /dev/ttyUSB0 115200 raw -echo
```

Capture logs:
```bash
mkdir -p logs
script -f logs/serial-$(date +%Y%m%d-%H%M%S).log
sudo picocom -b 115200 /dev/ttyUSB0
```

### 4. Boot Source and Recovery

Verify:
- Boot mode straps
- SPI/eMMC/SD/UFS/NVMe presence
- Flash voltage
- Image layout
- Recovery path: USB DFU, UART download, JTAG, external programmer

Flash/readback examples:
```bash
# SPI NOR on Linux, if exposed as MTD.
cat /proc/mtd
sudo flashrom -p linux_mtd:dev=/dev/mtd0 -r flash-readback.bin
sha256sum expected.bin flash-readback.bin

# USB devices/recovery modes.
lsusb -t
lsusb
dmesg -w
```

### 5. Minimal Boot Milestones

Track milestones:
- Power rails good
- Clock present
- Reset deasserts
- Boot ROM emits output or fetches boot source
- SPL/firmware starts
- DRAM initialized
- Bootloader/UEFI starts
- Kernel decompression starts
- Kernel mounts rootfs
- Userspace reaches login/service target
- Peripheral enumeration succeeds

## Firmware, BIOS, UEFI, and Bootloader Workflow

### Firmware Orientation

First identify:
- Firmware stack: EDK II, coreboot, U-Boot, TF-A, vendor BIOS, Slim Bootloader, custom SPL
- Boot phases
- Image layout and signing requirements
- Update mechanism
- Debug output path
- Handoff contract to OS: ACPI, device tree, SMBIOS, EFI memory map, initramfs, bootargs

For UEFI-specific work, also load and follow `uefi-firmware`.

### Build and Version Capture

Always record exact firmware provenance:
```bash
git rev-parse HEAD
git status --short
git describe --tags --always --dirty
date -Is
```

For EDK II-like builds, capture:
```bash
build -a X64 -t GCC5 -p Platform/YourBoard/YourBoard.dsc 2>&1 | tee build.log
```

For U-Boot:
```bash
make <board>_defconfig
make -j"$(nproc)" 2>&1 | tee build.log
```

For coreboot:
```bash
make olddefconfig
make -j"$(nproc)" 2>&1 | tee build.log
```

### Firmware Debug Checklist

Check:
- Does firmware run from expected boot source?
- Is DRAM training successful and stable?
- Are memory regions reserved correctly?
- Are MMIO ranges correct?
- Are clocks/resets/regulators configured before device access?
- Are ACPI/DT resources complete and accurate?
- Are interrupt polarity, GPIO numbering, and address cells correct?
- Is Secure Boot / measured boot / image signing blocking execution?
- Is the OS handoff contract stable across cold/warm boot?

### UEFI/BIOS OS-Handoff Checks

On Linux:
```bash
dmesg | grep -Ei 'efi|acpi|smbios|dmi|secure|tpm|iommu|reserved|mem'
ls /sys/firmware
ls /sys/firmware/efi || true
sudo efibootmgr -v || true
sudo acpidump -o acpi.dat
iasl -d acpi.dat
```

Device tree systems:
```bash
dtc -I fs -O dts /sys/firmware/devicetree/base > running.dts
dmesg | grep -Ei 'of:|device tree|reserved-memory|chosen'
```

Bootloader environment:
```bash
fw_printenv 2>/dev/null || true
cat /proc/cmdline
```

## Linux Kernel Integration Workflow

### 1. Establish Kernel Baseline

Capture:
```bash
uname -a
cat /proc/version
cat /proc/cmdline
zcat /proc/config.gz > running.config 2>/dev/null || true
dmesg -T > dmesg.txt
lsmod > lsmod.txt
```

If building:
```bash
make olddefconfig
make -j"$(nproc)" 2>&1 | tee kernel-build.log
```

### 2. Device Enumeration

Generic:
```bash
dmesg -T | less
dmesg -T | grep -Ei 'error|fail|warn|timeout|defer|probe|firmware'
ls /sys/bus
find /sys/bus -maxdepth 3 -name '*<device-or-driver>*' 2>/dev/null
```

PCIe:
```bash
lspci -nnvv
lspci -t
dmesg -T | grep -Ei 'pci|pcie|aer|link'
```

USB:
```bash
lsusb -t
lsusb -v
dmesg -T | grep -Ei 'usb|xhci|dwc|typec'
```

I2C:
```bash
i2cdetect -l
sudo i2cdetect -y <bus>
sudo i2cget -y <bus> <addr> <reg>
dmesg -T | grep -Ei 'i2c|smbus'
```

SPI:
```bash
ls /sys/bus/spi/devices
dmesg -T | grep -Ei 'spi|mtd|nor|nand'
cat /proc/mtd 2>/dev/null || true
```

GPIO:
```bash
gpioinfo
gpiodetect
dmesg -T | grep -Ei 'gpio|pinctrl'
```

Clocks, regulators, resets:
```bash
sudo cat /sys/kernel/debug/clk/clk_summary 2>/dev/null
sudo cat /sys/kernel/debug/regulator/regulator_summary 2>/dev/null
sudo cat /sys/kernel/debug/pinctrl/*/pinmux-pins 2>/dev/null
```

### 3. Probe Failure Triage

Classify probe failures:
- `-EPROBE_DEFER`: dependency missing, usually regulator/clock/reset/GPIO supplier
- `-ENODEV`: ID mismatch, wrong compatible/HID/CID, hardware absent
- `-EINVAL`: malformed firmware property or invalid resource
- timeout: bus, reset, clock, power, interrupt, or protocol-level issue
- firmware load error: missing file or userspace path problem

Commands:
```bash
dmesg -T | grep -Ei 'defer|probe|supplier|regulator|clock|reset|firmware'
cat /sys/kernel/debug/devices_deferred 2>/dev/null || true
find /lib/firmware -maxdepth 3 -type f | sort | less
```

### 4. Device Tree Validation

For DT systems:
```bash
make dtbs_check DT_SCHEMA_FILES=<binding>.yaml
make dt_binding_check DT_SCHEMA_FILES=<binding>.yaml
dtc -I dtb -O dts build/path/board.dtb > built.dts
dtc -I fs -O dts /sys/firmware/devicetree/base > running.dts
diff -u built.dts running.dts | less
```

Check:
- `compatible`
- `reg`
- `interrupts` and interrupt parent
- `clocks`
- `resets`
- `power-domains`
- `vdd-supply` and other regulator supplies
- `pinctrl-names` and `pinctrl-0`
- DMA properties
- `status = "okay"`

### 5. ACPI Validation

For ACPI systems:
```bash
sudo acpidump -o acpi.dat
iasl -d acpi.dat
grep -R "HID\|CID\|CRS\|DSD\|PRT\|STA" -n *.dsl
dmesg -T | grep -Ei 'acpi|dsdt|ssdt|resource|irq'
```

Check:
- `_HID` / `_CID`
- `_CRS` resources
- `_STA` device presence
- `_DSD` properties
- GPIO/interrupt polarity
- I2C/SPI serial bus descriptors
- Power resources
- Operation region side effects

### 6. Driver Debugging

Use dynamic debug:
```bash
sudo mount -t debugfs none /sys/kernel/debug 2>/dev/null || true
sudo sh -c 'echo "file drivers/path/to/driver.c +p" > /sys/kernel/debug/dynamic_debug/control'
dmesg -w
```

Use ftrace:
```bash
sudo trace-cmd record -e module -e irq -e gpio -e regulator -e clk -e spi -e i2c sleep 10
sudo trace-cmd report | less
```

Function tracing:
```bash
sudo sh -c 'echo function_graph > /sys/kernel/debug/tracing/current_tracer'
sudo sh -c 'echo <driver_probe_function> > /sys/kernel/debug/tracing/set_graph_function'
sudo cat /sys/kernel/debug/tracing/trace_pipe
```

## Userspace Integration Workflow

After kernel enumeration is proven:

### Device Nodes and Permissions

```bash
ls -l /dev
udevadm info --attribute-walk --name=/dev/<node>
udevadm monitor --environment --udev
systemctl status systemd-udevd
```

### systemd Services

```bash
systemctl status <service>
journalctl -u <service> -b --no-pager
systemd-analyze blame
systemd-analyze critical-chain
```

### Firmware Blobs

```bash
dmesg -T | grep -Ei 'firmware|Direct firmware load'
find /lib/firmware -maxdepth 4 -type f | sort
modinfo <driver> | grep -i firmware
```

### Runtime Libraries and HALs

```bash
ldd /usr/bin/<tool>
strace -f -o trace.txt /usr/bin/<tool> <args>
journalctl -b | grep -Ei '<device>|<driver>|permission|denied|firmware'
```

## Common Cross-Layer Failure Patterns

### Device Does Not Appear in Linux

Work downward:
1. Is it physically powered?
2. Is reset deasserted?
3. Is the clock present?
4. Are straps/address pins correct?
5. Does bus probing see anything?
6. Does firmware describe it?
7. Does the driver match the compatible/HID/ID?
8. Did probe defer or fail?
9. Does userspace have permission?

Commands:
```bash
dmesg -T | grep -Ei 'probe|defer|fail|timeout|regulator|clk|reset|pinctrl'
cat /sys/kernel/debug/devices_deferred 2>/dev/null || true
```

### Intermittent Boot Failure

Check:
- Power ramp and reset timing
- Clock startup time
- DRAM training margins
- Temperature dependence
- Race in firmware resource init
- Kernel async probe order
- Brownout during inrush
- Uninitialized GPIO/pinmux state

Run repeated tests:
```bash
for i in $(seq 1 50); do
  echo "cycle $i $(date -Is)"
  # Insert board-specific reboot/power-cycle command here.
  sleep 5
done | tee reboot-cycles.log
```

### Probe Defer Never Resolves

Check supplier:
```bash
cat /sys/kernel/debug/devices_deferred 2>/dev/null
dmesg -T | grep -Ei 'supplier|defer|regulator|clock|reset|gpio'
```

Likely causes:
- Missing regulator node
- Wrong phandle
- Clock provider not enabled
- Driver not built
- Load order issue
- ACPI/DT resource mismatch

### PCIe Link Down

Check:
- Refclk
- PERST# timing
- CLKREQ#
- power rails
- lane polarity/reversal support
- reset GPIO ownership
- firmware resource allocation
- ASPM/L1 substates
- endpoint strap mode

Commands:
```bash
lspci -vv
dmesg -T | grep -Ei 'pcie|pci|aer|link|aspm|reset'
sudo setpci -s <bus:dev.fn> CAP_EXP+0x12.w
```

### USB Not Enumerating

Check:
- VBUS
- CC orientation/type-C controller
- D+/D- or SS lane routing
- PHY clocks/resets
- overcurrent GPIO polarity
- role switching
- firmware DT/ACPI PHY linkage

Commands:
```bash
lsusb -t
dmesg -w
dmesg -T | grep -Ei 'usb|xhci|dwc|phy|typec|role'
```

### I2C/SPI Device Missing

Check:
- voltage and pull-ups
- address pins
- bus speed
- pinmux
- reset/power sequence
- chip select polarity
- level shifting
- firmware resource description

Commands:
```bash
i2cdetect -l
sudo i2cdetect -y <bus>
sudo i2ctransfer -y <bus> w1@<addr> <reg> r1
ls /sys/bus/spi/devices
```

### Suspend/Resume Failure

Check:
- wake sources
- power domains
- IRQ wake configuration
- regulator state in suspend
- firmware sleep states
- device runtime PM
- ordering of resume callbacks

Commands:
```bash
dmesg -T | grep -Ei 'suspend|resume|wakeup|pm:|dpm|freeze|thaw'
cat /sys/kernel/debug/wakeup_sources 2>/dev/null
sudo rtcwake -m mem -s 10
```

## Code and Repository Inspection

When a repository is available, inspect before advising.

Useful commands:
```bash
git status --short
git log --oneline -20
git diff --stat
git grep -n "<compatible-or-driver-name>"
git grep -n "MODULE_DEVICE_TABLE\|of_match_table\|acpi_match_table"
git grep -n "regulator_get\|clk_get\|reset_control\|devm_gpiod"
```

Kernel tree orientation:
```bash
git grep -n "compatible = \".*<vendor>.*\"" Documentation/devicetree/bindings drivers arch
git grep -n "<driver_name>" drivers Documentation
```

Firmware tree orientation:
```bash
git grep -n "<GUID-or-protocol-or-board-name>"
git grep -n "<device-or-interface-name>"
```

## Minimal Artifacts to Request or Produce

For hardware design:
- Schematic PDF or relevant pages
- PCB revision
- Datasheet links/sections
- Interface matrix
- Power tree
- Clock/reset tree

For bring-up:
- Board revision and BOM variant
- Photos of setup if available
- Rail measurements
- Scope/logic analyzer captures
- Full serial log from reset
- Firmware image version/hash

For firmware:
- Firmware repo commit
- Build command and build log
- Flash layout
- Boot log
- ACPI dump or DTB/DTS
- Secure/signing policy

For Linux:
- Kernel commit/version
- `.config`
- full `dmesg`
- `/proc/cmdline`
- DT/ACPI dump
- driver probe logs
- relevant `/sys` state

For userspace:
- service logs
- udev rules
- permissions
- firmware blob paths
- exact tool command and output

## Output Templates

### Investigation Summary

```text
Symptom:
Board/SoC:
Board revision:
Firmware version:
Kernel version:
Interface/device:
Reproduction steps:

Layer assessment:
- Hardware:
- Firmware/bootloader:
- Kernel:
- Userspace:

Evidence:
- Logs:
- Measurements:
- Register/sysfs state:
- Known-good comparison:

Most likely root cause:
Next verification:
Smallest proposed change:
Rollback plan:
```

### Bring-Up Status Table

```text
Milestone                         Status   Evidence
Power input current               PASS/FAIL
Always-on rails                   PASS/FAIL
Main rails                        PASS/FAIL
Reference clocks                  PASS/FAIL
Reset deassertion                 PASS/FAIL
Boot straps                       PASS/FAIL
Boot ROM activity                 PASS/FAIL
Firmware starts                   PASS/FAIL
DRAM init                         PASS/FAIL
Kernel starts                     PASS/FAIL
Rootfs/userspace                  PASS/FAIL
Target peripheral enumerates      PASS/FAIL
```

### Hardware Review Finding

```text
Finding:
Severity: Blocker / High / Medium / Low
Layer: Schematic / Layout / Firmware dependency / Linux dependency / Manufacturing
Evidence:
Risk:
Recommendation:
Verification method:
```

## Pitfalls

1. Debugging Linux before power/reset/clock is proven.
   - Fix: verify rail, reset, clock, and bus presence first.

2. Treating a device tree or ACPI node as proof the hardware exists.
   - Fix: confirm physical bus response and driver binding separately.

3. Ignoring board revision and BOM variant.
   - Fix: record revision in every log and compare against known-good hardware.

4. Skipping full boot logs.
   - Fix: capture from reset through userspace; early warnings often explain late failures.

5. Using `i2cdetect` unsafely on sensitive devices.
   - Fix: check datasheet; avoid probing PMICs, EEPROMs, or write-sensitive devices blindly.

6. Confusing pin number spaces.
   - Fix: distinguish package ball, schematic net, SoC GPIO number, Linux GPIO line, and connector pin.

7. Missing pinmux ownership.
   - Fix: inspect firmware pinmux, bootloader pinmux, kernel pinctrl, and runtime overlays.

8. Assuming warm reboot equals cold boot.
   - Fix: test cold power cycle, warm reset, software reboot, and suspend/resume separately.

9. Forgetting firmware tables.
   - Fix: dump ACPI/DT from the running system; do not assume built DTB or source ASL is what booted.

10. Fixing symptoms with delays.
    - Fix: measure and model sequencing; use proper dependencies, reset controls, and readiness checks.

11. Changing multiple layers at once.
    - Fix: one variable per test; record firmware, kernel, and hardware state for each run.

12. Overlooking userspace policy.
    - Fix: after kernel success, check udev, permissions, systemd ordering, firmware paths, and service logs.

13. Treating intermittent failures as “lab noise.”
    - Fix: repeat cycles, vary temperature/power, and capture statistics.

14. Ignoring manufacturing testability.
    - Fix: add test points, recovery paths, fixture hooks, and serial numbers early.

15. Presenting vendor-specific behavior as standard behavior.
    - Fix: label source: datasheet, UEFI/ACPI/PCI/USB spec, EDK II/coreboot/U-Boot implementation, board policy, Linux driver behavior.

## Verification Checklist

Before declaring success:

- [ ] Board revision, BOM variant, firmware version, and kernel version recorded
- [ ] Full boot log captured from reset through target behavior
- [ ] Power rails measured under relevant load
- [ ] Reset and clock behavior verified
- [ ] Boot mode and straps confirmed
- [ ] Firmware image provenance recorded
- [ ] ACPI or device tree dump captured from the running system
- [ ] Kernel config and dmesg captured
- [ ] Target driver binding verified
- [ ] Probe errors, deferrals, and firmware-load failures checked
- [ ] Userspace permissions/services checked when applicable
- [ ] Cold boot and warm reboot tested
- [ ] Regression or manufacturing test added where possible
- [ ] Known-good comparison performed when available
- [ ] All assumptions labeled by source: measurement, log, code, datasheet, or spec

## One-Shot Recipes

### Recipe: “Peripheral is not detected”

```bash
uname -a
cat /proc/cmdline
dmesg -T | tee dmesg.txt
dmesg -T | grep -Ei 'probe|defer|fail|timeout|regulator|clock|reset|pinctrl|firmware'
cat /sys/kernel/debug/devices_deferred 2>/dev/null || true
sudo cat /sys/kernel/debug/clk/clk_summary 2>/dev/null | grep -i <device>
sudo cat /sys/kernel/debug/regulator/regulator_summary 2>/dev/null | grep -i <rail-or-device>
```

Then verify physically:
- rail voltage
- reset line
- clock
- bus activity
- address/strap pins

### Recipe: “Kernel driver does not bind”

```bash
modinfo <driver>
lsmod | grep <driver> || true
dmesg -T | grep -i <driver>
find /sys/bus -maxdepth 4 -name '*<device>*' 2>/dev/null
git grep -n "of_match_table\|acpi_match_table\|MODULE_DEVICE_TABLE" drivers/
```

Check:
- compatible/HID/CID matches
- driver built-in or module loaded
- resources complete
- no probe defer
- firmware blob available

### Recipe: “ACPI or device tree mismatch”

Device tree:
```bash
dtc -I fs -O dts /sys/firmware/devicetree/base > running.dts
grep -n "<device>" running.dts
```

ACPI:
```bash
sudo acpidump -o acpi.dat
iasl -d acpi.dat
grep -R "<HID-or-device>" -n *.dsl
```

Compare against firmware source and the kernel driver binding.

### Recipe: “Boot hang”

```bash
# Capture serial from reset.
script -f logs/boot-hang-$(date +%Y%m%d-%H%M%S).log
sudo picocom -b 115200 /dev/ttyUSB0
```

Classify last known phase:
- no output: power, reset, clock, boot straps, ROM, UART mux
- SPL only: DRAM, boot media, image format
- bootloader only: kernel image, initrd, DT/ACPI, bootargs
- kernel early hang: earlycon, memory map, interrupt controller, timer
- userspace hang: rootfs, init, systemd, storage, permissions

### Recipe: “Firmware update did not change behavior”

```bash
sha256sum firmware.bin
git rev-parse HEAD
strings firmware.bin | grep -Ei 'version|build|date|board' | head
```

Verify:
- image was built from intended commit
- image was flashed to active slot
- readback matches
- boot log reports new version
- no fallback slot was selected

## Final Reporting Style

When reporting to the user, be concise but evidence-based:

- State the likely layer and why.
- List the evidence already verified.
- List the next one or two measurements/commands.
- Avoid broad rewrites until the failing boundary is proven.
- If uncertainty remains, name the exact missing artifact.

Good example:

```text
This currently looks like a firmware-description or pinctrl issue, not a userspace issue:
- The device rail is present and reset is deasserted.
- I2C bus 3 responds, but the kernel driver never binds.
- dmesg shows no matching compatible string and the running DT lacks the sensor node.

Next checks:
1. Dump running DT and compare with the built DTB.
2. Confirm the sensor compatible and supply names against the kernel binding.
```

Bad example:

```text
Just add a delay in the driver.
```

Delays are a last resort only after sequencing and readiness signals have been proven.
