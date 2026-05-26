---
name: board-bringup-lab
description: Use when powering, measuring, booting, or debugging new hardware prototypes in a lab. Provides an evidence-first board bring-up workflow covering pre-power checks, rails, clocks, resets, straps, serial/JTAG access, boot media, firmware handoff, peripheral smoke tests, artifacts, pitfalls, and verification.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hardware, board-bringup, lab, embedded, power, clocks, reset, firmware, bootloader, diagnostics]
    related_skills: [hardware-firmware-linux-stack, pcie-debug-and-design, linux-kernel-driver-enablement]
---

# Board Bring-Up Lab

## Overview

Use this skill for first-power, prototype validation, lab debug, and board-revision evidence capture. The goal is to move from unknown hardware state to verified boot/peripheral baseline without skipping physical-layer proof.

Core rule: do not debug firmware or Linux until power rails, clocks, reset, boot straps, and debug access have been proven with measurements or logs.

## When to Use

Use when bringing up a new PCB/EVT/DVT/PVT unit/reworked prototype/BOM variant; first power-on; dead-board/no-boot/no-UART/reset-loop/brownout/boot-media triage; or creating lab handoff evidence.

Do not use as the primary skill for pure Linux driver probe issues after hardware/firmware are proven, pure schematic review without lab activity, or app-level debugging.

## Required Inputs

```text
Board name/revision/BOM/serial:
SoC/CPU/MCU:
Power source and expected input current:
Firmware stack and boot source:
Debug ports available:
Target milestone:
Known-good comparison:
Lab tools available:
```

Minimum evidence: board photo/ID, schematic pages for power/reset/clocks/straps/debug headers, power tree, boot strap table, serial log if any, firmware image version/hash.

## Bring-Up Workflow

### 1. Create a Session Folder

```bash
export BRINGUP_DIR="bringup/$(date +%Y%m%d-%H%M%S)-<board>-<rev>"
mkdir -p "$BRINGUP_DIR"/{logs,measurements,photos,firmware,notes}
date -Is | tee "$BRINGUP_DIR/session.txt"
uname -a | tee -a "$BRINGUP_DIR/session.txt"
```

### 2. Pre-Power Checks

Power off. Verify: visual inspection, correct rev/BOM, no solder bridges/reversed parts, rail resistance-to-ground, input polarity, jumpers/straps, current limit, emergency power-off.

Do not power if input rail is shorted, PMIC orientation is suspect, boot/power jumper is unknown, or current limit is not configured.

### 3. First Power

Apply power with current limiting. Measure input current, always-on rails, main rails, enables/PGOODs, reset lines, oscillators, and boot straps at reset sampling time. Stop on unexpected current limit hit, rapid heating, rail overvoltage, or contradictory sequence.

### 4. Establish Debug Access

Find earliest channel: Boot ROM UART, SPL/U-Boot UART, UEFI serial, JTAG/SWD, USB recovery/DFU, SPI programmer, BMC/EC console.

```bash
ls -l /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
sudo picocom -b 115200 /dev/ttyUSB0
script -f "$BRINGUP_DIR/logs/serial-$(date +%Y%m%d-%H%M%S).log"
```

If no serial: check UART voltage, TX/RX crossover, baud, pinmux/default console, TX activity on scope, reset deassertion.

### 5. Boot Source and Recovery

Verify straps, storage power, flash voltage, image layout/signing, and recovery before risky flashing.

```bash
lsusb; lsusb -t
dmesg -T | grep -Ei 'usb|dfu|serial|flash|mtd|mmc|sdhci|nvme|spi'
cat /proc/mtd 2>/dev/null || true
lsblk
```

### 6. Milestone Tracking

```text
Milestone                         Status   Evidence
Input current sane                PASS/FAIL
Always-on rails valid             PASS/FAIL
Main rails valid                  PASS/FAIL
Reference clocks present          PASS/FAIL
Reset deasserts                   PASS/FAIL
Boot straps sampled correctly     PASS/FAIL
Boot ROM activity                 PASS/FAIL
SPL/first firmware starts         PASS/FAIL
DRAM init                         PASS/FAIL
Bootloader/UEFI starts            PASS/FAIL
Kernel starts                     PASS/FAIL
Rootfs/userspace starts           PASS/FAIL
Target peripheral smoke-tested    PASS/FAIL
```

### 7. Peripheral Smoke Tests

After stable boot:

```bash
uname -a | tee "$BRINGUP_DIR/logs/uname.txt"
cat /proc/cmdline | tee "$BRINGUP_DIR/logs/cmdline.txt"
dmesg -T | tee "$BRINGUP_DIR/logs/dmesg.txt"
lsmod | tee "$BRINGUP_DIR/logs/lsmod.txt"
lspci -nnvv | tee "$BRINGUP_DIR/logs/lspci.txt"
lsusb -t | tee "$BRINGUP_DIR/logs/lsusb-tree.txt"
i2cdetect -l | tee "$BRINGUP_DIR/logs/i2c-buses.txt"
gpioinfo | tee "$BRINGUP_DIR/logs/gpioinfo.txt"
```

Do not blindly probe sensitive I2C devices.

## Common Pitfalls

1. Powering without current limit.
2. Debugging firmware before reset/clock are proven.
3. Assuming no UART output means firmware failure.
4. Measuring boot straps after Linux pinmux changes them.
5. Flashing without recovery path.
6. Treating warm reboot success as cold-boot success.
7. Losing board identity in logs.
8. Changing hardware, firmware, and kernel at once.

## Verification Checklist

- [ ] Board revision/BOM/serial recorded
- [ ] Pre-power inspection and rail R-to-GND complete
- [ ] Current-limited first power performed
- [ ] Critical rails, reset, clocks, boot straps measured
- [ ] Serial/JTAG/recovery path proven
- [ ] Firmware version/hash recorded
- [ ] Full boot log captured from reset
- [ ] Kernel/userspace baseline captured if Linux boots
- [ ] Key buses enumerated and target peripheral smoke-tested
- [ ] Cold boot and warm reboot tested
- [ ] Open issues listed with evidence and next measurement

## References

See `references/lab-checklists.md`, `references/evidence-log-template.md`, `references/bringup-command-recipes.md`, `references/failure-patterns.md`, templates, and scripts.
