---
name: ultra-agent-stinct
description: "Autonomous coding, debugging, and code maintenance. Use when the user asks to: fix a bug, debug an error, write code or scripts, run tests, review or refactor code, investigate stack traces or logs, make git commits, add a feature, or any coding task. Triggers: 'fix this', 'debug', 'write code', 'run tests', 'check the error', 'look at the code', 'commit', 'what's wrong with', 'refactor', 'add a feature', 'build', 'deploy', 'install'."
version: 1.0.1
author: grimmjoww
homepage: https://github.com/grimmjoww/ultra-agent-stinct
metadata: {"openclaw": {"emoji": "\u26a1", "os": ["darwin", "linux", "win32"]}}
---

# Ultra Agent Stinct

Autonomous debugging, code writing, and project maintenance. Trust your instincts — read, understand, fix.

## Safety Rules (ALWAYS)

1. **Read before edit.** Never `edit` without `read` first — exact text match required or it fails
2. **`write` overwrites entirely.** Use `edit` for changes to existing files
3. **Never delete without asking.** Prefer safe deletion over `rm -rf`
4. **Never push without asking.** `git push` only when the user explicitly says to
5. **Never commit without asking.** Stage and commit only on request
6. **Backup awareness.** Before large refactors, suggest a branch or stash

## Debug Workflow

When the user reports a bug or error:

**1. Reproduce** — Run the failing command:
```
exec command:"<failing command>" workdir:"<project dir>"
```

**2. Read the error** — Parse the stack trace. Identify file + line number.

**3. Read the code** — Read the relevant file(s):
```
read path:"<file from stack trace>"
```

**4. Trace the cause** — Follow the call chain. Read imports, dependencies, config. Check for:
- Typos, wrong variable names
- Missing imports or dependencies
- Type mismatches, null/undefined access
- Wrong paths, missing env vars
- Logic errors in conditionals

**5. Fix** — Apply the minimal correct fix:
```
read path:"<file>"
edit path:"<file>" old:"<exact broken code>" new:"<fixed code>"
```

**6. Verify** — Re-run the original failing command. Confirm the fix works.

**7. Explain** — Tell the user what was wrong and what you changed (brief).

## Write Code Workflow

**1. Understand the project** — Check existing patterns:
```
exec command:"ls -la" workdir:"<project dir>"
```
Read `package.json`, `pyproject.toml`, `Cargo.toml`, or equivalent. Read existing similar files to match style, conventions, imports.

**2. Plan first** — Before writing, outline what you'll create. Think through the structure, dependencies, and edge cases.

**3. Write** — Create the file:
```
write path:"<new file path>" content:"<complete file content>"
```

**4. Verify** — Run linting, type checking, or the feature:
```
exec command:"<appropriate test command>" workdir:"<project dir>"
```

## Test Workflow

**1. Find the test runner** — Check the project manifest for test scripts:
- **Node.js**: `npm test` / `npx jest` / `npx vitest`
- **Python**: `pytest` / `python -m unittest`
- **Rust**: `cargo test`
- **Go**: `go test ./...`

**2. Run tests:**
```
exec command:"<test command>" workdir:"<project>" timeout:120
```

**3. On failure:** Read the failing test, read the source under test, apply Debug Workflow.

**4. On success:** Report summary (passed, skipped, failed counts).

## Git Integration

Only when the user asks to commit, stage, or check git status.

```
exec command:"git status" workdir:"<project>"
exec command:"git diff --stat" workdir:"<project>"
exec command:"git add <specific files>" workdir:"<project>"
exec command:"git commit -m '<message>'" workdir:"<project>"
```

For detailed git workflows, see [references/git-workflow.md](references/git-workflow.md).

## Spawning Coding Agents (Heavy Tasks)

For large tasks (multi-file refactors, entire features, long builds), spawn a background agent:

```
exec pty:true workdir:"<project>" background:true command:"claude '<detailed task>'"
```

Monitor:
```
process action:list
process action:log sessionId:<id>
process action:poll sessionId:<id>
```

See [references/escalation-guide.md](references/escalation-guide.md) for when to self-handle vs delegate.

## Cross-Platform Quick Reference

| Task | macOS/Linux | Windows (Git Bash) |
|------|-------------|-------------------|
| Find files | `find . -name "*.ts" -not -path "*/node_modules/*"` | Same |
| Search code | `grep -rn "pattern" --include="*.ts" .` | Same |
| Process list | `ps aux \| grep node` | `tasklist \| findstr node` |
| Kill process | `kill -9 <PID>` | `taskkill //f //pid <PID>` |
| Python | `python3` (or `python`) | `python` |
| Open file | `open <file>` | `start <file>` |

## Context Management

- Keep tool calls focused — one task per chain
- Don't read files already in your system prompt
- For large files, read targeted sections rather than the whole thing
- If context is getting heavy, summarize findings before continuing
