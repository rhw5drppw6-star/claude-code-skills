---
description: Choisit le protocole de construction assistée par IA (solo-agent ou multi-agents) et le déroule jusqu'à la documentation finale
argument-hint: [projet à construire]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, Agent, Skill
---

Établis la feuille de route de construction du projet suivant, puis déroule-la :

$ARGUMENTS

## 1. Trancher le tunnel — avant toute autre chose

Compte les **briques** du projet : un module qui se déploie, se teste et tombe en panne
seul. Une API, un front, un ordonnanceur, un magasin de données comptent chacun pour une.
Un fichier utilitaire ne compte pas.

| Briques | Tunnel | Pourquoi |
|---|---|---|
| 3 ou moins | **A — solo-agent** | L'orchestration coûterait plus cher que le projet |
| 4 ou plus | **B — multi-agents** | Le coût fixe d'orchestration s'amortit |

Annonce ton compte, la liste des briques et le tunnel retenu **avant de commencer**, pour
que je puisse te corriger. Deux réserves qui priment sur le nombre :

- Un projet de 5 briques mais sans aucun test existant reste en **tunnel A** : le tunnel B
  repose sur une suite de tests que l'agent testeur exécute. Sans elle, il n'a rien à faire.
- Un projet de 2 briques dont une touche à de l'argent, à des identifiants ou à de la
  production emprunte quand même la **boucle d'audit** du tunnel A, jamais la voie rapide.

---

## TUNNEL A — protocole solo-agent

**Règle d'or : rien n'audite son propre travail dans le contexte qui l'a produit.**
Un modèle qui relit son code dans la session qui l'a écrit ne le relit pas, il le
reconnaît — il y retrouve ses propres intentions et les prend pour des preuves.

### A.1 — Cadrage et isolation des contextes

- Rédige `spec.txt` à la racine : le livrable, les contraintes, les signatures publiques.
  Il devient la **seule source de vérité**. Toute décision prise en cours de route y remonte.
- Découpe en fonctions isolées, chacune tenant dans une tête à la fois.
- **Ne charge jamais tout le code.** Pour chaque fonction : `spec.txt`, la signature des
  fonctions voisines, rien d'autre. Ce qui n'est pas dans le contexte ne peut pas être cassé.

### A.2 — Le cycle en deux sessions

| | Rôle | Ce qu'on lui donne | Ce qu'on en tire |
|---|---|---|---|
| **Session 1** | développeur senior | `spec.txt` + signatures voisines | le code de la fonction |
| **Session 2** | hacker éthique / QA | le code seul, sans son historique | 5 failles, bugs ou lourdeurs |
| **Retour** | session 1 | les critiques de la session 2 | la correction |

La session 2 s'ouvre **vierge** : un nouveau fil, ou `claude -p` dans un terminal neuf.
Si tu veux que je l'ouvre en sous-agent à contexte froid, demande-le — je ne le fais pas
de moi-même. Un sous-agent qui hérite de mon contexte ne remplit pas la condition.

Demande explicitement **cinq** défauts : en dessous, le modèle s'arrête au premier ; le
quota le force à chercher au-delà de l'évident.

### A.3 — Validation humaine et figeage

- Tu exécutes le code **sur ta machine**. Un test que l'IA décrit sans le lancer ne vaut rien.
- Une fonction qui marche entre en production et **n'y retourne plus**. Modifie-la seulement
  si son comportement doit changer, jamais pour l'embellir.
- Tiens `STRUCTURE.md` à jour : ce qui est figé, ce que ça fait, ce qui en dépend.
  Ce fichier est ce qu'on relit dans six mois — et ce que la prochaine session lira à ta place.

---

## TUNNEL B — protocole multi-agents

**Règle d'or : des garde-fous financiers avant la première exécution, pas après la facture.**

### B.1 — Architecture et connecteurs

- Cinq rôles au plus : PO, Architecte, Codeur, Testeur, Reviewer. Au-delà, ils se marchent dessus.
- Chaque agent reçoit des **outils nommés**, et la liste de ceux qui lui sont interdits :
  un outil non mentionné est implicitement permis, et c'est ainsi qu'un agent finit par
  écrire là où il ne devait pas.
- L'écriture est confinée à un répertoire de travail. L'exécution se limite au lanceur de
  tests du projet (`pytest`, `jest`, …). Jamais de `sudo`, jamais de réseau sortant hors du projet.

### B.2 — Le cycle branché sur Git

1. **Code et test** — le Codeur travaille sur une branche temporaire, jamais sur la principale.
   Le Testeur exécute les tests unitaires du module.
2. **Audit automatisé** — le Reviewer vérifie la conformité, l'accessibilité des composants
   produits et le respect de la spec.
3. **Non-régression** — la suite complète du projet est rejouée. Une suite qui n'existait pas
   avant ce module ne prouve rien : elle ne teste que le neuf.

### B.3 — Garde-fous humains et budgétaires

- `max_loops = 3` entre Codeur et Testeur, et un plafond de tokens par exécution. Le compteur
  doit **survivre** au tour de boucle : un compteur remis à zéro à chaque itération ne compte rien.
- Au troisième échec, le système **se fige** et produit un rapport : ce qui a été tenté, ce qui
  a échoué, l'instruction qui se contredit. Il ne réessaie pas une quatrième fois.
- Le commit et le passage au module suivant sont **une décision humaine**. C'est toi qui
  tranches le conflit d'instructions, pas le Reviewer.

---

## Clôture commune — quel que soit le tunnel

Rien n'est terminé tant que ceci n'existe pas :

- `README.md` : installer, lancer, tester. Vérifie chaque commande en l'exécutant avant de l'écrire.
- La documentation des routes d'API, au format du projet (Swagger/OpenAPI si l'API est HTTP).
- Les choix d'UI/UX retenus, et surtout **ceux qui ont été écartés, avec leur raison** :
  sans quoi ils reviendront dans trois mois sous forme de bonne idée.

## Ce que tu ne fais jamais

- Auditer dans le contexte qui a produit le code.
- Charger tout le projet dans une session « pour avoir le contexte ».
- Annoncer qu'un test passe sans l'avoir exécuté.
- Laisser une boucle d'agents tourner sans borne d'itérations **et** sans plafond de tokens.
- Rouvrir une fonction figée pour l'améliorer.
