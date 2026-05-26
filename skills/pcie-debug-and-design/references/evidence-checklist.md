# PCIe Evidence Checklist

## Identification
- [ ] Board name/revision/BOM/rework
- [ ] CPU/SoC/chipset/root complex
- [ ] Endpoint/switch/retimer/redriver part numbers
- [ ] Connector/slot/cable/riser
- [ ] Expected PCIe generation and width
- [ ] Firmware/BIOS version and settings
- [ ] Kernel version/config

## Linux Artifacts
- [ ] `uname -a`, `/proc/cmdline`, full `dmesg -T`
- [ ] `lspci -nn`, `lspci -tv`, `lspci -nnvv`, `lspci -xxxx`
- [ ] `current_link_speed`, `current_link_width`, max link values
- [ ] AER/DPC logs
- [ ] driver binding path
- [ ] IOMMU/MSI logs if driver fails

## Firmware Artifacts
- [ ] root port enablement, generation limit, bifurcation, hot-plug, ASPM/L1SS, SR-IOV/ARI/ACS/ATS/PASID if relevant
- [ ] above-4G decoding
- [ ] ACPI dump or running DT
- [ ] MCFG/ECAM/resource windows

## Hardware Measurements
- [ ] endpoint rails
- [ ] REFCLK
- [ ] PERST# timing
- [ ] CLKREQ#/WAKE#/PRSNT# when relevant
- [ ] endpoint straps
- [ ] retimer/redriver mode/config
- [ ] temperature/load condition
- [ ] scope/LA screenshots archived
