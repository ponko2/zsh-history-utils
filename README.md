# Zsh history utils

[![CI](https://github.com/ponko2/zsh-history-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/ponko2/zsh-history-utils/actions/workflows/ci.yml)
[![CodeQL](https://github.com/ponko2/zsh-history-utils/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/ponko2/zsh-history-utils/actions/workflows/github-code-scanning/codeql)

## Usage

### Decode

```sh
uv run zsh_history_utils.py decode $HISTFILE >! .zsh_history
```

### Encode

```sh
uv run zsh_history_utils.py encode .zsh_history >! $HISTFILE
```
