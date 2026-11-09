# pronote-cli

Un petit outil en ligne de commande pour lire ses données Pronote (emploi du temps,
devoirs, notes, liens des profs, messages) sans ouvrir un navigateur.

Conçu comme une brique pour un agent (Hermes, Claude Code, Codex…) : chaque commande
sort du texte brut, facile à lire pour un humain **et** pour un modèle.

```
pronote today            cours du jour
pronote week [n]         semaine n (0 = cette semaine, 1 = la suivante)
pronote homework [jours] devoirs sur N jours (défaut 14)
pronote grades           moyennes par matière
pronote links [jours]    liens Teams / sites déposés par les profs
pronote messages [n]     derniers messages (défaut 5)
```

## Pourquoi ce projet existe

L'API interne de Pronote n'est pas documentée, et le portail web (`.../pronote/eleve.html`)
refuse les clients automatisés. L'astuce : **l'endpoint mobile**
(`.../pronote/mobile.eleve.html`) accepte les mêmes identifiants et renvoie le même
contenu. C'est le point le plus important du dépôt — si vous obtenez une erreur
d'authentification alors que vos identifiants fonctionnent dans le navigateur,
vous êtes probablement sur le mauvais endpoint.

## Installation

```bash
git clone https://github.com/emilio-n8n/pronote-cli.git
cd pronote-cli
sh install.sh
```

Le script crée un environnement Python isolé dans `~/.pronote-cli/venv`, installe
la commande `pronote` dans `~/.local/bin`, puis demande l'URL, l'identifiant et
le mot de passe (saisie masquée).

Installation manuelle, si tu préfères :

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install .
python -m pronote_cli.setup
```

Les identifiants sont stockés dans `~/.config/pronote-cli/credentials.json`
(permissions 600). En environnement de test, `PRONOTE_CONFIG` permet de changer ce chemin.

## Limitations assumées (état actuel : comptes élève)

- **Comptes élève uniquement.** L'API utilisée ici est celle de l'espace élève.
  Les comptes professeur utilisent un autre espace Pronote, avec d'autres onglets et
  d'autres fonctions — voir `docs/portee.md`. La couche d'authentification et de
  signature des requêtes est en revanche la même : c'est la partie réutilisable.
- **Lecture seule.** L'outil ne modifie rien. Écrire des notes depuis un compte
  professeur demanderait de reproduire les requêtes de saisie, ce qui n'est pas
  fait ici.
- **Pas de retry automatique.** En cas de verrouillage (trop de tentatives), le
  script s'arrête et le dit. Une boucle de réessai ne ferait qu'aggraver le blocage.
- **Dépend de `pronotepy`**, qui suit les évolutions du serveur. Une mise à jour de
  Pronote peut casser l'outil : c'est le risque de tout client non officiel.

## Avertissement

Projet non officiel, sans lien avec Index Éducation. Vous l'utilisez sur **votre**
compte, avec **vos** identifiants. Le scraping peut être contraire aux conditions
d'utilisation de votre établissement : vérifiez avant de diffuser.

## Licence

MIT — voir `LICENSE`.
