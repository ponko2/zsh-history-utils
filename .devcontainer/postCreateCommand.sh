#!/usr/bin/env bash

set -euo pipefail

git config --global --add safe.directory /workspaces/zsh-history-utils

sudo chown -R "$(whoami):" /home/vscode/.cache

curl -LsSf https://astral.sh/uv/install.sh | sh

uv sync
