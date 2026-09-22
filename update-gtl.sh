#!/usr/bin/env bash
set -euo pipefail
gtl_root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
if [[ -z "${GTL_PYTHON:-}" ]]; then
  for gtl_candidate in python3 python3.14 python3.13 python3.12 python3.11; do
    if command -v "$gtl_candidate" >/dev/null && "$gtl_candidate" -c 'import tomllib' 2>/dev/null; then
      GTL_PYTHON="$gtl_candidate"
      break
    fi
  done
fi
if [[ -z "${GTL_PYTHON:-}" ]]; then
  echo "The verified updater needs Python 3.11+ (game itself only needs Java 17)." >&2
  exit 1
fi
exec "$GTL_PYTHON" "$gtl_root/gtl-update.py" --java "${GTL_JAVA:-java}" "$@"
