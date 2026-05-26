# BMC/EC Pitfalls

1. Ignoring ownership: host, BMC, EC, PMIC, and CPLD may all touch the same signal.
2. Trusting sensor names without physical mapping.
3. Debugging host only when BMC holds reset/power.
4. Updating BMC firmware without recovery path.
5. Confusing IPMI/Redfish service bug with board-level signal failure.
