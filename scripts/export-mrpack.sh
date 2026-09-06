#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_version=$(sed -n 's/^version = "\(.*\)"/\1/p' "$gtl_root/pack.toml" | head -1)
gtl_output_dir="$gtl_root/dist"
gtl_output="$gtl_output_dir/GregTech-Leisure-$gtl_version.mrpack"

mkdir -p "$gtl_output_dir"
cd "$gtl_root"
"$gtl_root/scripts/packwiz-command.sh" refresh
"$gtl_root/scripts/packwiz-command.sh" modrinth export -o "$gtl_output"
shasum -a 256 "$gtl_output"
