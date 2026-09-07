#!/usr/bin/env bash
set -euo pipefail

gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gtl_api="https://api.modrinth.com/v2/version_files"
gtl_tmp=$(mktemp -d "${TMPDIR:-/tmp}/gtl-modrinth.XXXXXX")

cleanup() {
  rm -rf "$gtl_tmp"
}
trap cleanup EXIT

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

read_toml_string() {
  local gtl_key=$1
  local gtl_file=$2
  sed -n "s/^${gtl_key} = \"\(.*\)\"$/\1/p" "$gtl_file" | head -1
}

require_command curl
require_command jq
require_command shasum

gtl_hashes="$gtl_tmp/hashes.txt"
gtl_request="$gtl_tmp/request.json"
gtl_response="$gtl_tmp/response.json"
touch "$gtl_hashes"

for gtl_meta in "$gtl_root"/mods/*.pw.toml; do
  gtl_filename=$(read_toml_string filename "$gtl_meta")
  gtl_jar="$gtl_root/mods/$gtl_filename"
  if [[ ! -f "$gtl_jar" ]]; then
    echo "Metadata payload is not active locally: $gtl_filename" >&2
    exit 1
  fi
  shasum -a 512 "$gtl_jar" | awk '{print $1}' >> "$gtl_hashes"
done

jq -R -s '{hashes:(split("\n") | map(select(length > 0))), algorithm:"sha512"}' \
  "$gtl_hashes" > "$gtl_request"

curl --fail --silent --show-error \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: kairan0/gregtech-leisure-pack' \
  --data-binary "@$gtl_request" \
  --output "$gtl_response" \
  "$gtl_api"

gtl_migrated=0
for gtl_meta in "$gtl_root"/mods/*.pw.toml; do
  gtl_name=$(read_toml_string name "$gtl_meta")
  gtl_filename=$(read_toml_string filename "$gtl_meta")
  gtl_side=$(read_toml_string side "$gtl_meta")
  gtl_hash=$(shasum -a 512 "$gtl_root/mods/$gtl_filename" | awk '{print $1}')

  if ! jq -e --arg h "$gtl_hash" 'has($h)' "$gtl_response" >/dev/null; then
    continue
  fi

  gtl_project=$(jq -r --arg h "$gtl_hash" '.[$h].project_id' "$gtl_response")
  gtl_version=$(jq -r --arg h "$gtl_hash" '.[$h].id' "$gtl_response")
  gtl_url=$(jq -r --arg h "$gtl_hash" \
    '.[$h].files[] | select(.hashes.sha512 == $h) | .url' "$gtl_response" | head -1)
  if [[ -z "$gtl_url" ]]; then
    echo "Modrinth response has no file URL for $gtl_filename" >&2
    exit 1
  fi

  gtl_new="$gtl_tmp/$(basename "$gtl_meta")"
  {
    printf 'name = "%s"\n' "$gtl_name"
    printf 'filename = "%s"\n' "$gtl_filename"
    printf 'side = "%s"\n\n' "$gtl_side"
    printf '[download]\n'
    printf 'hash-format = "sha512"\n'
    printf 'hash = "%s"\n' "$gtl_hash"
    printf 'mode = "url"\n'
    printf 'url = "%s"\n\n' "$gtl_url"
    printf '[update]\n'
    printf '[update.modrinth]\n'
    printf 'mod-id = "%s"\n' "$gtl_project"
    printf 'version = "%s"\n' "$gtl_version"
  } > "$gtl_new"
  mv "$gtl_new" "$gtl_meta"
  printf 'Modrinth exact match: %s\n' "$gtl_filename"
  gtl_migrated=$((gtl_migrated + 1))
done

"$gtl_root/scripts/packwiz-command.sh" refresh
printf 'Migrated %d exact SHA-512 matches to Modrinth metadata.\n' "$gtl_migrated"
