# ACPI / UEFI / Linux Spec Map

## Official Specifications

- UEFI Forum ACPI specs: https://uefi.org/specifications and https://uefi.org/specs/ACPI/
- UEFI specs: https://uefi.org/specifications and https://uefi.org/specs/UEFI/
- ACPICA: https://acpica.org/ and https://github.com/acpica/acpica
- Linux ACPI docs: https://docs.kernel.org/firmware-guide/acpi/
- Linux source areas: `drivers/acpi/`, `drivers/acpi/acpica/`, `include/acpi/`, `include/linux/acpi.h`

## Section-Pointer Style

Use references like:
- ACPI 6.x, ACPI System Description Tables
- ACPI 6.x, Definition Blocks and Namespace
- ACPI 6.x, Device Configuration Objects: `_HID`, `_CID`, `_UID`, `_ADR`, `_STA`, `_CRS`, `_DSD`, `_DEP`, `_OSC`
- ACPI 6.x, GPIO and Serial Bus Connection Resource Descriptors
- UEFI 2.x, Configuration Table / ACPI table GUID handoff

## Related Skill

MarsDoge UEFI firmware skill: https://github.com/MarsDoge/uefi-firmware-skill

Use for broader firmware navigation and spec-boundary discipline. Do not copy normative spec text.
