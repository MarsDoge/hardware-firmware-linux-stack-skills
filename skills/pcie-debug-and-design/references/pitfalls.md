# PCIe Pitfalls

1. PERST# timing not scoped: scope rails, REFCLK, PERST# from cold power-on.
2. REFCLK assumed good because oscillator is populated: verify at endpoint/connector and clocking architecture.
3. Lane map mismatch hidden by lower-width training: compare schematic, bifurcation, endpoint expectations, `LnkSta`.
4. Retimer/redriver not configured: check straps, I2C config, EEPROM, reset sequencing.
5. Cable/riser treated as transparent: remove or replace with generation-rated known-good part.
6. Root port disabled or bifurcated incorrectly: record BIOS setup and platform policy.
7. Resource windows too small: inspect ACPI `_CRS`, bridge windows, above-4G.
8. Bad MCFG/ECAM: compare ACPI table to platform memory map.
9. `_OSC` ownership mismatch: inspect ACPI logs and firmware policy.
10. AER treated as root cause: decode class and find first failing layer.
11. `pcie_aspm=off` used as final fix: use only to isolate ASPM/CLKREQ#/L1SS.
12. Gen1 forced and declared success: proves basic connectivity, not design margin.
