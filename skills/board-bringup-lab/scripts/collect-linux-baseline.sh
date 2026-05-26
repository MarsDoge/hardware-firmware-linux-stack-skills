#!/usr/bin/env bash
set -euo pipefail
out="${1:-bringup-linux-baseline-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$out"
uname -a > "$out/uname.txt"
cat /proc/cmdline > "$out/cmdline.txt"
dmesg -T > "$out/dmesg.txt"
lsmod > "$out/lsmod.txt"
lspci -nnvv > "$out/lspci.txt" 2>&1 || true
lsusb -t > "$out/lsusb-tree.txt" 2>&1 || true
i2cdetect -l > "$out/i2c-buses.txt" 2>&1 || true
gpioinfo > "$out/gpioinfo.txt" 2>&1 || true
