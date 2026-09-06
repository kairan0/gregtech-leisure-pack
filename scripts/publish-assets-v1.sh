#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_repo="kairan0/gregtech-leisure-pack"

cd "$gtl_root"
"$gtl_root/scripts/stage-custom-assets.sh"

if gh release view assets-v1 --repo "$gtl_repo" >/dev/null 2>&1; then
  echo "GitHub release assets-v1 already exists; refusing to overwrite immutable assets." >&2
  exit 1
fi

gh release create assets-v1 "$gtl_root"/dist/assets-v1/*.jar \
  --repo "$gtl_repo" \
  --title "GTL custom binary assets v1" \
  --notes "Exact SHA-256 pinned custom and compatibility JARs required by the initial packwiz release."
