#!/usr/bin/env bash
set -euo pipefail

gtl_server_root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
exec bash "$gtl_server_root/update-gtl.sh" --side server "$@"
