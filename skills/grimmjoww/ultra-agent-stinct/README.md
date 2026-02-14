# Ultra Agent Stinct

Autonomous coding, debugging, and code maintenance skill for [OpenClaw](https://openclaw.ai) agents. Structured debug workflows, code writing, test running, git integration, and coding agent escalation. Cross-platform.

Like Goku's Ultra Instinct, but for code — trust your instincts, read, understand, fix.

## Install

```bash
clawhub install ultra-agent-stinct
```

Or clone into your workspace skills directory:
```bash
cd <your-workspace>/skills
git clone https://github.com/grimmjoww/ultra-agent-stinct.git
```

Then enable in your `clawdbot.json`:
```json
{
  "skills": {
    "entries": {
      "ultra-agent-stinct": {
        "enabled": true
      }
    }
  }
}
```

## What It Does

Gives your OpenClaw agent structured workflows for:

- **Debugging** — 7-step workflow: reproduce, read error, read code, trace cause, fix, verify, explain
- **Code Writing** — Plan-first approach: understand project, plan, write, verify
- **Test Running** — Auto-detect test runner (Node.js, Python, Rust, Go), run tests, handle failures
- **Git Integration** — Status, diff, stage, commit (only when the user asks)
- **Escalation** — Knows when to handle it directly vs spawn a background coding agent for heavy tasks

## Safety Built In

- Always reads before editing (exact text match required)
- Never deletes, pushes, or commits without explicit permission
- Suggests branches/stashes before large refactors

## Cross-Platform

Works on macOS, Linux, and Windows (Git Bash). Includes a quick reference table with platform-specific commands.

## References

- `references/git-workflow.md` — Branching, stashing, PRs, merge conflicts, commit style
- `references/escalation-guide.md` — When to self-handle vs spawn a coding agent

## Requirements

- [OpenClaw](https://openclaw.ai) (any version with skill support)
- Optional: A coding agent CLI (Claude Code, Codex, Aider) for heavy task delegation

## License

MIT
