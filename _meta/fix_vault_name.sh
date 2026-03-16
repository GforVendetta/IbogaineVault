#!/bin/bash
# fix_vault_name.sh — Replace "IbogaineVault" / "IbogaineVault" → "IbogaineVault"
# Covers both /Users/aretesofia/IbogaineVault and IbogaineVault-Tier1
# Skips: .git, .smart-env, .obsidian, binary files
# Safe: "IbogaineVault" doesn't contain "IbogaineVault" — no double-replacement risk

set -euo pipefail

DIRS=("/Users/aretesofia/IbogaineVault" "/Users/aretesofia/IbogaineVault-Tier1")
EXTS=(md yml yaml json txt sh py cff css html js jsx ts)

# Build find -name args
build_name_args() {
  local first=true
  for ext in "${EXTS[@]}"; do
    if $first; then
      echo -n "-name '*.${ext}'"
      first=false
    else
      echo -n " -o -name '*.${ext}'"
    fi
  done
}

echo "=== Scanning for IbogaineVault / IbogaineVault ==="
TOTAL=0
FILES_LIST=()

for dir in "${DIRS[@]}"; do
  [ -d "$dir" ] || continue
  while IFS= read -r f; do
    count=$(grep -c 'IbogaineVault\|IbogaineVault' "$f" 2>/dev/null || true)
    if [ "$count" -gt 0 ]; then
      echo "  [$count] $f"
      TOTAL=$((TOTAL + count))
      FILES_LIST+=("$f")
    fi
  done < <(find "$dir" \( -path '*/.git/*' -o -path '*/.smart-env/*' -o -path '*/.obsidian/*' \) -prune -o -type f \( -name '*.md' -o -name '*.yml' -o -name '*.yaml' -o -name '*.json' -o -name '*.txt' -o -name '*.sh' -o -name '*.py' -o -name '*.cff' -o -name '*.css' -o -name '*.html' -o -name '*.js' -o -name '*.jsx' -o -name '*.ts' \) -print)
done

echo ""
echo "Total matches: $TOTAL across ${#FILES_LIST[@]} files"
[ "$TOTAL" -eq 0 ] && echo "Nothing to fix." && exit 0

echo ""
read -p "Proceed with replacement? (y/n) " confirm
[ "$confirm" != "y" ] && echo "Aborted." && exit 0

echo ""
echo "=== Replacing ==="
FIXED=0
for f in "${FILES_LIST[@]}"; do
  sed -i '' -e 's/IbogaineVault/IbogaineVault/g' -e 's/IbogaineVault/IbogaineVault/g' "$f"
  echo "  Fixed: $f"
  FIXED=$((FIXED + 1))
done

echo ""
echo "=== Verification ==="
for dir in "${DIRS[@]}"; do
  [ -d "$dir" ] || continue
  remaining=$(find "$dir" \( -path '*/.git/*' -o -path '*/.smart-env/*' -o -path '*/.obsidian/*' \) -prune -o -type f \( -name '*.md' -o -name '*.yml' -o -name '*.yaml' -o -name '*.json' -o -name '*.cff' \) -print | xargs grep -l 'IbogaineVault\|IbogaineVault' 2>/dev/null | wc -l | tr -d ' ')
  echo "  $dir: $remaining files still containing IbogaineVault/IbogaineVault"
done
echo ""
echo "Fixed $FIXED files. Done."
