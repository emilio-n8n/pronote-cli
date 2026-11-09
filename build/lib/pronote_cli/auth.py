"""Chargement des identifiants et connexion Pronote."""
import json
import os
import sys

import pronotepy

DEFAULT_PATH = "~/.config/pronote-cli/credentials.json"


def config_path() -> str:
    """Chemin du fichier d'identifiants (PRONOTE_CONFIG sinon ~/.config/pronote-cli)."""
    return os.path.expanduser(os.environ.get("PRONOTE_CONFIG", DEFAULT_PATH))


def load() -> dict:
    path = config_path()
    if not os.path.exists(path):
        sys.exit(f"Identifiants absents ({path}). Lance `python -m pronote_cli.setup`.")
    with open(path) as f:
        return json.load(f)


def connect():
    """Ouvre une session. Sort proprement (code 1) en cas d'échec."""
    c = load()
    try:
        cli = pronotepy.Client(
            c["pronote_url"],
            c["username"],
            c["password"],
            uuid=c.get("uuid", "pronote-cli"),
            client_identifier=c.get("client_identifier"),
            device_name=c.get("device_name", "pronote-cli"),
        )
    except Exception as e:
        msg = str(e)
        if "23" in msg or "trop" in msg.lower():
            sys.exit("Pronote verrouille le compte (trop d'authentifications). "
                     "Attends 10-30 min, ne relance pas en boucle.")
        sys.exit(f"Connexion impossible : {type(e).__name__} {msg[:200]}")

    if not getattr(cli, "logged_in", False):
        sys.exit(
            "Pronote refuse l'identifiant ou le mot de passe.\n"
            "  • Vérifie que l'URL se termine par /pronote/mobile.eleve.html\n"
            "    (le portail .../eleve.html refuse les clients automatisés).\n"
            "  • Relance `python -m pronote_cli.setup` en collant le mot de passe."
        )
    return cli
