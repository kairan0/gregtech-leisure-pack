#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_output="$gtl_root/dist/assets-v1"
mkdir -p "$gtl_output"

cp "$gtl_root/mods/Cell4-1.20.1-1.0.3+datapack-0.0.1.jar" "$gtl_output/cell4-1.20.1-1.0.3-datapack-0.0.1.jar"
cp "$gtl_root/mods/GTMAdvancedHatch-1.20.1-0.1.10 fix2.jar" "$gtl_output/gtmadvancedhatch-1.20.1-0.1.10-fix2.jar"
cp "$gtl_root/mods/WorldComment-0.3.2+1.20.1.jar" "$gtl_output/worldcomment-0.3.2-1.20.1.jar"
cp "$gtl_root/mods/[Custom-亚空间]gtladditions-3.2Custom_SubSpace.jar" "$gtl_output/gtladditions-3.2-custom-subspace.jar"
cp "$gtl_root/mods/[化学结构式显示]gtmoldraw-1.2coldfix1.jar" "$gtl_output/gtmoldraw-1.2-coldfix1.jar"
cp "$gtl_root/mods/ae2lt-forge-1.20.1-2.1.0-beta.3-gtlcore-compat.2.jar" "$gtl_output/ae2lt-forge-1.20.1-2.1.0-beta.3-gtlcore-compat.2.jar"
cp "$gtl_root/mods/extendedae_plus_gtladd-1.0.2.jar" "$gtl_output/extendedae-plus-gtladd-1.0.2.jar"
cp "$gtl_root/mods/gtl_extend-3.2.1-NoPlanetaryEngine-pre1.jar" "$gtl_output/gtl-extend-3.2.1-no-planetary-engine-pre1.jar"
cp "$gtl_root/mods/gtlcore-1.2.3.1-fix1.jar" "$gtl_output/gtlcore-1.2.3.1-fix1.jar"
cp "$gtl_root/mods/gtmthings-1.3.5.b.jar" "$gtl_output/gtmthings-1.3.5.b.jar"
cp "$gtl_root/mods/openysm-forge-2.6.6.6.jar" "$gtl_output/openysm-forge-2.6.6.6.jar"
cp "$gtl_root/mods/thunderbolt-forge-1.20.1-2.0.0-beta.3-gtlcore-compat.2.jar" "$gtl_output/thunderbolt-forge-1.20.1-2.0.0-beta.3-gtlcore-compat.2.jar"
cp "$gtl_root/mods/voicechat-forge-1.20.1-2.6.23.jar" "$gtl_output/voicechat-forge-1.20.1-2.6.23.jar"
cp "$gtl_root/mods/wildcard_pattern-0.1.2-gtl-ae2lt-compat.4.jar" "$gtl_output/wildcard-pattern-0.1.2-gtl-ae2lt-compat.4.jar"

shasum -a 256 "$gtl_output"/*.jar
