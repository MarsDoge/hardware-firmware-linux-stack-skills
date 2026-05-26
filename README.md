# hardware-firmware-linux-stack-skills

A Hermes/Agent Skills-compatible collection for cross-layer hardware, firmware, BIOS/UEFI, bootloader, Linux kernel, and userspace engineering.

This repo is intentionally structured as a modular skill collection. The main skill is a cross-layer router/orchestrator; deeper areas such as PCIe, ACPI, board bring-up, and Linux driver enablement live as focused child skills that cross-link back to the router.

## Skills

```text
skills/
├── hardware-firmware-linux-stack/        # cross-layer router/orchestrator
├── pcie-debug-and-design/                # PCIe design, link training, AER, ASPM, enumeration
├── acpi-platform-enablement/             # ACPI DSDT/SSDT, _CRS/_DSD/_STA, Linux ACPI handoff
├── board-bringup-lab/                    # first power, rails, clocks, reset, straps, lab evidence
└── linux-kernel-driver-enablement/       # driver binding/probe/resources/DT/ACPI/upstreaming
```

## What it covers

- Hardware design review: schematic, PCB constraints, power/clock/reset, interface matrix
- Board bring-up: rails, clocks, resets, straps, serial console, recovery path
- Firmware / BIOS / UEFI / bootloader: image provenance, OS handoff, ACPI/DT/SMBIOS
- PCIe: root ports, endpoints, retimers, link speed/width, AER/DPC, ASPM, resource windows
- ACPI: DSDT/SSDT, `_CRS`, `_DSD`, `_STA`, table handoff, Linux ACPI debug
- Linux kernel enablement: driver binding, probe defer, regulators, clocks, resets, pinctrl, GPIO, I2C/SPI/PCIe/USB
- Userspace integration: udev, systemd, firmware blobs, permissions, diagnostics
- Cross-layer debugging: evidence-first triage from hardware through userspace

## Install for Hermes Agent

Install all skills from an already cloned repo:

```bash
mkdir -p ~/.hermes/skills/software-development
cp -R skills/* ~/.hermes/skills/software-development/
```

Install only the main router skill:

```bash
mkdir -p ~/.hermes/skills/software-development
cp -R skills/hardware-firmware-linux-stack ~/.hermes/skills/software-development/hardware-firmware-linux-stack
```

Install one child skill:

```bash
mkdir -p ~/.hermes/skills/software-development
cp -R skills/pcie-debug-and-design ~/.hermes/skills/software-development/pcie-debug-and-design
```

Then restart Hermes or reload skills if your runtime supports it.

## Install from GitHub

Install all skills:

```bash
git clone https://github.com/MarsDoge/hardware-firmware-linux-stack-skills.git /tmp/hardware-firmware-linux-stack-skills
mkdir -p ~/.hermes/skills/software-development
cp -R /tmp/hardware-firmware-linux-stack-skills/skills/* ~/.hermes/skills/software-development/
```

Install only the main router skill:

```bash
git clone https://github.com/MarsDoge/hardware-firmware-linux-stack-skills.git /tmp/hardware-firmware-linux-stack-skills
mkdir -p ~/.hermes/skills/software-development
cp -R /tmp/hardware-firmware-linux-stack-skills/skills/hardware-firmware-linux-stack ~/.hermes/skills/software-development/hardware-firmware-linux-stack
```

## Repository structure

```text
skills/<skill-name>/
├── SKILL.md
├── references/   # spec maps, workflows, evidence checklists, pitfalls
├── templates/    # report templates / CSV templates when useful
└── scripts/      # optional evidence collection helpers
```

Current support files include:

```text
skills/pcie-debug-and-design/references/{spec-map,workflows,evidence-checklist,pitfalls}.md
skills/acpi-platform-enablement/references/{spec-map,linux-acpi-debugging,asl-review-checklists,firmware-handoff}.md
skills/board-bringup-lab/references/*.md
skills/board-bringup-lab/templates/*
skills/board-bringup-lab/scripts/*.sh
skills/linux-kernel-driver-enablement/references/*.md
skills/linux-kernel-driver-enablement/templates/*
skills/linux-kernel-driver-enablement/scripts/*.sh
```

## Validation

Run the same checks as CI before committing:

```bash
python scripts/validate-skills.py
find skills -path '*/scripts/*.sh' -print0 | xargs -0 -r bash -n
git diff --check
```

GitHub Actions runs `.github/workflows/validate-skills.yml` on push, pull request, and manual dispatch. The validator checks skill frontmatter, description length, required headings, related-skill references, support-file links, and executable shell helpers.

## Design notes

- The main `hardware-firmware-linux-stack` skill is a router/orchestrator, not a monolithic protocol encyclopedia.
- Child skills are class-level references. They should stay practical: workflows, evidence models, command recipes, pitfalls, and verification checklists.
- Official specification landing pages are referenced instead of copying proprietary spec text.
- For standards work, cite spec name/version/section/table plus engineering implication; do not paste copyrighted spec content.
- Nuwa/Nvwa-style distillation is optional: use it only when it improves a technical skill; skip it if it adds overhead or persona-like baggage.

## Related references

- MarsDoge UEFI firmware skill: https://github.com/MarsDoge/uefi-firmware-skill
- PCI-SIG specifications: https://pcisig.com/specifications
- UEFI Forum specifications: https://uefi.org/specifications
- Linux kernel docs: https://docs.kernel.org/
- Linux PCI docs: https://docs.kernel.org/PCI/
- Linux ACPI docs: https://docs.kernel.org/firmware-guide/acpi/

## License

MIT
