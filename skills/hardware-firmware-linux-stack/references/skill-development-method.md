# Skill Development Method: Nuwa-Inspired Technical Distillation

This reference adapts the idea from https://github.com/alchaincyf/nuwa-skill for technical hardware/firmware/Linux skills.

Nuwa-style distillation is optional. Use it only when it clearly improves a technical skill; if it adds ceremony, overhead, or persona-like baggage, skip it. Technical engineering skills should distill an expert workflow rather than imitate a persona. The goal is not to copy someone's voice; it is to extract a repeatable engineering operating system.

## When to Use This Method

Use this method only when it helps produce a better skill with less ambiguity. Good fit:

- The domain has expert judgment that is hard to capture as simple commands.
- There are many similar-looking failures across hardware, firmware, kernel, and userspace layers.
- A strong heuristic/evidence model would prevent repeated mistakes.
- The skill is class-level and worth maintaining over time.

Skip this method when:

- A simple checklist or command recipe is enough.
- The method would create verbose process text without better runtime behavior.
- The result starts looking like roleplay/persona instead of engineering guidance.
- The skill can be improved faster by adding a focused `references/spec-map.md`, `references/workflows.md`, or `templates/debug-report.md` file.

Use this method when creating or updating focused domain skills such as:

- PCIe debug/design
- USB/Type-C/PD enablement
- DDR/LPDDR bring-up
- ACPI platform enablement
- UEFI/EDK II firmware development
- Linux kernel driver enablement
- BMC/EC/power/thermal control
- Board bring-up lab workflow
- Manufacturing validation

Do not use it to add long copied specification text. Use official spec landing pages and cite section/table identifiers instead.

## Technical Distillation Layers

For technical skills, distill these layers:

| Layer | What to Extract | Example |
| --- | --- | --- |
| Trigger model | When this skill should activate | `PCIe link down`, `driver probe defer`, `ACPI _CRS mismatch` |
| System model | How experts decompose the domain | PCIe: PHY/link/transaction/config/software; Firmware: PEI/DXE/BDS/OS handoff |
| Evidence model | What data proves or disproves hypotheses | scope traces, LTSSM state, dmesg, lspci -vv, ACPI dump, running DT |
| Decision heuristics | What to check first, second, never skip | prove rail/refclk/PERST# before changing Linux driver |
| Command recipes | Exact commands and expected artifacts | `lspci -nnvv`, `acpidump`, `dtc`, `trace-cmd`, `setpci` |
| Spec map | Official references and section pointers | PCI-SIG, UEFI Forum, ACPI spec, Linux docs, vendor datasheets |
| Failure patterns | Repeated root causes and signatures | polarity mismatch, missing regulator, bad pinmux, probe defer supplier missing |
| Boundaries | What the skill cannot know or must not assume | proprietary spec text, board-specific schematics, vendor policy, unpublished errata |

## Recommended Directory Shape

For each class-level skill:

```text
<skill-name>/
├── SKILL.md
└── references/
    ├── spec-map.md          # official links, spec versions, section/table pointers
    ├── workflows.md         # step-by-step lab/code/debug workflows
    ├── evidence-checklist.md # required logs, measurements, dumps, screenshots
    └── pitfalls.md          # recurring failure modes and false assumptions
```

Optional for deeper skills:

```text
scripts/
  collect-evidence.sh        # safe read-only data collection where possible
templates/
  debug-report.md            # standardized issue/report template
```

## Research and Distillation Workflow

1. Define the domain boundary.
   - Example: `pcie-debug-and-design` covers link training, CEM timing, Linux PCIe debug, but not all storage/NVMe internals.

2. Collect source classes.
   - Official specs and landing pages
   - Vendor datasheets and design guides
   - Linux kernel docs and bindings
   - Firmware docs and code examples
   - Known-good debug logs and bug reports
   - Existing MarsDoge repos/skills, including https://github.com/MarsDoge/uefi-firmware-skill when relevant

3. Extract expert heuristics.
   - What does an expert check before touching code?
   - Which failures look similar but live in different layers?
   - Which measurements are decisive?
   - Which logs are misleading without hardware evidence?

4. Convert into Hermes skill runtime behavior.
   - `When to Use`
   - `When Not to Use`
   - `Layer Model`
   - `First Response Workflow`
   - `One-Shot Recipes`
   - `Common Pitfalls`
   - `Verification Checklist`

5. Keep the skill modular.
   - Put detailed reference maps in `references/`.
   - Keep `SKILL.md` actionable and scannable.
   - Link to adjacent skills instead of duplicating them.

6. Verify the skill.
   - Frontmatter parses.
   - Description <= 1024 chars.
   - Skill directory is self-contained.
   - External links are official or clearly marked as community references.
   - No copyrighted spec text is copied.
   - Recipes are safe by default and destructive actions require explicit confirmation.

## Citation Format

Use this compact format in skill references:

```text
Source: PCI-SIG PCI Express Base Specification, version X.Y, section/table Z
URL: https://pcisig.com/specifications
Use: LTSSM state interpretation / equalization requirement / PERST# timing boundary
Notes: Do not quote proprietary text; summarize engineering implication only.
```

For open docs:

```text
Source: Linux kernel documentation, Documentation/devicetree/bindings/<path>
Repo/kernel version: <commit or release>
Use: binding property names and required resources
```

## Key Rule

Nuwa-style distillation is useful as a methodology, not as a runtime persona requirement. For hardware/firmware/Linux skills, distill how a strong engineer thinks, verifies, and decides; do not turn the skill into roleplay.