"""Serveur MCP exposant TruffleHog (exécuté dans Docker) à Claude Code.

    claude mcp add trufflehog -- python3 /chemin/vers/trufflehog_mcp_server.py

Optionnel : le skill sait lancer les mêmes commandes en Bash. Ce serveur n'a d'intérêt
que si tu veux l'outil exposé à d'autres clients MCP.

Principe directeur : fail-closed. Un scan qui n'a pas pu tourner n'est jamais rapporté
comme un scan propre.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("trufflehog")

IMAGE = "trufflesecurity/trufflehog:latest"   # image officielle ; « trhl/trufflehog » n'existe pas
CODE_SECRETS_TROUVES = 183                    # --fail : « Exit with code 183 if results are found »
DELAI_MAX_S = 900


def _fichier_motifs(racine: str, scan_type: str) -> str:
    """Assemble les motifs d'exclusion, hors du dépôt, dans les deux formes de chemin.

    Le scan « filesystem » voit /workspace/tests/x.py, le scan « git » voit tests/x.py :
    un motif écrit pour l'un ne filtre rien pour l'autre, silencieusement.
    """
    lignes = []
    if scan_type == "filesystem":
        # TruffleHog décompresse les objets Git : sans cette ligne, un secret indexé une
        # fois reste détecté à jamais, même retiré du working tree.
        lignes.append(r"^/workspace/\.git/.*$")

    projet = os.path.join(racine, ".trufflehog-exclude")
    if os.path.exists(projet):
        with open(projet, encoding="utf-8") as f:
            for ligne in f:
                motif = ligne.strip()
                if not motif or motif.startswith("#"):
                    continue
                lignes.append(motif)
                lignes.append(re.sub(r"^\^", "^/workspace/", motif))

    tmp = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    tmp.write("\n".join(lignes) + "\n")
    tmp.close()
    return tmp.name


@mcp.tool()
def scan_repository(scan_type: str = "filesystem", depth: int = 50) -> str:
    """Détecte les secrets du dépôt courant avec TruffleHog.

    :param scan_type: 'filesystem' pour le code sur le disque, 'git' pour l'historique.
    :param depth: nombre de commits remontés (scan 'git' uniquement).
    """
    if scan_type not in ("filesystem", "git"):
        return "BLOQUÉ — type de scan invalide : attendu 'filesystem' ou 'git'."
    if not isinstance(depth, int) or not 1 <= depth <= 10_000:
        return "BLOQUÉ — profondeur invalide : attendu un entier entre 1 et 10000."

    racine = os.path.abspath(os.getcwd())

    if shutil.which("docker") is None:
        return "BLOQUÉ — docker introuvable : aucun scan n'a eu lieu."
    if subprocess.run(["docker", "info"], capture_output=True).returncode != 0:
        return "BLOQUÉ — le démon Docker ne répond pas : aucun scan n'a eu lieu."

    motifs = _fichier_motifs(racine, scan_type)
    try:
        cible = ["filesystem", "/workspace"] if scan_type == "filesystem" \
            else ["git", "file:///workspace", f"--max-depth={depth}"]
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{racine}:/workspace",
            "-v", f"{motifs}:/motifs.txt:ro",
            IMAGE, *cible,
            "--json", "--fail", "--fail-on-scan-errors", "--no-update",
            "--exclude-paths=/motifs.txt",
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=DELAI_MAX_S)
        except subprocess.TimeoutExpired:
            return f"BLOQUÉ — le scan {scan_type} a dépassé {DELAI_MAX_S} s : résultat inconnu."

        if r.returncode == 0:
            return f"Propre — scan {scan_type} effectué, aucun secret détecté."

        if r.returncode != CODE_SECRETS_TROUVES:
            # Config illisible, image absente, chemin invalide : rien n'a été analysé.
            # Ne jamais traduire ce cas par « aucun secret » — c'est « je n'ai rien regardé ».
            detail = (r.stderr or "").strip().splitlines()
            return (f"BLOQUÉ — le scan {scan_type} a échoué (code {r.returncode}). "
                    f"Rien n'a été vérifié. {detail[-1] if detail else ''}")

        trouvailles = []
        for ligne in r.stdout.splitlines():
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            data = d.get("SourceMetadata", {}).get("Data", {})
            git, fs = data.get("Git", {}), data.get("Filesystem", {})
            trouvailles.append({
                "detecteur": d.get("DetectorName"),
                "fichier": fs.get("file") or git.get("file") or "?",
                # « Staged » pour un fichier indexé mais pas encore commité.
                "commit": git.get("commit", "—") if scan_type == "git" else "—",
                "verifie_par_api": d.get("Verified", False),
            })

        if not trouvailles:
            return (f"BLOQUÉ — code {CODE_SECRETS_TROUVES} reçu (secrets trouvés) mais "
                    "sortie illisible. Rejoue le scan à la main avant de commiter.")

        return ("CRITIQUE — secrets détectés, commit et push interdits :\n"
                + json.dumps(trouvailles, indent=2, ensure_ascii=False)
                + "\n\nUn secret réel se révoque D'ABORD ; le nettoyage d'historique vient après.")
    finally:
        os.unlink(motifs)


if __name__ == "__main__":
    mcp.run(transport="stdio")
