#!/bin/bash
set -eu
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
    printf '需要 Python 3.10 或更高版本：https://www.python.org/downloads/macos/\n'
    exit 1
fi
exec python3 ./launch.py "$@"
