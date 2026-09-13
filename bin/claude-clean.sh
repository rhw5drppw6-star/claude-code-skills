#!/usr/bin/env bash
#
# claude-clean.sh — Boucle "checkpoint" pour Claude Code.
#
# Lance Claude Code. Quand la session se termine, si la commande /checkpoint a
# déposé un fichier _clear_trigger.txt dans le dossier courant, le script relance
# Claude dans une session NEUVE en lui injectant ce fichier comme prompt initial.
#
# Usage :  cl                 (dans le dossier du projet)
#          cl --model opus    (les arguments sont passés au premier lancement)

set -uo pipefail

TRIGGER="_clear_trigger.txt"
ARCHIVE_DIR=".claude/checkpoints"
CYCLE=0

# Sécurité : on ne repart jamais sur un trigger périmé laissé par une session passée.
if [ -f "$TRIGGER" ]; then
  printf '\033[33m[claude-clean] Un %s existe déjà, il est archivé et ignoré.\033[0m\n' "$TRIGGER"
  mkdir -p "$ARCHIVE_DIR"
  mv "$TRIGGER" "$ARCHIVE_DIR/stale-$(date +%Y%m%d-%H%M%S).txt"
fi

claude "$@"

while [ -f "$TRIGGER" ]; do
  CYCLE=$((CYCLE + 1))
  PROMPT="$(cat "$TRIGGER")"

  if [ -z "${PROMPT//[[:space:]]/}" ]; then
    printf '\033[33m[claude-clean] %s est vide, arrêt.\033[0m\n' "$TRIGGER"
    rm -f "$TRIGGER"
    break
  fi

  # On archive plutôt que de supprimer : le fil des checkpoints reste relisible.
  mkdir -p "$ARCHIVE_DIR"
  mv "$TRIGGER" "$ARCHIVE_DIR/$(date +%Y%m%d-%H%M%S).txt"

  printf '\n\033[36m[claude-clean] Checkpoint #%d — nouvelle session avec contexte propre.\033[0m\n' "$CYCLE"
  printf '\033[2m(Ctrl+C maintenant pour interrompre la boucle)\033[0m\n\n'

  claude "$PROMPT"
done

printf '\n\033[32m[claude-clean] Terminé (%d checkpoint(s)).\033[0m\n' "$CYCLE"
