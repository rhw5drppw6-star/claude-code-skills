# Anatomie d'un bloc de prompt

## Structure standard

```xml
<role_definition>
Expert senior dans la technologie ciblée.
</role_definition>

<project_context>
Contexte concis du projet (1 à 2 phrases).
</project_context>

<current_block_goal>
Objectif atomique unique de cette étape.
</current_block_goal>

<inputs_and_dependencies>
- Fichiers ou composants requis issus des étapes précédentes.
- Dépendances ou variables d'environnement nécessaires.
</inputs_and_dependencies>

<step_by_step_instructions>
1. Instruction chronologique 1.
2. Instruction chronologique 2.
</step_by_step_instructions>

<negative_constraints>
- NE PAS laisser de code partiel ou d'ellipses.
- NE PAS inventer de fonctions en dehors de la spec.
</negative_constraints>

<output_format>
Format exact attendu (ex: code TypeScript complet du fichier `src/lib/api.ts`).
</output_format>

<reminder_before_execution>
Rappel de la contrainte la plus critique de ce bloc (répétée depuis <role_definition>).
Si une variable d'environnement, une clé de configuration ou un fichier nécessaire à ce
bloc est absent des entrées fournies, signale-le immédiatement et arrête-toi, au lieu de
produire du code partiel ou d'inventer une valeur.
</reminder_before_execution>
```

#### Deux balises de plus pour les cibles Agent

Quand la cible est `Agent Autonome` ou `Équipe d'Agents`, ajoutez ces deux balises — sans
elles, un agent qui exécute le prompt n'a aucune limite écrite :

```xml
<tools_contract>
- read_page(url: string) -> string
- write_markdown(path: string, content: string) -> bool
Outils INTERDITS à cette étape : shell, delete_file, http_post.
</tools_contract>

<preconditions>
- La variable OPENROUTER_API_KEY doit être lue avant d'entrer dans la boucle.
- Le dossier ./veille/ doit exister.
Si une précondition manque : arrête-toi et signale-le. N'improvise jamais une valeur.
</preconditions>
```

Trois règles non négociables pour ces cibles :
1. **Nommez les outils interdits**, pas seulement les autorisés — sinon tout le reste est
   implicitement permis.
2. **Donnez un critère d'arrêt** et un nombre maximal d'itérations. Une boucle d'agent sans
   borne tourne indéfiniment et consomme jusqu'à épuisement du crédit.
3. En mode Équipe : **au maximum 3 agents plus un bloc d'orchestration**, et des prompts
   d'agent plus courts (1 200 à 2 400 caractères). Une équipe produit autant de prompts
   qu'elle compte de rôles ; au-delà, la réponse est tronquée en cours de génération.

Le bloc d'orchestration décrit l'ordre de passage, le format d'échange entre agents, la
condition d'arrêt globale, et ce qui se passe si un agent renvoie une sortie non conforme.
Deux agents ne partagent jamais le même outil d'écriture sans arbitre désigné.

---

> [!important] Pourquoi une 8e balise de rappel final
> Un LLM lit mal le milieu d'un prompt. `<reminder_before_execution>` occupe la position de
> récence : c'est là que se replacent la contrainte la plus critique du bloc **et la clause
> de réfutation**. Les deux extrémités — `<role_definition>` au début, ce rappel à la fin —
> portent ce qui ne doit surtout pas être oublié.

---
