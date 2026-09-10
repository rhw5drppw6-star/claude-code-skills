# Exclure un faux positif — le format réel

## Ce qui ne marche pas

Un fichier `trufflehog.yaml` de cette forme est du **gitleaks**, pas du TruffleHog :

```yaml
version: "1.0"
allowlist:
  paths: [...]
  secrets: [...]
```

Passé à `--config`, TruffleHog le rejette et **s'arrête avant de scanner** :

```
error parsing the provided configuration file  error: proto: unknown field "allowlist"
```

Sortie en code `1`, zéro fichier analysé. Un appelant qui interprète « code non nul sans
résultats » comme « rien trouvé » annonce alors un dépôt propre qui n'a jamais été regardé.
C'est le scénario que la table des codes de sortie du SKILL.md existe pour empêcher.

`--config` sert aux **détecteurs personnalisés**, pas aux exclusions.

## Ce qui marche

Un fichier texte, **une expression régulière par ligne**, passé à `--exclude-paths` (`-x`).

`.trufflehog-exclude`, à la racine du dépôt, motifs **relatifs à la racine** :

```
# fixtures de test : jetons factices, jamais valides
^tests/fixtures/.*$
^docs/examples/.*$
^.*\.lock$

# dépendances installées : ni écrites par toi, ni versionnées, ni commitables
# (à l'audit large uniquement — le hook ne regarde déjà que le versionné)
^.*/(node_modules|\.venv|venv|target|dist|build|__pycache__|\.next)/.*$
```

## Le piège : les deux sources ne nomment pas les fichiers pareil

Le même secret, le même fichier, deux scans — deux chemins différents :

| Scan | Chemin rapporté | Motif qui filtre |
|---|---|---|
| `filesystem` | `/workspace/tests/fixtures/x.py` | `^/workspace/tests/fixtures/.*$` |
| `git` | `tests/fixtures/x.py` | `^tests/fixtures/.*$` |

Un motif écrit pour l'une **ne filtre rien pour l'autre, et sans le dire**. Constaté en test :
avec les seuls motifs `/workspace/…`, le scan fichiers passait au vert pendant que le scan
git bloquait toujours sur le même fichier.

C'est pourquoi le hook fourni assemble lui-même les deux formes à partir de tes motifs
relatifs. Si tu appelles TruffleHog à la main, écris les deux, ou vise la bonne source.

## `.git/` doit être écarté du scan « filesystem »

TruffleHog sait décompresser les objets Git. Un scan `filesystem` sur la racine d'un dépôt
lit donc `.git/objects/`, où survit **tout ce qui a été indexé une seule fois** — même un
fichier supprimé depuis, même un commit jamais abouti. Constaté en test : un secret retiré
du working tree continuait de bloquer, signalé dans
`/workspace/.git/objects/ec/0b3ec0…`.

Sans exclusion, le blocage est perpétuel et le message désigne un blob illisible plutôt
qu'un fichier. Le hook écarte donc `^/workspace/\.git/.*$` d'office : l'historique reste
couvert par le scan `git`, qui sait dire dans quel commit — ou dans l'index (`Staged`) —
se trouve la fuite.

## Les autres leviers

| Besoin | Option |
|---|---|
| Exclure un détecteur entier | `--exclude-detectors=github,openai` |
| Ne remonter que les secrets confirmés par appel API | `--results=verified` |
| Ne garder que certains chemins | `--include-paths` (`-i`), même format |

## La règle de jugement

Une exclusion se justifie par ce qu'**est** le fichier, jamais par le fait qu'il bloque.
Une fixture de test, un exemple de documentation : légitimes. Un fichier de configuration
de production, un `.env`, un dossier entier « parce que ça gêne » : c'est le blocage qui
avait raison. Chaque ligne ajoutée mérite un commentaire disant pourquoi elle est là —
sinon elle survit à la raison qui l'a créée.
