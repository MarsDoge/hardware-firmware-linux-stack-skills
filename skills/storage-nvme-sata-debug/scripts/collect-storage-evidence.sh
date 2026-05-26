#!/usr/bin/env bash
set -euo pipefail
out="${1:-storage-evidence-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$out"
uname -a > "$out/uname.txt"
cat /proc/cmdline > "$out/cmdline.txt"
dmesg -T > "$out/dmesg.txt"
lsblk -o NAME,MODEL,SERIAL,SIZE,TYPE,FSTYPE,MOUNTPOINTS > "$out/lsblk.txt" 2>&1 || true
blkid > "$out/blkid.txt" 2>&1 || true
nvme list > "$out/nvme-list.txt" 2>&1 || true
smartctl --scan > "$out/smart-scan.txt" 2>&1 || true
