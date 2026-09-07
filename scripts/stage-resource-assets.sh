#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_output="$gtl_root/dist/resources-v1"
mkdir -p "$gtl_output"

cp "$gtl_root/resourcepacks/产线摧毁者附带材质.zip" "$gtl_output/production-destroyer-textures.zip"
cp "$gtl_root/resourcepacks/[适配GTL＆GTO]AE亮色UI-3.5fix(0.5.4)多模组覆盖⚠大量修改资源 与其他AE材质不能混合使用 .zip" "$gtl_output/ae-bright-ui-gtl-gto-3.5-fix.zip"
cp "$gtl_root/resourcepacks/GToTextureBackportGTLv3.0coldfix.zip" "$gtl_output/gto-texture-backport-gtl-v3.0-coldfix.zip"
cp "$gtl_root/resourcepacks/Pretty_Pipez_1_20_0-1.zip" "$gtl_output/pretty-pipez-1.20.0-1.zip"
cp "$gtl_root/resourcepacks/GT-PBR.zip" "$gtl_output/gt-pbr.zip"
cp "$gtl_root/shaderpacks/photon-main.zip" "$gtl_output/photon-main.zip"

shasum -a 256 "$gtl_output"/*.zip
