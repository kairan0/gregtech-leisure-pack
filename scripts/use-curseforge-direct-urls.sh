#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_tmp=$(mktemp -d "${TMPDIR:-/tmp}/gtl-curseforge.XXXXXX")
gtl_map="$gtl_tmp/urls.tsv"

cleanup() {
  rm -rf "$gtl_tmp"
}
trap cleanup EXIT

read_toml_string() {
  local gtl_key=$1
  local gtl_file=$2
  sed -n "s/^${gtl_key} = \"\(.*\)\"$/\1/p" "$gtl_file" | head -1
}

read_toml_integer() {
  local gtl_key=$1
  local gtl_file=$2
  sed -n "s/^${gtl_key} = \([0-9][0-9]*\)$/\1/p" "$gtl_file" | head -1
}

touch "$gtl_map"
for gtl_meta in "$gtl_root"/mods/*.pw.toml; do
  if ! grep -q '^\[update\.curseforge\]$' "$gtl_meta"; then
    continue
  fi

  gtl_filename=$(read_toml_string filename "$gtl_meta")
  gtl_file_id=$(read_toml_integer file-id "$gtl_meta")
  if [[ -z "$gtl_filename" || -z "$gtl_file_id" ]]; then
    echo "Incomplete CurseForge metadata: $gtl_meta" >&2
    exit 1
  fi

  gtl_group=$((gtl_file_id / 1000))
  printf -v gtl_tail '%03d' "$((gtl_file_id % 1000))"
  gtl_encoded=$(jq -nr --arg value "$gtl_filename" '$value | @uri')
  gtl_url="https://edge.forgecdn.net/files/$gtl_group/$gtl_tail/$gtl_encoded"
  printf '%s\t%s\n' "$gtl_meta" "$gtl_url" >> "$gtl_map"
done

while IFS=$'\t' read -r gtl_meta gtl_url; do
  curl --fail --silent --show-error --location --head \
    --retry 2 --retry-all-errors \
    --header 'User-Agent: kairan0/gregtech-leisure-pack' \
    "$gtl_url" >/dev/null
  printf 'CurseForge URL verified: %s\n' "$(read_toml_string filename "$gtl_meta")"
done < "$gtl_map"

gtl_converted=0
while IFS=$'\t' read -r gtl_meta gtl_url; do
  gtl_name=$(read_toml_string name "$gtl_meta")
  gtl_filename=$(read_toml_string filename "$gtl_meta")
  gtl_side=$(read_toml_string side "$gtl_meta")
  gtl_hash_format=$(read_toml_string hash-format "$gtl_meta")
  gtl_hash=$(read_toml_string hash "$gtl_meta")
  gtl_file_id=$(read_toml_integer file-id "$gtl_meta")
  gtl_project_id=$(read_toml_integer project-id "$gtl_meta")
  gtl_new="$gtl_tmp/$(basename "$gtl_meta")"

  {
    printf 'name = "%s"\n' "$gtl_name"
    printf 'filename = "%s"\n' "$gtl_filename"
    printf 'side = "%s"\n\n' "$gtl_side"
    printf '[download]\n'
    printf 'hash-format = "%s"\n' "$gtl_hash_format"
    printf 'hash = "%s"\n' "$gtl_hash"
    printf 'mode = "url"\n'
    printf 'url = "%s"\n\n' "$gtl_url"
    printf '[update]\n'
    printf '[update.curseforge]\n'
    printf 'file-id = %s\n' "$gtl_file_id"
    printf 'project-id = %s\n' "$gtl_project_id"
  } > "$gtl_new"
  mv "$gtl_new" "$gtl_meta"
  gtl_converted=$((gtl_converted + 1))
done < "$gtl_map"

"$gtl_root/scripts/packwiz-command.sh" refresh
printf 'Converted %d CurseForge entries to verified direct CDN URLs.\n' "$gtl_converted"
