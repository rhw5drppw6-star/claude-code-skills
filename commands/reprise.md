---
description: Recharge le dernier checkpoint archivé et reprend le travail là où il s'était arrêté
argument-hint: [nom ou date d'un checkpoint précis, optionnel]
allowed-tools: Read, Bash, Grep, Glob
---

Reprends le travail à partir d'un checkpoint sauvegardé.

$ARGUMENTS

**Marche à suivre :**

1. Liste les checkpoints disponibles :
   `ls -lt .claude/checkpoints/ 2>/dev/null | head -20`
   S'il n'y en a aucun, cherche un `_clear_trigger.txt` à la racine.
   Si rien n'existe nulle part, dis-le simplement et arrête-toi là.

2. Prends le plus récent — sauf si j'ai précisé lequel ci-dessus. Lis-le.

3. **Confronte le checkpoint à la réalité avant de me répondre.** Il a pu vieillir :
   - les fichiers cités existent-ils toujours ? (`ls`, `git log --oneline -15`)
   - la « prochaine étape » a-t-elle déjà été faite entre-temps ?
   - `git status` : y a-t-il du travail non commité dont le checkpoint ne parle pas ?

4. Fais-moi une synthèse en trois blocs, courte :
   - **Reprise** : l'objectif et le prochain geste concret, tels que le checkpoint les donne.
   - **Écarts** : ce qui a changé dans le dépôt depuis, et ce que ça invalide.
   - **À ne pas refaire** : les impasses listées dans le checkpoint, en une ligne chacune.

5. Puis attends ma confirmation avant de modifier quoi que ce soit.
   Un checkpoint est une piste, pas un ordre de mission.
