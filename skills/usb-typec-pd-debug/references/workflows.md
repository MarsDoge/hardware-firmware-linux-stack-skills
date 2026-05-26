# USB Type-C / PD Workflows

## No enumeration
Check VBUS, CC attach, orientation, port role, reset/clock/PHY, dmesg, lsusb, controller driver, DT/ACPI resources.

## PD negotiation failure
Capture PD analyzer trace if available, CC voltages, source/sink caps, cable e-marker, policy engine logs, tcpm/ucsi logs.

## SuperSpeed failure
Check USB2 vs USB3 distinction, mux orientation, retimer config, lane polarity, equalization, cable rating.
