#!/usr/bin/env bash
set -euo pipefail
board="${1:-board}"
rev="${2:-rev}"
dir="bringup/$(date +%Y%m%d-%H%M%S)-${board}-${rev}"
mkdir -p "$dir"/{logs,measurements,photos,firmware,notes}
{
  date -Is
  uname -a
  echo "board=$board"
  echo "rev=$rev"
} | tee "$dir/session.txt"
echo "$dir"
