#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

if [[ -x "$gtl_root/.tools/packwiz" ]]; then
  exec "$gtl_root/.tools/packwiz" "$@"
fi

if command -v packwiz >/dev/null 2>&1; then
  exec packwiz "$@"
fi

echo "packwiz not found: place it at $gtl_root/.tools/packwiz or install it in PATH" >&2
exit 127
