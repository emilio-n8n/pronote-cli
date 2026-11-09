# Portée : comptes élève vs comptes professeur

Ce dépôt est écrit pour un **compte élève**. Le passage à un compte professeur
n'est pas un simple changement d'URL : l'espace enseignant est un autre produit,
avec d'autres onglets et d'autres fonctions serveur.

## Ce qui se réutilise tel quel

- **L'authentification.** Même mécanisme : `Identification` puis `Authentification`,
  avec un challenge et un mot de passe haché côté client. `pronotepy` gère déjà ça,
  et c'est la partie la plus délicate à reproduire.
- **La signature des requêtes.** Chaque requête POST porte une signature calculée
  sur le corps et un en-tête d'ordre. Indépendant du type de compte.
- **La gestion de session et le format des réponses** (`dataSec.data`).

C'est pour cette raison que la base est bonne : les deux tiers du travail (parler
au serveur) sont faits.

## Ce qui change

- **L'URL.** L'espace enseignant n'est pas `/pronote/eleve.html` mais un autre
  point d'entrée de l'établissement. À relever dans le navigateur du compte concerné.
- **Les objets métier.** Un professeur n'a pas de « moyennes par matière » ni de
  « devoirs à faire » : il a des classes, des élèves, des évaluations, des
  appréciations, des absences à justifier.
- **Les fonctions serveur.** Le lecteur de notes côté élève (`DernieresNotes` et
  consorts) ne donne pas la saisie. Écrire une note suppose de reproduire la
  fonction de saisie de l'espace enseignant, qui n'existe pas dans `pronotepy`.

## Comment attaquer l'adaptation

1. Se connecter au compte professeur dans le navigateur, ouvrir la page de saisie
   des notes, enregistrer un **HAR** (F12 → Réseau → cocher « Allow to generate HAR
   with sensitive data »).
2. Repérer la fonction serveur appelée lors d'un enregistrement, et la forme exacte
   du corps envoyé (numéro d'onglet, identifiants d'élève, de période, de service).
3. La rejouer en Python pur via `client.post("<NomDeLaFonction>", onglet, data)`,
   en commençant par une **lecture** (aucune écriture tant que la lecture ne
   renvoie pas les bonnes données).
4. N'écrire qu'ensuite, sur une évaluation de test créée par l'enseignant lui-même,
   jamais sur une note réelle.

## Avertissement

Écrire des notes au nom d'un enseignant est un acte qui a des conséquences réelles
sur des élèves. Un tel outil doit rester en **confirmation humaine obligatoire** :
l'agent prépare, l'enseignant valide. Aucun envoi automatique.
