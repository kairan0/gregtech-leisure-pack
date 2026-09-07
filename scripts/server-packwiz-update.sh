#!/usr/bin/env bash
set -euo pipefail

gtl_server_root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
gtl_pack_url="https://kairan0.github.io/gregtech-leisure-pack/pack.toml"
gtl_bootstrap="$gtl_server_root/packwiz-installer-bootstrap.jar"
gtl_bootstrap_url="https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar"
gtl_bootstrap_sha256="a8fbb24dc604278e97f4688e82d3d91a318b98efc08d5dbfcbcbcab6443d116c"

gtl_current_sha256=""
if [[ -f "$gtl_bootstrap" ]]; then
  gtl_current_sha256=$(sha256sum "$gtl_bootstrap" | awk '{print $1}')
fi

if [[ "$gtl_current_sha256" != "$gtl_bootstrap_sha256" ]]; then
  gtl_bootstrap_tmp=$(mktemp "$gtl_server_root/.packwiz-installer-bootstrap.XXXXXX")
  trap 'rm -f "$gtl_bootstrap_tmp"' EXIT
  curl -fL --retry 3 -o "$gtl_bootstrap_tmp" "$gtl_bootstrap_url"
  echo "$gtl_bootstrap_sha256  $gtl_bootstrap_tmp" | sha256sum -c -
  mv "$gtl_bootstrap_tmp" "$gtl_bootstrap"
  trap - EXIT
fi

cd "$gtl_server_root"
java -jar "$gtl_bootstrap" -g -s server "$gtl_pack_url"
