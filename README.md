# Zsh history utils

## Usage

### Decode

```sh
uv run zsh_history_utils.py decode $HISTFILE >! .zsh_history
```

### Encode

```sh
uv run zsh_history_utils.py encode .zsh_history >! $HISTFILE
```
