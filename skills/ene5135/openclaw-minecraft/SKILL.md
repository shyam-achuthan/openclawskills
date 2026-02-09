---
name: OpenClaw Minecraft
version: 0.1.0
specialty: minecraft-control
category: tools
description: Control Minecraft bots through a Mineflayer controller API using JSON actions and heartbeat autonomy.
---

# Mineflayer Controller Skill

Use this skill to create and control Minecraft bots via a controller API. The controller executes only JSON actions. Do not send API keys or other secrets to the controller. The agent performs LLM reasoning locally and only sends actions.

## Register First (Open Registration)
If open registration is enabled, the agent can self-issue a token:
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/auth/open/register" \
  -H "Content-Type: application/json" \
  -d '{"agentName":"andy"}'
```

Recommended: store the response in `memory/mc-auth.json` and reuse the `accessToken` for future calls.

## Requirements
- Base URL: `https://56eb-125-246-120-211.ngrok-free.app/v1`
- `MC_CONTROLLER_TOKEN` (agent-specific JWT)

To obtain a JWT, an operator should call `POST /v1/auth/register` with the master issuer secret and share the returned `accessToken` with the agent. Refresh tokens can be rotated via `POST /v1/auth/refresh`.

If you don't want to share the master secret, the controller can expose `POST /v1/auth/proxy/register` with allowlist + rate-limit. In that mode, the agent requests an access token using a `proxyKey`.

If open registration is enabled (`POST /v1/auth/open/register`), the agent can request an access token without a proxy key. This is less secure and should only be used when you accept open access.

## Safety Rules
- Never send LLM API keys to the controller.
- Only control bots owned by your token.
- Prefer `queue: queue` unless you must interrupt a running task.

## Workflow
1. Ensure the bot exists; create it if missing.
2. Connect the bot to the Minecraft server.
3. Read state for current context.
4. Send an action request.
5. Poll task status or subscribe to events.

## Autonomous Loop
For autonomous behavior, repeat:
1. `GET /bots/{botId}/state`
2. If `metadata.currentTaskId` is set, wait briefly and loop.
3. Decide one safe action and send it via `POST /bots/{botId}/act`.
4. Use `mode: until` or `mode: loop` with `timeoutMs`.

## Heartbeat Integration
OpenClaw supports periodic heartbeats. If a `HEARTBEAT.md` file exists in the workspace root, it will be used for scheduled autonomous actions.

After installing this skill, copy or merge:
- `skills/openclaw-minecraft/HEARTBEAT.md` -> `HEARTBEAT.md` (workspace root)

## API Patterns

### Create bot
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/bots" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"botId":"andy","username":"andy"}'
```

### Connect bot
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/bots/andy/connect" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"host":"127.0.0.1","port":25565,"version":"1.21.9"}'
```

### Read state
```bash
curl -sS -X GET "https://56eb-125-246-120-211.ngrok-free.app/v1/bots/andy/state" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN"
```

### Send action (loop)
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/bots/andy/act" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action":"chat",
    "params":{"message":"hello"},
    "mode":"loop",
    "intervalMs":2000,
    "maxIterations":3
  }'
```

### Send action (until)
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/bots/andy/act" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action":"move_to",
    "params":{"x":10,"y":64,"z":-12},
    "mode":"until",
    "stopCondition":{"type":"reach_position","radius":1.5},
    "timeoutMs":60000
  }'
```

## Action Guidance
- Convert natural-language goals to **one** JSON action at a time.
- If the goal requires multiple steps, sequence them and wait for each task to finish.
- Use `mode: until` for navigation or repeated tasks.
- Use `mode: loop` for periodic actions (e.g., scanning, chat).

## Known Limitations
- JSON-only payloads for now. Media/attachments are not supported yet.
- Actions are best-effort and may fail if the bot is not connected or lacks items.
