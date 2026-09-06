#!/usr/bin/env bash
set -euo pipefail

gtl_pack_url="https://kairan0.github.io/gregtech-leisure-pack/pack.toml"

ssh office "cd \"\$HOME/MC/GregTech_Leisure_Modified\" && java -jar packwiz-installer-bootstrap.jar -g -s server '$gtl_pack_url'"
