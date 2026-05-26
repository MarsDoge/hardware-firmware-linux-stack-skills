#!/usr/bin/env bash
set -euo pipefail
out="${1:-power-thermal-evidence-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$out"
uname -a > "$out/uname.txt"
cat /proc/cmdline > "$out/cmdline.txt"
dmesg -T > "$out/dmesg.txt"
find /sys/class/thermal -maxdepth 3 -type f -print -exec cat {} \; > "$out/thermal.txt" 2>/dev/null || true
find /sys/class/hwmon -maxdepth 3 -type f -print -exec cat {} \; > "$out/hwmon.txt" 2>/dev/null || true
cat /sys/kernel/debug/regulator/regulator_summary > "$out/regulator_summary.txt" 2>/dev/null || true
cat /sys/kernel/debug/clk/clk_summary > "$out/clk_summary.txt" 2>/dev/null || true
