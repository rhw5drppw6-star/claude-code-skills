---
name: scan-secrets
description: >-
  Scanne le répertoire de travail et l'historique Git avec TruffleHog (exécuté dans Docker)
  pour intercepter les fuites de secrets, en appliquant les exclusions du projet. À utiliser
  avant tout commit ou push, lors d'un audit de sécurité, après avoir fusionné une branche
  distante, et chaque fois qu'un identifiant, un token ou une clé apparaît dans le code.
---

# Audit de secrets — système de fichiers et historique Git

## Directives

1. **Validation pré-commit.** Avant d'exécuter ou de suggérer un `git commit`, lance le scan
   `filesystem`. Sans exception.
2. **Audit d'historique.** À la demande, ou après l'intégration d'une branche distante, lance
   le scan `git`.
3. **Blocage.** Un secret détecté et non exclu **arrête le flux de travail**. Aucun commit,
   aucun push, aucun contournement. Tu annonces le blocage, tu ne le négocies pas.
4. **Remédiation** — dans cet ordre, jamais l'inverse :
   - **Secret réel** → fais-le **révoquer d'abord**. Un secret qui a existé dans un dépôt est
     compromis, que l'historique soit nettoyé ensuite ou non. Le nettoyage (`git filter-repo`,
     BFG) vient après, il réécrit l'historique et exige une force-push : c'est une décision
     humaine, tu la proposes, tu ne l'exécutes pas seul.
   - **Faux positif** (fixture, clé de test publique, exemple de documentation) → ajoute son
     chemin aux exclusions : `references/exclusions.md` donne le format exact, qui n'est pas
     celui qu'on croit.

## Les commandes

Image officielle — **`trufflesecurity/trufflehog`**. Toute autre image est un tiers non vérifié
à qui tu montes le dépôt entier.

```bash
# Scan du code présent sur le disque
docker run --rm -v "$(pwd)":/workspace trufflesecurity/trufflehog:latest \
  filesystem /workspace --json --fail --fail-on-scan-errors --no-update \
  ${EXCLUDE:+--exclude-paths=/workspace/.trufflehog-exclude}

# Scan de l'historique (profondeur au choix, 50 par défaut ici)
docker run --rm -v "$(pwd)":/workspace trufflesecurity/trufflehog:latest \
  git file:///workspace --json --fail --fail-on-scan-errors --no-update --max-depth=50 \
  ${EXCLUDE:+--exclude-paths=/workspace/.trufflehog-exclude}
```

Les motifs d'exclusion ne s'écrivent pas pareil selon la source (`/workspace/…` pour
`filesystem`, chemin relatif pour `git`) et `.git/` doit être écarté du scan `filesystem` :
`references/exclusions.md` détaille les deux pièges, tous deux constatés en test. Le hook
fourni s'en charge tout seul.

## Lire le code de sortie — la seule chose qui compte

| Code | Signification | Ce que tu fais |
|---|---|---|
| `0` | scan effectué, rien trouvé | tu laisses passer |
| `183` | scan effectué, **secrets trouvés** | tu bloques et tu listes |
| **tout autre** | **le scan n'a pas eu lieu** | **tu bloques aussi** |

Cette troisième ligne est la règle la plus importante du skill. Docker éteint, image absente,
fichier d'exclusion illisible, chemin invalide : l'outil sort en `1` ou `125` avec une sortie
standard vide. Un code non nul sans résultats ne veut pas dire « propre », il veut dire
**« je n'ai rien regardé »**. Ne dis jamais « aucun secret détecté » sur autre chose qu'un `0` :
c'est ainsi qu'un garde-fou devient un tampon de conformité.

Vérifie que Docker répond avant de conclure quoi que ce soit : `docker info >/dev/null 2>&1`.

## N'écris jamais le rapport dans le dossier scanné

La sortie JSON contient les secrets **en clair**. Déposée dans l'arborescence, elle est
détectée au scan suivant, elle traîne sur le disque, et elle finit par être commitée. Écris-la
hors du dépôt, ou lis-la depuis un tube sans jamais la poser.

## Deux périmètres, deux usages — ne les confonds pas

| | Périmètre | Coût mesuré | Quand |
|---|---|---|---|
| **Hook pre-commit** | source `git` : l'index (`Staged`) et le dernier commit | 2 à 4 s | à chaque commit |
| **Audit `/scan-secrets`** | tout le disque du dépôt | 72 s sur 2,4 Go | à la demande |

Un hook ne scanne jamais le disque entier. Mesuré sur un dépôt réel de 2,4 Go : 72 secondes
et 93 secrets remontés, dont **91 dans `.venv/` et `target/`** — des dépendances installées,
ignorées par Git, qui ne partiront dans aucun commit. Le même dépôt, côté versionné : 3
secondes, rien. Un hook lent et faux se fait désactiver dans la semaine, et le dépôt se
retrouve sans protection du tout.

Quand tu lances l'audit large, exclus les dossiers générés (`references/exclusions.md`) :
ce qu'ils contiennent n'est ni à toi ni sur le chemin d'un commit.

## Fichiers fournis

| Fichier | Rôle |
|---|---|
| `references/exclusions.md` | le format réel des exclusions, avec les motifs testés |
| `assets/pre-commit` | le hook — la vraie barrière, elle s'applique sans IA dans la boucle |
| `assets/hook-secrets` | pose, retire et inspecte le hook, dépôt par dépôt |
| `assets/trufflehog_mcp_server.py` | serveur MCP, si tu veux l'outil exposé à d'autres clients |

## Poser le hook

```bash
H=~/.claude/skills/scan-secrets/assets/hook-secrets
$H etat ~/chemin/racine     # qui l'a, qui ne l'a pas, quel remote
$H poser <dépôt>...         # installe
$H retirer <dépôt>...       # désinstalle
```

Ce qui est posé dans `.git/hooks/pre-commit` est un **lanceur de trois lignes** qui appelle
le hook central du skill : une correction ici se propage à tous les dépôts sans réinstaller.
Si le hook central devient introuvable, le lanceur bloque le commit au lieu de le laisser
passer. Un hook étranger déjà présent est déplacé, jamais écrasé, et restauré au retrait.
