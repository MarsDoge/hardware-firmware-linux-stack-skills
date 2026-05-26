# Bring-Up Command Recipes

## Start Session
```bash
BRINGUP_DIR="bringup/$(date +%Y%m%d-%H%M%S)-board"
mkdir -p "$BRINGUP_DIR"/{logs,measurements,firmware,notes}
date -Is | tee "$BRINGUP_DIR/session.txt"
```

## Serial Capture
```bash
script -f "$BRINGUP_DIR/logs/serial.log"
sudo picocom -b 115200 /dev/ttyUSB0
```

## Linux Baseline
```bash
uname -a
cat /proc/cmdline
dmesg -T
lsmod
lspci -nnvv
lsusb -t
i2cdetect -l
```

## Firmware Readback
```bash
sha256sum firmware.bin
sudo flashrom -p <programmer> -r readback.bin
sha256sum readback.bin
```
