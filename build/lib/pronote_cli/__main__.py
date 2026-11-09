"""Point d'entrée : python -m pronote_cli <commande>."""
import sys

from . import commands

USAGE = """pronote-cli — tes données Pronote en ligne de commande.

  pronote today            cours du jour
  pronote week [n]         semaine n (0 = cette semaine, 1 = la suivante)
  pronote homework [jours] devoirs sur N jours (défaut 14)
  pronote grades           moyennes par matière
  pronote links [jours]    liens Teams / sites déposés par les profs
  pronote messages [n]     derniers messages (défaut 5)

Une seule authentification par commande. En cas de verrouillage (erreur 23),
le script s'arrête et le dit — aucune boucle de réessai.
"""

COMMANDS = {
    "today": commands.today,
    "week": commands.week,
    "homework": commands.homework,
    "grades": commands.grades,
    "links": commands.links,
    "messages": commands.messages,
}


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print(USAGE)
        return

    name, rest = args[0], args[1:]
    if name not in COMMANDS:
        print(USAGE)
        sys.exit(2)

    func = COMMANDS[name]
    if rest:
        try:
            func(int(rest[0]))
        except ValueError:
            sys.exit(f"Argument invalide : {rest[0]} (un nombre de jours est attendu).")
    else:
        func()


if __name__ == "__main__":
    main()
