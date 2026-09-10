#!/bin/sh
# Installe les commandes et skills de ce dépôt dans ~/.claude/.
#
#   ./install.sh              copie ; refuse d'écraser un fichier existant
#   ./install.sh --force      écrase
#   ./install.sh --link       liens symboliques vers ce dépôt (suit les mises à jour)
#
# Redémarre Claude Code après : les commandes apparaissent avec /.

set -e

SOURCE="$(cd "$(dirname "$0")" && pwd)"
CIBLE="${CLAUDE_HOME:-$HOME/.claude}"
FORCE=0
LIEN=0

for a in "$@"; do
  case "$a" in
    --force) FORCE=1 ;;
    --link)  LIEN=1 ;;
    -h|--help) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "option inconnue : $a" >&2; exit 1 ;;
  esac
done

mkdir -p "$CIBLE/commands" "$CIBLE/skills"

poser() {
  src="$1"; dst="$2"; nom="$3"
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if [ "$FORCE" -eq 0 ]; then
      echo "  · $nom — existe déjà, ignoré (--force pour écraser)"
      return 0
    fi
    rm -rf "$dst"
  fi
  if [ "$LIEN" -eq 1 ]; then
    ln -s "$src" "$dst"
    echo "  ✓ $nom (lien)"
  else
    cp -R "$src" "$dst"
    echo "  ✓ $nom"
  fi
}

echo "Commandes → $CIBLE/commands/"
for f in "$SOURCE"/commands/*.md; do
  poser "$f" "$CIBLE/commands/$(basename "$f")" "$(basename "$f" .md)"
done

echo "Skills → $CIBLE/skills/"
for d in "$SOURCE"/skills/*/; do
  nom="$(basename "$d")"
  poser "${d%/}" "$CIBLE/skills/$nom" "$nom"
done

# Les deux scripts shell de scan-secrets doivent rester exécutables.
for f in "$CIBLE/skills/scan-secrets/assets/pre-commit" "$CIBLE/skills/scan-secrets/assets/hook-secrets"; do
  [ -f "$f" ] && chmod +x "$f"
done

echo
echo "Terminé. Redémarre Claude Code, puis tape / pour voir les commandes."
if [ -d "$CIBLE/skills/scan-secrets" ]; then
  echo "scan-secrets a besoin de Docker. Pour poser le hook sur un dépôt :"
  echo "  $CIBLE/skills/scan-secrets/assets/hook-secrets poser <dépôt>"
fi
