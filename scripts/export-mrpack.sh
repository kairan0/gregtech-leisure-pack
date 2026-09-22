#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_version=$(sed -n 's/^version = "\(.*\)"/\1/p' "$gtl_root/pack.toml" | head -1)
gtl_output_dir="$gtl_root/dist"
gtl_output="$gtl_output_dir/GregTech-Leisure-$gtl_version.mrpack"

mkdir -p "$gtl_output_dir"
cd "$gtl_root"
"${GTL_PYTHON:-python3.11}" scripts/content_policy.py
if [[ "${1:-}" != "--preview" && -n "$(git status --porcelain)" ]]; then
  echo "Refusing release export from a dirty checkout; commit reviewed changes or use --preview." >&2
  exit 1
fi
"${GTL_PYTHON:-python3.11}" -m unittest discover -s scripts/tests -p 'test_*.py'
"$gtl_root/scripts/packwiz-command.sh" refresh
"${GTL_PYTHON:-python3.11}" scripts/content_policy.py
if [[ "${1:-}" != "--preview" && -n "$(git status --porcelain)" ]]; then
  echo "Refresh changed metadata; review and commit it before release export." >&2
  exit 1
fi
"$gtl_root/scripts/packwiz-command.sh" modrinth export --restrictDomains=false -o "$gtl_output"
gtl_check_args=(--bundle)
if [[ -n "${GTL_PAYLOAD_ROOT:-}" ]]; then
  gtl_check_args+=(--payload-root "$GTL_PAYLOAD_ROOT")
fi
"${GTL_PYTHON:-python3.11}" "$gtl_root/scripts/release-check.py" "$gtl_output" "${gtl_check_args[@]}"
shasum -a 256 "$gtl_output"
