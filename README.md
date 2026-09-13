# Skills & commandes perso pour Claude Code

Huit extensions que j'utilise au quotidien dans [Claude Code](https://claude.com/claude-code) :
cinq commandes (`~/.claude/commands/`), trois skills (`~/.claude/skills/`) et un script
shell (`bin/`) qui referme le cycle de mémoire.
Écrites en français, testées sur des dépôts réels.

## Ce qu'il y a dedans

### Le cycle de mémoire — `ancrer` · `checkpoint` · `reprise`

Une session finit toujours par saturer son contexte. Ces trois commandes séparent ce qui
doit survivre de ce qui doit disparaître.

| Commande | Ce qu'elle fait |
|---|---|
| `/ancrer [règle]` | Écrit dans le `CLAUDE.md` du dépôt ce qui sera **encore vrai dans trois mois** : commandes de test, conventions, pièges. Fusionne, n'écrase jamais, et vérifie chaque chemin contre le dépôt avant de l'écrire. |
| `/checkpoint [aspect]` | Écrit un `_clear_trigger.txt` : un prompt destiné à un Claude sans aucun souvenir. Sa section la plus importante est celle des **impasses** — ce qui a été essayé et qui ne marche pas, avec la raison. |
| `/reprise [nom]` | Relit le dernier checkpoint, le **confronte au dépôt** (les fichiers existent-ils encore ? l'étape suivante a-t-elle déjà été faite ?), résume les écarts, puis attend une confirmation. |

**Durable → `CLAUDE.md` · éphémère → checkpoint · redémarrage → reprise.**

#### `cl` — la boucle qui referme le cycle

`bin/claude-clean.sh` lance Claude Code et, quand la session se termine, regarde si
`/checkpoint` a laissé un `_clear_trigger.txt` dans le dossier courant. Si oui, il
l'archive dans `.claude/checkpoints/` et **relance Claude dans une session neuve** avec
ce fichier comme prompt initial — le contexte est propre, l'acquis est conservé. Il
recommence tant qu'un nouveau checkpoint apparaît.

```bash
cl                  # dans le dossier du projet
cl --model opus     # les arguments passent au premier lancement
```

Un trigger périmé laissé par une session passée est archivé et ignoré, jamais rejoué.
Le fil des checkpoints reste relisible dans `.claude/checkpoints/` — c'est là que
`/reprise` va chercher.

### Cadrage et construction

| Commande | Ce qu'elle fait |
|---|---|
| `/plan-directeur [périmètre]` | Rapport d'audit, veille et cadrage. Le principe est la **symétrie** : l'existant interne et le benchmark concurrentiel s'évaluent sur la même grille, dans le même ordre, avec les mêmes colonnes — le rapport ne vaut que par l'écart qu'il rend visible. Aucun chiffre sans sa provenance entre crochets. Livré en Artifact. |
| `/feuille-de-route [projet]` | Compte les briques du projet et tranche entre **tunnel A** (solo-agent, ≤ 3 briques) et **tunnel B** (multi-agents, ≥ 4). Règle d'or du tunnel A : rien n'audite son propre travail dans le contexte qui l'a produit. Règle d'or du tunnel B : des garde-fous budgétaires **avant** la première exécution. |

### Skills multi-fichiers

| Skill | Ce qu'il fait |
|---|---|
| `scan-secrets` | Barrière anti-fuite de secrets : TruffleHog dans Docker + un hook `pre-commit` **fail-closed**. La règle centrale : un code de sortie non nul sans résultats ne veut pas dire « propre », il veut dire *« je n'ai rien regardé »*. Le hook ne scanne que ce qui part au commit (2–4 s), l'audit `/scan-secrets` scanne le disque. |
| `prompt-studio-optimizer` | Idée brute → spécification limpide + prompts atomiques testables. Sa première règle est de **savoir se taire** : une demande déjà précise ne reçoit aucune question. |
| `stagiaire` | Mode « stagiaire » : base théorique solide, zéro expérience terrain, zéro improvisation. Chaque demande passe par trois étapes — **recherche des sources**, **justification soumise à validation** (aucune écriture avant le « oui »), puis **exécution stricte** du cadre validé, sans extrapolation. Une validation ne couvre que la démarche pour laquelle elle a été donnée. |

## Installation

```bash
git clone https://github.com/rhw5drppw6-star/claude-code-skills.git
cd claude-code-skills
./install.sh
```

Le script copie `commands/*.md` dans `~/.claude/commands/`, `skills/*` dans
`~/.claude/skills/` et `bin/claude-clean.sh` dans `~/bin/`. Il refuse d'écraser un fichier existant sauf avec `--force`,
et `--link` pose des liens symboliques plutôt que des copies (pratique pour suivre
les mises à jour du dépôt). Redémarre Claude Code ensuite : les commandes apparaissent
avec `/`.

Installation manuelle, si tu préfères choisir :

```bash
cp commands/ancrer.md ~/.claude/commands/
cp -R skills/scan-secrets ~/.claude/skills/
cp bin/claude-clean.sh ~/bin/ && chmod +x ~/bin/claude-clean.sh
```

Pour l'alias `cl`, ajoute à ton `~/.zshrc` (ou `~/.bashrc`) :

```bash
alias cl='~/bin/claude-clean.sh'
```

### Portée

- `~/.claude/commands/` et `~/.claude/skills/` → toutes tes sessions, tous tes projets.
- `<projet>/.claude/commands/` et `<projet>/.claude/skills/` → ce projet seulement.

### Dépendances

Seul `scan-secrets` en a : **Docker** (il exécute l'image officielle
`trufflesecurity/trufflehog`). Son serveur MCP optionnel demande en plus le paquet Python
`mcp`. Les cinq commandes et les deux autres skills n'ont besoin de rien d'autre que Claude Code.

## Écrire la sienne

Un fichier `~/.claude/commands/<nom>.md`, un en-tête YAML, puis le prompt.
`$ARGUMENTS` reçoit ce qui est tapé après la commande.

```markdown
---
description: ce que fait la commande, en une ligne
argument-hint: [ce qu'on peut lui passer, optionnel]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Le prompt. $ARGUMENTS
```

Pour un skill multi-fichiers : un dossier `~/.claude/skills/<nom>/` avec un `SKILL.md`
(en-tête `name` + `description`), et autant de `references/` et `assets/` que nécessaire —
ils ne sont chargés que lorsque le modèle en a besoin.

## Licence

MIT — voir [LICENSE](LICENSE). Prends, modifie, republie.
