#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_pack_url="https://kairan0.github.io/gregtech-leisure-pack/pack.toml"
gtl_server="office:/home/kairan/MC/GregTech_Leisure_Modified"

rsync -a \
  "$gtl_root/config/yes_steve_model/built/" \
  "$gtl_server/config/yes_steve_model/built/"
rsync -a \
  "$gtl_root/config/yes_steve_model/custom/" \
  "$gtl_server/config/yes_steve_model/custom/"

ssh office "cd \"\$HOME/MC/GregTech_Leisure_Modified\" && java -jar packwiz-installer-bootstrap.jar -g -s server '$gtl_pack_url'"
