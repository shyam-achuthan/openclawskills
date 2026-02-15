---
name: airpoint
description: Control a Mac through natural language — open apps, click buttons, read the screen, type text, manage windows, and automate multi-step tasks via Airpoint's AI computer-use agent.
metadata: {"openclaw": {"emoji": "🖐️", "homepage": "https://airpoint.app", "requires": {"bins": ["airpoint"]}, "os": ["darwin"]}}
---

# Airpoint — AI Computer Use for macOS

Airpoint gives you an AI agent that can **see and control a Mac** — open apps,
click UI elements, read on-screen text, type, scroll, drag, and manage windows.
You give it a natural-language instruction and it carries out the task
autonomously by perceiving the screen (accessibility tree + screenshots + visual
locator), planning actions, executing them, and verifying the result.

Everything runs through the `airpoint` CLI.

## Requirements

- **macOS** (Apple Silicon or Intel)
- **Airpoint app** — must be running. Download from [airpoint.app](https://airpoint.app).
- **Airpoint CLI** — the `airpoint` command must be on PATH. Install it from the Airpoint app: Settings → Plugins → Install CLI.

## Commands

### Ask the AI agent to do something (primary command)

This is the most important command. It sends a natural-language task to
Airpoint's built-in computer-use agent which can see the screen, move the
mouse, click, type, scroll, open apps via Spotlight, manage windows, and verify
its own actions.

```bash
# Synchronous — waits for the agent to finish (up to 5 min) and returns output
airpoint ask "open Safari and go to github.com"
airpoint ask "what's on my screen right now?"
airpoint ask "find the Slack notification and read it"
airpoint ask "open System Settings and enable Dark Mode"
airpoint ask "open Mail, find the latest email from John, and summarize it"

# Fire-and-forget — returns immediately
airpoint ask "open Spotify and play my liked songs" --no-wait

# Hidden mode — runs without showing the assistant panel on screen
airpoint ask "take a screenshot of the current window" --hidden
```

Use `--hidden` for background automation where you don't want the assistant
panel visible on screen.

### Capture a screenshot

```bash
airpoint see
```

Returns a screenshot of the current display. Useful for verifying state before
or after issuing an `ask` command.

### Check status

```bash
airpoint status
airpoint status --json
```

Returns app version and current state (tracking active, etc.).

### Hand tracking (secondary)

Airpoint also supports hands-free cursor control via camera-based hand tracking.
These commands start/stop that feature:

```bash
airpoint tracking on
airpoint tracking off
airpoint tracking        # show current state
```

### Read or change settings

```bash
airpoint settings list             # all current settings
airpoint settings list --json      # machine-readable
airpoint settings get cursor.sensitivity
airpoint settings set cursor.sensitivity 1.5
```

Common settings: `cursor.sensitivity` (default 1.0), `cursor.acceleration`
(default true), `scroll.sensitivity` (default 1.0), `scroll.inertia`
(default true).

### System vitals

```bash
airpoint vitals          # CPU, RAM, temperature
airpoint vitals --json
```

### Launch the app

```bash
airpoint open            # opens/focuses the Airpoint macOS app
```

## Tips

- **Use `airpoint ask` for almost everything.** The agent can read the screen,
  interact with any app, and chain multi-step workflows autonomously.
- Always use `--json` when you need to parse output programmatically.
- The agent can answer questions about what's on screen ("what app is in the
  foreground?", "read the error message in this dialog").
- Airpoint is a notarized, code-signed macOS app. Download it from
  [airpoint.app](https://airpoint.app).
