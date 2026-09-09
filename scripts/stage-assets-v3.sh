#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_output="$gtl_root/dist/assets-v3"
gtl_asset="extendedae_plus-1.5.5-neoeco-compat.1.jar"
gtl_sha256="cd47512a8b79cea991ba83191f9681d934b5803752ddb0d6630abdd081253078"

mkdir -p "$gtl_output"
cp "$gtl_root/mods/$gtl_asset" "$gtl_output/$gtl_asset"
echo "$gtl_sha256  $gtl_output/$gtl_asset" | shasum -a 256 -c -
