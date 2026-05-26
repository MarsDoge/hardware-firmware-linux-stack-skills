# ASL Review Checklists

## DSDT / SSDT
- DefinitionBlock fields intentional
- No duplicate namespace definitions unless verified
- Externals resolve with all SSDTs
- Methods have correct args/returns
- OperationRegion/Field definitions match registers
- `iasl` errors fixed; warnings reviewed

## Device Node
- Correct parent scope/bus
- `_HID`/`_CID` match driver or standard
- `_UID` stable and unique
- `_ADR` used for addressable bus children
- `_STA` not accidentally hiding device
- `_DEP` covers providers

## `_CRS`
- MMIO base/size correct
- IRQ flags match wiring
- GPIO polarity/pull/index correct
- I2C/SPI/UART descriptors specify controller/address/speed/mode
- Producer/consumer bits correct
- Resource not hidden in `_DSD`

## `_DSD`
- Correct UUID
- Valid package nesting
- Property names documented by Linux binding/driver
- Types match fwnode reads
- Supplemental data only

## Power / Dependencies
- `_PR0`/`_PR3` reference valid PowerResource objects
- `_PS0`/`_PS3` safe for OS PM
- `_DEP` covers required providers
- Wake methods/resources tested
