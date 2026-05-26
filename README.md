# hardware-firmware-linux-stack-skill

A Hermes/Agent Skills-compatible skill for cross-layer hardware, firmware, BIOS/UEFI, bootloader, Linux kernel, and userspace engineering.

This skill is a broad orchestrator for hardware/firmware/Linux work. It helps agents reason across schematics, board bring-up, BIOS/UEFI/bootloader handoff, ACPI/device tree, Linux driver probe, and userspace validation.

## What it covers

- Hardware design review: schematic, PCB constraints, power/clock/reset, interface matrix
- Board bring-up: rails, clocks, resets, straps, serial console, recovery path
- Firmware / BIOS / UEFI / bootloader: image provenance, OS handoff, ACPI/DT/SMBIOS
- Linux kernel enablement: driver binding, probe defer, regulators, clocks, resets, pinctrl, GPIO, I2C/SPI/PCIe/USB
- Userspace integration: udev, systemd, firmware blobs, permissions, diagnostics
- Cross-layer debugging: evidence-first triage from hardware through userspace

## Install for Hermes Agent

```bash
mkdir -p ~/.hermes/skills/software-development
cp -R skills/hardware-firmware-linux-stack ~/.hermes/skills/software-development/hardware-firmware-linux-stack
```

Then restart Hermes or reload skills if your runtime supports it.

## Install from GitHub

```bash
git clone https://github.com/MarsDoge/hardware-firmware-linux-stack-skill.git /tmp/hardware-firmware-linux-stack-skill
mkdir -p ~/.hermes/skills/software-development
cp -R /tmp/hardware-firmware-linux-stack-skill/skills/hardware-firmware-linux-stack ~/.hermes/skills/software-development/hardware-firmware-linux-stack
```

## Skill structure

```text
skills/hardware-firmware-linux-stack/
├── SKILL.md
└── references/
    └── skill-development-method.md
```

## Design notes

- This is intentionally a cross-layer orchestration skill, not a monolithic protocol encyclopedia.
- Specialized skills can branch out later for PCIe, USB, DDR/LPDDR, ACPI, UEFI, BMC/EC, power/thermal, board bring-up, and Linux kernel subsystems.
- Official specification landing pages are referenced instead of copying proprietary spec text.
- Nuwa-style distillation is optional: use it only when it improves a technical skill; skip it if it adds overhead or persona-like baggage.

## Related references

- MarsDoge UEFI firmware skill: https://github.com/MarsDoge/uefi-firmware-skill
- PCI-SIG specifications: https://pcisig.com/specifications
- UEFI Forum specifications: https://uefi.org/specifications
- Linux kernel docs: https://docs.kernel.org/

## License

MIT
