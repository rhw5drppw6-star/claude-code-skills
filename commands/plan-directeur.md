---
description: Produit un rapport d'audit, de veille et de cadrage projet selon le plan directeur symétrique (audit interne / benchmark sur la même grille)
argument-hint: [projet ou périmètre à auditer]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Artifact, Skill, AskUserQuestion
---

Rédige un **Rapport d'Audit, Veille et Cadrage Projet** sur le sujet suivant :

$ARGUMENTS

## Principe directeur — la symétrie

La Section 1 (mon existant) et la Section 2 (le marché) s'évaluent sur **la même
grille, dans le même ordre, avec les mêmes colonnes de tableau**. Le rapport ne
vaut que par l'écart mesurable qu'il rend visible entre les deux ; la Section 3
ne fait que combler cet écart. Si un critère n'est renseigné que d'un côté, il ne
sert à rien : va le chercher, ou retire-le des deux.

Les quatre axes de la grille, invariants :
**Business & Terrain · Technique & Sécurité · UI/UX & Design · Accessibilité & Conformité**

## Phase 0 — Cadrer avant d'écrire (obligatoire)

N'écris pas une ligne de rapport avant d'avoir :

1. **Inventorié les sources réelles** : dépôt, docs, tickets, analytics, retours
   support, factures d'infra — ce qui existe vraiment sur le disque ou ce que je
   te fournis. Explore le projet, ne suppose pas.
2. **Posé les questions bloquantes** en une seule fois (`AskUserQuestion`) :
   périmètre exact, les 3 concurrents à retenir, budget et échéance cibles,
   accès aux données chiffrées. Ne pose que ce qui change réellement le rapport.
3. **Lancé la veille** : `WebSearch`/`WebFetch` sur les concurrents, les normes
   (RGAA/WCAG, obligations sectorielles) et les tendances design du secteur.

## Règle de vérité — aucun chiffre inventé

Tout chiffre porte sa provenance, immédiatement, entre crochets :
`[analytics 2026-Q2]`, `[grille tarifaire concurrent, page consultée le JJ/MM]`,
`[**À CONFIRMER** — hypothèse de travail]`.
Un ROI, un budget ou une part de marché sans source est une hypothèse : il s'écrit
en toutes lettres comme telle. Mieux vaut une case « non mesuré » qu'un chiffre
plausible et faux — un rapport de cadrage sert à décider d'un investissement.

## Structure imposée du livrable

### 📜 Executive Summary — une page maximum, rédigée en dernier, placée en premier
- **Le constat urgent** : situation actuelle et pourquoi le statu quo est intenable.
- **La vision & différenciation** : fonctions, technologies, identité visuelle.
- **Les chiffres clés** : budget global estimé, ROI attendu, date de livraison.

### 1. L'Audit de l'existant — diagnostic interne symétrique
- Performance business & terrain : retours, plaintes support, abandon, satisfaction.
- Performance technique & sécurité : blocages récurrents, lenteurs, coût de maintenance, exposition.
- UI/UX & accessibilité interne : parcours (nombre de clics, clarté), charte vieillissante, contrastes et lisibilité.
- **Synthèse SWOT** : forces/faiblesses internes déduites de l'audit, face aux opportunités/menaces.

### 2. Veille stratégique & benchmark — l'analyse miroir (3 concurrents maximum)
- Benchmark business : parts de marché, prix, promesses, et surtout **leurs angles morts** (ce que leurs clients leur reprochent).
- Veille technologique : innovations (IA, automatisation) déjà éprouvées chez eux ou dans un secteur connexe.
- Benchmark UI/UX & design : **tendances & codes** (palettes, typographies, styles dominants) puis **contre-tendances** — ce que le secteur s'interdit et qui devient une opportunité de rupture graphique.
- Veille accessibilité & réglementation : conformité RGAA/WCAG des concurrents, à transformer en argument de différenciation.

### 3. Plan d'action, budgets & déploiement progressif
- **Matrice Impact / Effort** : Quick Wins distingués visuellement des chantiers de fond.
- **Feuille de route & ROI** : calendrier (Gantt) adossé aux coûts réels (licences, développements) et aux gains espérés.
- **Stratégie MVP** : tests à petite échelle — maquettes animées pour l'UI/UX, prototypes pour la tech — avant tout développement global.

### 4. Maîtrise des risques & alignement humain
- **Matrice des risques & plan B** : atténuation pour chaque scénario critique (dérive budgétaire, bugs, rejet de la nouvelle interface par les utilisateurs historiques).
- **Plan d'adoption** : communication et formation, pour que l'outil et le design neufs soient maîtrisés dès le premier jour.

### 🚀 5. Plan de démarrage immédiat — les 7 prochains jours
- **Le premier domino** : la toute première action concrète qui lance la machine.
- **Attribution des responsabilités** : qui fait quoi, immédiatement.

## Standards de forme

- **Tableaux comparatifs stricts** : structure de tableau identique en Section 1 et
  en Section 2, pour que la comparaison se fasse à l'œil, ligne à ligne.
- **Code couleur fonctionnel, sans exception** : rouge/orange **uniquement** pour
  les urgences et les retards ; vert/bleu pour les solutions et propositions d'avenir.
  Aucune couleur décorative.
- Phrases courtes, verbes d'action, aucune prose de remplissage. Un tableau ou une
  matrice partout où une liste à puces suffirait moins bien.

## Livraison

Le rapport est un document destiné à être lu et partagé : livre-le en **Artifact**.
Charge la skill `artifact-design` avant d'écrire la page, et `dataviz` avant toute
matrice, Gantt ou graphique. Si je demande explicitement un fichier, écris-le en
Markdown à la racine du projet concerné.

Termine par la liste des cases restées `[À CONFIRMER]` : ce sont les données que
je dois aller chercher pour que le rapport devienne décisionnel.
