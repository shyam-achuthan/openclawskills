# are.na CLI - Simple & Transparent

Simple CLI wrapper for are.na API. No AI. No automation.

## Install

```bash
git clone /path/to/arena-claw ~/arena-claw
chmod +x ~/arena-claw/arena
export PATH="$HOME/arena-claw:$PATH"
```

## Quick Start

```bash
# Add your API token
arena auth YOUR_API_TOKEN

# Check account
arena me

# List channels
arena channels

# Get channel contents
arena channel my-channel
```

## Commands

| Command | Description |
|---------|-------------|
| `arena auth <token>` | Add API token |
| `arena accounts` | List accounts |
| `arena switch <name>` | Switch account |
| `arena me` | Show user |
| `arena channels` | List channels |
| `arena channel <slug>` | Get contents |
| `arena add image <url>` | Add image |
| `arena add link <url>` | Add link |
| `arena watch <slug>` | Watch changes |
| `arena search <query>` | Search |
| `arena create <title>` | Create channel |
| `arena doctor` | Debug |

## Multi-Account

```bash
arena auth TOKEN1 account1
arena auth TOKEN2 account2
arena switch account1
arena -a account2 channel shared
```

## Security

- Tokens stored in `~/.arena_token` or `~/.openclaw/.arena_tokens`
- Only talks to `api.are.na`
- No external calls
- No data exfiltration

## Uninstall

```bash
rm -rf ~/arena-claw
rm ~/.arena_token ~/.openclaw/.arena_tokens
```
