# Board Bring-Up Failure Patterns

- No current draw: input path, fuse, switch, connector, enable missing.
- Excess current: short, reversed part, wrong rail, solder bridge, damaged IC.
- Rails good, reset held: PMIC PGOOD, supervisor threshold, reset pull, firmware-controlled enable.
- Reset releases, no UART: wrong boot mode, dead clock, UART mux/pinout/baud, ROM not executing.
- Firmware starts, DRAM fails: DDR power/clock/reset, topology, training config, wrong memory part.
- Bootloader starts, kernel fails: image format, DT/ACPI, bootargs, storage/rootfs, memory map.
- Intermittent boot: ramp timing, reset race, marginal clock, brownout, temperature, uninitialized strap.
