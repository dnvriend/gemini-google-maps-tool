---
description: Generate shell completion scripts
argument-hint: shell
---

Generate shell completion scripts for Bash, Zsh, or Fish to enable tab-completion.

## Usage

```bash
gemini-google-maps-tool completion {bash|zsh|fish}
```

## Arguments

- `SHELL`: Shell type - bash, zsh, or fish (required)

## Examples

```bash
# Generate Bash completion
eval "$(gemini-google-maps-tool completion bash)"

# Generate Zsh completion
eval "$(gemini-google-maps-tool completion zsh)"

# Install Fish completion
gemini-google-maps-tool completion fish > \
  ~/.config/fish/completions/gemini-google-maps-tool.fish
```

## Output

Shell-specific completion script that can be evaluated or saved to a file.
