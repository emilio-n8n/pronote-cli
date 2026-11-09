"""Enregistrement des identifiants (saisie masquée)."""
import getpass
import json
import os
import stat
import sys

from .auth import config_path


def main() -> None:
    path = config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    print("Configuration pronote-cli")
    print("Colle l'URL de l'espace *mobile* de ton établissement, par exemple :")
    print("  https://XXXXXXXX.index-education.net/pronote/mobile.eleve.html")
    url = input("URL Pronote [mobile.eleve.html] : ").strip()
    if not url:
        sys.exit("URL obligatoire.")
    if not url.endswith("mobile.eleve.html"):
        print("\n  Attention : l'URL ne finit pas par mobile.eleve.html.")
        print("  Le portail web classique refuse les connexions automatisées.\n")

    username = input("Identifiant : ").strip()
    if not username:
        sys.exit("Identifiant obligatoire.")

    password = getpass.getpass("Mot de passe (invisible) : ")
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
