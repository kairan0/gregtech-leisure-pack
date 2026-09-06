#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_version=$(sed -n 's/^version = "\(.*\)"/\1/p' "$gtl_root/pack.toml" | head -1)
gtl_tag="v$gtl_version"
gtl_mrpack="$gtl_root/dist/GregTech-Leisure-$gtl_version.mrpack"

cd "$gtl_root"
if ! gh release view assets-v1 --repo kairan0/gregtech-leisure-pack >/dev/null 2>&1; then
  echo "Required GitHub release assets-v1 does not exist; run scripts/publish-assets-v1.sh first." >&2
  exit 1
fi

"$gtl_root/scripts/export-mrpack.sh"

if [[ -n "$(git status --short)" ]]; then
  echo "Commit and push the refreshed pack metadata before publishing." >&2
  exit 1
fi

git push origin main
gh release create "$gtl_tag" "$gtl_mrpack" \
  --repo kairan0/gregtech-leisure-pack \
  --title "GregTech Leisure $gtl_version" \
  --notes-file CHANGELOG.md
"$gtl_root/scripts/update-office-server.sh"
