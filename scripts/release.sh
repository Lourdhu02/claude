#!/usr/bin/env bash
# release.sh — cut a monthly GitHub release from the CHANGELOG.
#
# Usage:
#   ./scripts/release.sh                    # tags + pushes + creates the release
#   ./scripts/release.sh --dry-run         # show what it would do, without pushing
#   ./scripts/release.sh --version 2026-09 # use a specific tag instead of today
#
# What it does:
#   1. Looks for the "## [Unreleased]" section in CHANGELOG.md.
#   2. If empty → exits with a note (nothing to release).
#   3. Otherwise → cuts a tag like 2026-09-01, pushes it, and creates a
#      GitHub Release whose body is the Unreleased section + header.
#
# Before running manually for the first time, authenticate gh:
#   gh auth login
#
# The scheduled GitHub Actions workflow (.github/workflows/monthly-release.yml)
# does the same thing automatically on the 1st of each month.

set -euo pipefail

DRY_RUN=false
VERSION=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --version)
      VERSION="$2"; shift 2
      ;;
    *)
      echo "Unknown flag: $1" >&2
      echo "Usage: $0 [--dry-run] [--version YYYY-MM-DD]" >&2
      exit 1
      ;;
  esac
done

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

CHANGELOG="CHANGELOG.md"
if [[ ! -f "$CHANGELOG" ]]; then
  echo "CHANGELOG.md not found in $ROOT_DIR" >&2
  exit 1
fi

# --- 1. Extract the "Unreleased" section -----------------------------------

UNRELEASED=$(awk '
  /^## \[Unreleased\]/ { in_section=1; next }
  /^## \[/ { in_section=0 }
  in_section { print }
' "$CHANGELOG" | sed '/^$/d')

if [[ -z "$UNRELEASED" ]]; then
  echo "Nothing in the Unreleased section — nothing to release."
  echo "Add changes under '## [Unreleased]' in CHANGELOG.md first."
  exit 0
fi

# --- 2. Determine the tag ---------------------------------------------------

if [[ -n "$VERSION" ]]; then
  TAG="$VERSION"
else
  TAG=$(date -u +"%Y-%m-%d")
fi

TITLE="Claude course — $(date -u +"%B %Y")"
NOTES_FILE=$(mktemp)
trap 'rm -f "$NOTES_FILE"' EXIT

{
  echo "## What's new — $TAG"
  echo ""
  echo "$UNRELEASED"
  echo ""
  echo "---"
  echo ""
  echo "_Automatically generated from [CHANGELOG.md](../CHANGELOG.md)._"
} > "$NOTES_FILE"

if [[ "$DRY_RUN" == true ]]; then
  echo "=== DRY RUN ==="
  echo "Tag      : $TAG"
  echo "Title    : $TITLE"
  echo "Notes    : $NOTES_FILE"
  echo ""
  echo "Release notes preview:"
  echo "---"
  cat "$NOTES_FILE"
  echo "---"
  echo ""
  echo "Would run:"
  echo "  git tag -a $TAG -m 'Release $TAG'"
  echo "  git push origin $TAG"
  echo "  gh release create $TAG --title '$TITLE' --notes-file $NOTES_FILE --verify-tag"
  exit 0
fi

# --- 3. Tag, push, release -------------------------------------------------

echo "Cutting release $TAG …"

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

git tag -a "$TAG" -m "Release $TAG"
git push origin "$TAG"

gh release create "$TAG" \
  --title "$TITLE" \
  --notes-file "$NOTES_FILE" \
  --verify-tag

echo ""
echo "Released: https://github.com/Lourdhu02/claude/releases/tag/$TAG"

# --- 4. Post-release: keep the changelog tidy -------------------------------
# (Optional) Move the just-released "Unreleased" content to a dated section
# so the next month starts fresh. Uncomment if you want this script to also
# update CHANGELOG.md for you on every run.
#
# echo ""
# echo "Updating CHANGELOG.md …"
# python - <<'PY'
# import re, sys, datetime
# path = "CHANGELOG.md"
# text = open(path).read()
# today = datetime.date.today().strftime("%Y-%m-%d")
# # Wrap released content under a new dated heading right after [Unreleased]
# dated = f"## [{today}]\n\n{text.split('## [Unreleased]')[1].split('## [')[0]}"
# text = text.replace("## [Unreleased]", dated, 1)
# open(path, "w").write(text)
# print("CHANGELOG.md updated — new section: ## [%s]" % today)
# PY
