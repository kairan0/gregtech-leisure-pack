#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_repo="kairan0/gregtech-leisure-pack"

cd "$gtl_root"
"$gtl_root/scripts/stage-assets-v3.sh"

if gh release view assets-v3 --repo "$gtl_repo" >/dev/null 2>&1; then
  echo "GitHub release assets-v3 already exists; refusing to overwrite immutable assets." >&2
  exit 1
fi

gh release create assets-v3 "$gtl_root"/dist/assets-v3/*.jar \
  --repo "$gtl_repo" \
  --title "GTL custom binary assets v3" \
  --notes "Version-locked ExtendedAE Plus 1.5.5 compatibility build for NeoECO 20.4.2 C4 virtual crafting completion. Source commit: 6ac52c5f."
