#!/bin/sh
# Installation de pronote-cli en une commande.
#   sh install.sh
# Crée un environnement Python isolé, installe l'outil, ajoute la commande
# `pronote` dans ~/.local/bin, puis lance la configuration.
set -eu

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
VENV="$HOME/.pronote-cli/venv"
BIN_DIR="$HOME/.local/bin"

say() { printf '%s\n' "$*"; }
die() { printf 'Erreur : %s\n' "$*" >&2; exit 1; }

# 1. Python 3.9+
PY=""
for candidate in python3 python3.13 python3.12 python3.11 python3.10 python3.9; do
    if command -v "$candidate" >/dev/null 2>&1; then
        if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; then
            PY="$candidate"; break
        fi
    fi
done
[ -n "$PY" ] || die "Python 3.9 ou plus est requis. Sur macOS : xcode-select --install"

say "Python utilisé : $PY ($("$PY" -V 2>&1))"

# 2. Environnement isolé
say "Création de l'environnement dans $VENV"
mkdir -p "$HOME/.pronote-cli"
[ -d "$VENV" ] || "$PY" -m venv "$VENV" || die "Impossible de créer l'environnement virtuel."
"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install --quiet "$REPO_DIR" || die "Installation échouée."

# 3. Commande `pronote`
mkdir -p "$BIN_DIR"
ln -sf "$VENV/bin/pronote" "$BIN_DIR/pronote"
say "Commande installée : $BIN_DIR/pronote"

case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) say "Attention : $BIN_DIR n'est pas dans ton PATH. Ajoute cette ligne à ~/.zshrc :"
       say "  export PATH=\"\$HOME/.local/bin:\$PATH\"" ;;
esac

# 4. Configuration
say ""
say "Configuration des identifiants (une seule fois)."
"$VENV/bin/python" -m pronote_cli.setup

say ""
say "Terminé. Essaie :"
say "  pronote today"
