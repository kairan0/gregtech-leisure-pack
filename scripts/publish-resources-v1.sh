#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_repo="kairan0/gregtech-leisure-pack"

cd "$gtl_root"
"$gtl_root/scripts/stage-resource-assets.sh"

if gh release view resources-v1 --repo "$gtl_repo" >/dev/null 2>&1; then
  echo "GitHub release resources-v1 already exists; refusing to overwrite immutable assets." >&2
  exit 1
fi

gh release create resources-v1 "$gtl_root"/dist/resources-v1/*.zip \
  --repo "$gtl_repo" \
  --title "GTL client resource assets v1" \
  --notes "Exact SHA-256 pinned local resource and shader packs used by the initial lightweight distribution."
