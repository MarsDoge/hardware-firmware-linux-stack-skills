# PCIe Spec and Standards Map

Use authoritative references without copying copyrighted text.

## Official Sources

- PCI-SIG specifications: https://pcisig.com/specifications
  - PCI Express Base Specification
  - PCI Express Card Electromechanical Specification
  - ECNs and engineering change notices
- UEFI Forum specifications: https://uefi.org/specifications
  - ACPI specification for MCFG, `_CRS`, `_OSC`, `_PRT`, resources
  - UEFI specification for firmware/OS handoff context
- Linux PCI docs: https://docs.kernel.org/PCI/
- Kernel source under test: `drivers/pci/`, `Documentation/PCI/`, `Documentation/devicetree/bindings/pci/`

## Engineering Map

| Topic | Reference | Engineering Use |
| --- | --- | --- |
| LTSSM/link training | PCIe Base | No-link and wrong-speed triage |
| Config space/capabilities | PCIe Base | `lspci -vvxxxx` and capability interpretation |
| AER/DPC | PCIe Base | Error class triage |
| ASPM/L1SS/PME | PCIe Base + platform docs | Power management debug |
| Add-in card timing | PCIe CEM | PERST#, REFCLK, connector implications |
| Firmware resource handoff | ACPI/UEFI | MCFG, `_CRS`, `_OSC`, bridge windows |
| Linux enumeration | Linux PCI docs/source | Link/config/BAR/MSI/driver distinction |

## Citation Template

```text
Reference:
Version:
Section/table:
URL/path:
Summary in own words:
Decision supported:
Evidence collected:
```

Allowed: official links, section/table pointers, original summaries. Avoid: copied spec paragraphs/tables or member-only text.
