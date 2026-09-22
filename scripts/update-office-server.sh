#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_server="office:/home/kairan/MC/GregTech_Leisure_Modified"

ssh office 'python3 -c "import tomllib"'
rsync -a "$gtl_root/gtl-update.py" "$gtl_root/gtl-known-jars.json" "$gtl_root/update-gtl.sh" "$gtl_server/"
rsync -a \
  "$gtl_root/scripts/server-packwiz-update.sh" \
  "$gtl_server/update-pack.sh"
rsync -a \
  "$gtl_root/config/yes_steve_model/built/" \
  "$gtl_server/config/yes_steve_model/built/"
rsync -a \
  "$gtl_root/config/yes_steve_model/custom/" \
  "$gtl_server/config/yes_steve_model/custom/"

ssh office "chmod +x \"\$HOME/MC/GregTech_Leisure_Modified/update-pack.sh\" && \"\$HOME/MC/GregTech_Leisure_Modified/update-pack.sh\""
