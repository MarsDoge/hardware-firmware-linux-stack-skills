# PCIe Debug Workflows

## No Device in lspci

```bash
uname -a
cat /proc/cmdline
dmesg -T | tee dmesg.txt
lspci -nn
lspci -tv
dmesg -T | grep -Ei 'pci|pcie|mcfg|ecam|link|resource|bar|aer|dpc'
```

Then check: root port visible/enabled, ECAM/MCFG or DT host bridge, bridge windows, endpoint rails, REFCLK, PERST#, straps, lane map, retimer/redriver, cable/riser.

## Wrong Speed or Width

```bash
DEV=<bus:dev.fn>
sudo lspci -s "$DEV" -vv
cat /sys/bus/pci/devices/0000:$DEV/current_link_speed
cat /sys/bus/pci/devices/0000:$DEV/current_link_width
cat /sys/bus/pci/devices/0000:$DEV/max_link_speed
cat /sys/bus/pci/devices/0000:$DEV/max_link_width
```

Check BIOS generation limit, lane bifurcation, endpoint strap/config, retimer mode, insertion loss/equalization, lane reversal/polarity support, cable/riser rating.

## AER/DPC Storm

```bash
dmesg -T | grep -Ei 'aer|dpc|pcie bus error|corrected|uncorrected|fatal|non-fatal'
sudo lspci -vv | grep -Ei 'AER|DPC|UESta|CESta|DevSta|LnkSta' -A5 -B3
```

Classify error first; do not treat AER text as the root cause.

## BAR/Resource Failure

```bash
dmesg -T | grep -Ei 'BAR|resource|bridge window|no space|failed to assign'
sudo lspci -tv
sudo lspci -vv
```

Check above-4G decoding, 64-bit BARs, bridge windows, bus numbers, ACPI `_CRS`, MCFG/ECAM.
