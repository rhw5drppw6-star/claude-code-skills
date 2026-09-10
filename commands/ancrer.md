---
description: Consigne dans le CLAUDE.md du projet les règles durables apprises pendant la session
argument-hint: [règle précise à ancrer, optionnel]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Mets à jour (ou crée) le fichier `CLAUDE.md` à la racine du dépôt courant.

$ARGUMENTS

**Distinction fondamentale — n'ancre que le DURABLE :**

| Va dans CLAUDE.md | Va dans /checkpoint |
|---|---|
| Comment lancer les tests, le build, le serveur | Où j'en suis dans la tâche |
| Conventions de code du projet, style imposé | Ce que j'essaie en ce moment |
| Fichiers générés / à ne jamais éditer à la main | L'impasse rencontrée aujourd'hui |
| Architecture : où vit quoi | La prochaine ligne à écrire |
| Pièges connus du dépôt, contraintes d'environnement | L'état des tests à cet instant |

Autrement dit : ce qui sera **encore vrai dans trois mois**.

**Méthode :**
1. Lis le `CLAUDE.md` existant s'il y en a un. Ne l'écrase jamais : fusionne.
   Une règle déjà présente ne se réécrit pas ; une règle devenue fausse se corrige.
2. Reprends notre session et retiens uniquement ce qui est durable : ce que j'ai
   corrigé chez toi, les commandes qu'on a fini par trouver, les pièges découverts,
   les conventions que tu as dû déduire.
3. Vérifie chaque affirmation contre le dépôt avant de l'écrire. Un chemin, une
   commande ou un nom de script doit exister réellement — teste-le si c'est rapide.
4. Écris court et impératif. Pas de prose, pas de « il est recommandé de ».
   « Les tests : `pytest -q tests/`. Ne pas lancer pytest à la racine, ça scanne venv/. »
5. N'ancre rien qui soit déjà évident à la lecture du code ou du README.

Termine en me montrant **uniquement le diff** de ce que tu as ajouté ou modifié,
pour que je valide.
