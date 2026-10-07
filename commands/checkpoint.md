---
description: Écrit un prompt de reprise pour repartir sur un contexte propre sans perdre l'acquis
argument-hint: [aspect à privilégier, optionnel]
allowed-tools: Write, Read, Bash, Grep, Glob
---

Analyse l'historique de notre session, puis écris `_clear_trigger.txt` dans le dossier courant.

$ARGUMENTS

Ce fichier est un prompt adressé à un Claude qui n'a **aucun souvenir** de la session.
Structure-le ainsi :

## 1. Objectif
Le but du projet en 2 phrases. Puis le but de *cette* session en particulier.

## 2. État réel
Trois listes distinctes, sans les mélanger :
- **Fait et vérifié** — le code tourne, les tests passent (dis lesquels).
- **Écrit mais jamais exécuté** — la partie dangereuse : ne la présente jamais comme acquise.
- **Pas commencé.**

## 3. Impasses (section la plus importante)
Ce qui a été essayé et qui **ne marche pas**, avec la raison exacte : approches
abandonnées, bibliothèques écartées, messages d'erreur rencontrés, hypothèses
invalidées. Sans cette section, la session suivante refera ces erreurs.

## 4. Contraintes
Ce que l'utilisateur a demandé ou refusé en cours de route et qui n'est écrit nulle
part dans le code : style, choix techniques imposés, fichiers à ne pas toucher,
préférences de communication.

## 5. Commandes du projet
Comment lancer les tests, le build, le serveur. Chemins exacts.

## 6. Reprise immédiate
Le prochain geste concret : quel fichier, quelle fonction, quelle ligne, quoi y faire.
Pas « continuer l'implémentation » mais « ajouter la validation du token dans
auth.py:42, la fonction verify() renvoie True sans vérifier l'expiration ».

## 7. Incertitudes
Ce dont tu n'es pas sûr, marqué explicitement comme tel.

---

**Règles de rédaction :**
- **Pointe, ne paraphrase pas.** Le prochain Claude sait lire les fichiers. Donne les
  chemins ; ne recopie pas le code. Le résumé sert à ce qui n'est *pas* dans le dépôt.
- N'écris rien qui ne soit pas dans notre historique. Aucune extrapolation.
- Jamais de « comme convenu », « on continue » : le lecteur n'était pas là.
- 400 mots maximum.

---

## Phase 2 — Purge (avant d'afficher le fichier)

Le contexte déjà chargé ne peut pas être effacé : il est en lecture seule, seuls `/clear` et
le compactage automatique le réduisent. Ce qui suit réduit donc ce que la session aura à
RELIRE et à porter ensuite — ce qui revient au même en pratique, et permet de continuer
sans quitter la conversation.

**1. Mettre à l'abri ce qui vit encore dans le scratchpad.** Le scratchpad disparaît à la fin
de la session. Avant toute suppression, vérifier que ces éléments existent ailleurs :
- rapports d'agents déjà exploités → dans le dépôt concerné, ou dans `<projet>/rapports/` ;
- fichiers écrits par un agent et pas encore relus → les DÉPLACER, jamais les supprimer ;
- clés, jetons, identifiants encore utiles → hors scratchpad, permissions 600 ;
- captures et exports qui servent de preuve → joints au projet ou envoyés à l'utilisateur.

**2. Supprimer ce qui est reproductible en une commande** (et cela seulement) :
- exports web, dossiers de build, archives, `dist/`, `/tmp/*-web` ;
- sorties d'agents dont les constats sont déjà appliqués ET consignés ;
- fichiers de travail intermédiaires (prompts d'agents déjà lancés, logs d'attente).
Ne jamais supprimer : un fichier du dépôt, une donnée non versionnée, un rapport non lu,
la moindre chose que l'utilisateur n'a pas vue.

**3. Écrire l'état condensé** dans `_clear_trigger.txt` (déjà fait en phase 1) et rappeler à
l'utilisateur, en une ligne, ce qui a été déplacé et ce qui a été supprimé.

**4. Annoncer ce qui reste lourd** : si des éléments volumineux subsistent (caches de build,
`node_modules`, exports de données), les citer avec leur taille et demander avant de purger.
Une suppression n'est jamais automatique : elle se propose.

---

Une fois écrit, affiche le contenu du fichier pour que je puisse le corriger, puis dis :
"Mémoire sauvegardée ! Tu peux quitter la session, le script va automatiquement te recréer un contexte propre."

Si la session continue sans `/clear`, remplacer cette phrase par : le point de reprise est
écrit, la purge est faite, et la suite du travail peut reprendre ici même.
