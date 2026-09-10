# Protocole de validation QA

## Ce qui accompagne chaque bloc

Chaque bloc de prompt doit obligatoirement être accompagné de son protocole de vérification pour l'humain :
- **Checklist Visuelle** : 2 à 3 points clés à inspecter à l'œil nu dans la réponse de l'IA.
- **Commande Shell de Test** : commandes terminal exécutables (`npm run type-check`,
  `pytest -v`, `curl -I http://localhost:3000/...`).
- **Critère de Succès (Pass / Fail)** : Ce qui valide le passage au bloc suivant.

> [!danger] Ces commandes seront exécutées par un humain qui vous fait confiance
> Ne proposez que des vérifications **en lecture seule**, ou créant au plus un fichier
> temporaire. Sont interdits : `rm`, `mv` sur des fichiers du projet, `sudo`, `chmod -R`,
> et tout appel réseau sortant vers un domaine étranger au projet.
> Si vous livrez ces commandes dans un fichier `.sh`, **livrez-les commentées**, sous un
> en-tête disant qu'elles ont été écrites par un LLM et doivent être relues avant exécution.
