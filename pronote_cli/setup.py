"""Enregistrement des identifiants (saisie masquée)."""
import getpass
import json
import os
import stat
import sys

from .auth import config_path


def _ask(prompt: str) -> str:
    """input() qui échoue proprement si l'entrée n'est pas interactive."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit("Configuration interrompue — rien n'a été enregistré.")


def main() -> None:
    path = config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    print("Configuration pronote-cli")
    print("Colle l'URL de l'espace *mobile* de ton établissement, par exemple :")
    print("  https://XXXXXXXX.index-education.net/pronote/mobile.eleve.html")
    url = _ask("URL Pronote [mobile.eleve.html] : ")
    if not url:
        sys.exit("URL obligatoire.")
    if not url.endswith("mobile.eleve.html"):
        print("\n  Attention : l'URL ne finit pas par mobile.eleve.html.")
        print("  Le portail web classique refuse les connexions automatisées.\n")

    username = _ask("Identifiant : ")
    if not username:
        sys.exit("Identifiant obligatoire.")

    try:
        password = getpass.getpass("Mot de passe (invisible) : ")
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit("Configuration interrompue — rien n'a été enregistré.")
    if not password:
        sys.exit("Mot de passe vide.")

    data = {
        "pronote_url": url,
        "username": username,
        "password": password,
        "uuid": "pronote-cli",
        "client_identifier": None,
        "device_name": "pronote-cli",
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=1)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 600
    print(f"\nEnregistré dans {path} (lisible par toi seul).")
    print("Teste avec : python -m pronote_cli today")


if __name__ == "__main__":
    main()
