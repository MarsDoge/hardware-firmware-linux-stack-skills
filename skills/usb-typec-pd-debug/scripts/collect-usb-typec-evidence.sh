#!/usr/bin/env bash
set -euo pipefail
out="${1:-usb-typec-evidence-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$out"
uname -a > "$out/uname.txt"
cat /proc/cmdline > "$out/cmdline.txt"
dmesg -T > "$out/dmesg.txt"
lsusb > "$out/lsusb.txt" 2>&1 || true
lsusb -t > "$out/lsusb-tree.txt" 2>&1 || true
find /sys/class/typec -maxdepth 4 -type f -print -exec cat {} \; > "$out/typec-sysfs.txt" 2>/dev/null || true
