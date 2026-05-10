#!/usr/bin/env bash
# Fail if any docs.json navigation page slug has no matching .mdx at repo root (docs/).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if ! command -v jq >/dev/null 2>&1; then
  echo "check_nav_pages: jq is required" >&2
  exit 2
fi
missing=0
while IFS= read -r page; do
  case "$page" in
    ""|"null") continue ;;
  esac
  if [[ ! -f "${page}.mdx" ]]; then
    echo "MISSING MDX for nav page: ${page}.mdx" >&2
    missing=1
  fi
done < <(jq -r '.navigation.tabs[] | .groups[]? | .pages[]?' docs.json)
exit "$missing"
