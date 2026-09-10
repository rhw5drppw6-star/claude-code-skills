# Les quatre formats de guide

## La question à poser

> [!IMPORTANT]
> Vous **DEVEZ** obligatoirement demander à l'utilisateur sous quel format il souhaite recevoir son guide de projet avant de générer la version finale :

Posez la question suivante à l'utilisateur :
```markdown
### 📝 Sous quel format souhaitez-vous recevoir votre guide de projet ?
1. **🅰️ Note Obsidian / Markdown Enrichie** : Structure complète avec callouts (`> [!info]`), diagramme Mermaid, liens `[[wikilinks]]` et tableau d'architecture.
2. **🅱️ Suite de Blocs XML Prêts à l'Emploi** : Prompts découpés avec les 8 balises strictes (`<role_definition>`, `<current_block_goal>`, `<negative_constraints>`, `<reminder_before_execution>`…) prêts à copier dans votre outil cible.
3. **🅲️ Guide Opérationnel Pas-à-Pas (Test-Driven)** : Chaque étape avec sa checklist visuelle, ses commandes shell de test et ses critères d'acceptation Pass/Fail.
4. **🅳️ Spécification Technique Consolidée (Cahier des Charges)** : Synthèse exhaustive, modèles de données, endpoints d'API et règles de gestion.
*(Vous pouvez aussi demander un format combiné, ex: Note Obsidian + Blocs XML)*
```
