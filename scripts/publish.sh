#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_version=$(sed -n 's/^version = "\(.*\)"/\1/p' "$gtl_root/pack.toml" | head -1)
gtl_tag="v$gtl_version"
gtl_mrpack="$gtl_root/dist/GregTech-Leisure-$gtl_version.mrpack"
gtl_repo="kairan0/gregtech-leisure-pack"

cd "$gtl_root"
if ! gh release view assets-v1 --repo kairan0/gregtech-leisure-pack >/dev/null 2>&1; then
  echo "Required GitHub release assets-v1 does not exist; run scripts/publish-assets-v1.sh first." >&2
  exit 1
fi
if ! gh release view resources-v1 --repo kairan0/gregtech-leisure-pack >/dev/null 2>&1; then
  echo "Required GitHub release resources-v1 does not exist; run scripts/publish-resources-v1.sh first." >&2
  exit 1
fi

"$gtl_root/scripts/export-mrpack.sh"

if [[ -n "$(git status --short)" ]]; then
  echo "Commit and push the refreshed pack metadata before publishing." >&2
  exit 1
fi

git push origin main
# Pages must serve the exact reviewed source, not merely report git push success.
"${GTL_PYTHON:-python3.11}" scripts/release-check.py "$gtl_mrpack" --public
gtl_commit=$(git rev-parse HEAD)
gtl_main=$(git ls-remote origin refs/heads/main | cut -f1)
if [[ "$gtl_commit" != "$gtl_main" ]]; then
  echo "HEAD is not published main; aborting release." >&2
  exit 1
fi
gh release create "$gtl_tag" "$gtl_mrpack" --draft --target "$gtl_commit" \
  --repo "$gtl_repo" \
  --title "GregTech Leisure $gtl_version" \
  --notes-file CHANGELOG.md
gtl_verify_dir=$(mktemp -d "$gtl_root/dist/release-download.XXXXXX")
gh release download "$gtl_tag" --repo "$gtl_repo" --pattern "$(basename "$gtl_mrpack")" --dir "$gtl_verify_dir"
cmp "$gtl_mrpack" "$gtl_verify_dir/$(basename "$gtl_mrpack")"
gh release edit "$gtl_tag" --repo "$gtl_repo" --draft=false --latest
echo "Client release verified and published. Server deployment is a separate explicit step."
