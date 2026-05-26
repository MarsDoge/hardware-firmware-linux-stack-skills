# Linux ACPI Debugging

## Evidence Collection

```bash
uname -a
cat /proc/cmdline
dmesg -T > dmesg.txt
dmesg -T | grep -Ei 'acpi|aml|dsdt|ssdt|irq|gsi|gpio|i2c|spi|uart|resource|probe'
sudo acpidump -o acpi.dat
acpixtract -a acpi.dat
iasl -e ssdt*.dat -d dsdt.dat
```

## Device Discovery

```bash
find /sys/bus/acpi/devices -maxdepth 2 -type f \( -name hid -o -name modalias -o -name path -o -name status \) -print -exec cat {} \;
```

Useful paths: `/sys/firmware/acpi/tables/`, `/sys/bus/acpi/devices/`, `/sys/bus/platform/devices/`, `/proc/interrupts`, `/proc/iomem`.

## Common Log Patterns

- `ACPI BIOS Error (bug): Could not resolve symbol`: missing namespace reference or external SSDT dependency.
- `AE_NOT_FOUND`: missing object or unresolved name.
- `AE_AML_OPERAND_TYPE`: wrong AML type.
- IRQ/resource conflict: compare `_CRS`, `/proc/interrupts`, `/proc/iomem`, driver resources.
- Device not binding: check `_STA`, IDs, modalias, driver ACPI match table.
- GPIO lookup failure: check `_CRS` GPIO descriptors, `_DSD` property name, controller path, index, polarity.
