# Power / Thermal Reference Map

Use vendor PMIC/regulator datasheets, board schematics, SoC power-management manuals, thermal design guides, Linux regulator/hwmon/thermal framework documentation, ACPI thermal/power resources where applicable, and platform EC/BMC policy documentation.

Do not copy proprietary tables or copyrighted specification text. Cite document name, version, section/table, URL or local path, and the engineering implication.

Key topics:

- Input power source, protection, current limit, inrush, brownout behavior
- Always-on and switched rails, enables, PGOODs, resets, sequencing
- Regulator constraints, consumers, voltage/current limits, mode transitions
- Suspend/resume and runtime PM ownership across firmware, EC/BMC, and Linux
- Thermal sensors, calibration, zone mapping, trip points, cooling devices, fan policy
- Throttling paths: CPUfreq/devfreq, firmware-first policy, hardware thermal shutdown
