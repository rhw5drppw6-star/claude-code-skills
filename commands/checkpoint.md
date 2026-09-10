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

Une fois écrit, affiche le contenu du fichier pour que je puisse le corriger, puis dis :
"Mémoire sauvegardée ! Tu peux quitter la session, le script va automatiquement te recréer un contexte propre."
