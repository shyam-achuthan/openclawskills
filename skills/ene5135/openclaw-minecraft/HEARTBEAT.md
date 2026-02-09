# Heartbeat

## Minecraft Autonomy (every 2 minutes)
1. Health check: `GET https://56eb-125-246-120-211.ngrok-free.app/health`.
2. Auth token:
   - If `memory/mc-auth.json` missing or `accessToken` empty, call:
     `POST https://56eb-125-246-120-211.ngrok-free.app/v1/auth/open/register` with `{"agentName":"<your-agent-name>"}`.
   - Save response to `memory/mc-auth.json`.
   - Use `accessToken` (or `MC_CONTROLLER_TOKEN` if set) for all API calls.
3. Ensure bot exists:
   - `GET /v1/bots` and check for `botId`.
   - If missing, `POST /v1/bots` with `{ "botId":"<botId>", "username":"<botId>" }`.
4. Ensure bot connected (every heartbeat):
   - `GET /v1/bots/{botId}` and check `status`.
   - If `status` is `connected`, continue.
   - If `status` is `connecting`, wait 2 seconds and end this heartbeat.
   - If `status` is `kicked`, `error`, or `disconnected`, call `POST /v1/bots/{botId}/connect`.
   - If connect fails, record the error in `memory/mc-autonomy.json` and end this heartbeat.
5. Observe: `GET /v1/bots/{botId}/state`.
6. If `metadata.currentTaskId` exists, wait 2 seconds and end this heartbeat.
7. Plan: decide ONE safe action based on `nearby`, `health`, `hunger`.
8. Announce plan in Minecraft chat:
   - Template: `[plan] <one short sentence>`
   - Example: `[plan] Heading to nearby oak to gather wood.`
   - `POST /v1/bots/{botId}/act` with `action: "chat"` and the template above.
9. Act: `POST /v1/bots/{botId}/act` using `mode: until` or `mode: loop` and set `timeoutMs`.
10. Log decisions in `memory/mc-autonomy.json` with timestamps.

## Decision Hints
- If health is low, move to a safe spot or stop.
- If idle, explore by moving to a nearby random point.
- If interesting blocks are nearby, move closer and inspect.
- Avoid spamming actions; one action per heartbeat.
