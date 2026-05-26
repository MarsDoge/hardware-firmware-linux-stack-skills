# Firmware Handoff for ACPI Tables

## Handoff Chain

```text
platform firmware source/config
  -> AML/table build
  -> firmware installs ACPI tables
  -> UEFI configuration table exposes RSDP
  -> boot loader preserves/passes tables
  -> kernel locates RSDP/XSDT/FADT/DSDT/SSDT
  -> ACPICA parses namespace
  -> Linux ACPI core creates devices/fwnodes
  -> bus/framework/driver probes
```

## edk2 Orientation

```text
EFI_ACPI_TABLE_PROTOCOL
InstallAcpiTable()
MdePkg/Include/IndustryStandard/Acpi*.h
MdeModulePkg/Universal/Acpi/AcpiTableDxe/
DynamicTablesPkg/
Platform/*/
Silicon/*/
```

Search:
```bash
git grep -n "EFI_ACPI_TABLE_PROTOCOL"
git grep -n "InstallAcpiTable"
git grep -n "DefinitionBlock"
git grep -n "_CRS\|_DSD\|_STA\|_HID\|_CID"
```

## Product vs Diagnostic

Diagnostic: initrd table override, one-off AML patch, kernel cmdline workaround. Product: firmware source/generator/config fix or upstream Linux binding/driver fix when firmware is correct.
