# Log Analysis Techniques

Practical patterns for extracting evidence from OpenClaw logs.

## Session JSONL Analysis

Session logs are stored at: `~/.openclaw/agents/AGENT_NAME/sessions/SESSION_ID.jsonl`

### Find Specific Messages

**By message ID:**
```bash
jq 'select(.id == "ffb67afd")' SESSION.jsonl
```

**By message number (from Telegram/Discord):**
```bash
jq 'select(.message.content[].text | contains("message_id: 2010"))' SESSION.jsonl
```

**By timestamp:**
```bash
jq 'select(.timestamp >= "2026-02-14T23:18:00Z" and .timestamp <= "2026-02-14T23:20:00Z")' SESSION.jsonl
```

**By role:**
```bash
jq 'select(.message.role == "user")' SESSION.jsonl
jq 'select(.message.role == "assistant")' SESSION.jsonl
```

### Trace Message Chains

**Find message and its parent:**
```bash
MESSAGE_ID="ffb67afd"
jq "select(.id == \"$MESSAGE_ID\" or .parentId == \"$MESSAGE_ID\")" SESSION.jsonl
```

**Build conversation thread:**
```bash
# Show ID -> parentID relationships
jq -r '.id + " -> " + .parentId' SESSION.jsonl
```

**Find orphaned messages (parent doesn't exist):**
```bash
# Extract all IDs
jq -r '.id' SESSION.jsonl > all_ids.txt
# Extract all parent IDs
jq -r '.parentId' SESSION.jsonl | sort -u > all_parents.txt
# Find parents that don't have corresponding IDs
comm -13 all_ids.txt all_parents.txt
```

### Extract Context

**Show message sequence with metadata:**
```bash
jq -c '{line: input_line_number, id, parentId, role: .message.role, type, timestamp: .timestamp[0:19]}' SESSION.jsonl
```

**Get specific line range:**
```bash
sed -n '260,265p' SESSION.jsonl | jq '.'
```

**Show thinking blocks:**
```bash
jq 'select(.message.content[]? | .type == "thinking") | .message.content[] | select(.type == "thinking") | .thinking' SESSION.jsonl
```

### Performance Analysis

**Count message types:**
```bash
jq -r '.type' SESSION.jsonl | sort | uniq -c
```

**Average response time:**
```bash
jq -r 'select(.message.role == "assistant") | .timestamp' SESSION.jsonl | \
  awk '{if (prev) print $0 " " prev; prev=$0}' | \
  # Calculate time differences
```

## Gateway Log Analysis

Gateway logs: `~/.openclaw/logs/gateway.log` and `gateway.err.log`

### Find Events by Time

**Specific timestamp:**
```bash
grep "2026-02-14T23:18" gateway.log
```

**Time range:**
```bash
awk '/2026-02-14T23:18:/,/2026-02-14T23:22:/' gateway.log
```

**Around specific time (context):**
```bash
grep -C 10 "2026-02-14T23:18:38" gateway.log
```

### Filter by Component

**Telegram events:**
```bash
grep "\[telegram\]" gateway.log
```

**Error events:**
```bash
grep "ERROR\|WARN" gateway.log
```

**Session events:**
```bash
grep "\[session\]" gateway.log
```

### Correlate Logs

**Find gateway events matching session timestamps:**
```bash
# Extract timestamp from session log
SESSION_TIME=$(jq -r 'select(.id == "MESSAGE_ID") | .timestamp[0:19]' SESSION.jsonl)

# Find in gateway log
grep "$SESSION_TIME" gateway.log
```

**Timeline view (multiple logs):**
```bash
# Merge logs with timestamps
{ sed 's/^/[session] /' SESSION.jsonl; \
  sed 's/^/[gateway] /' gateway.log; \
} | sort -k2
```

## Error Log Patterns

### Common Error Types

**AbortError:**
```bash
grep "AbortError" gateway.err.log
```

**Connection errors:**
```bash
grep -E "ECONNREFUSED|ETIMEDOUT|ENOTFOUND" gateway.err.log
```

**API errors:**
```bash
grep -E "400|401|403|404|429|500|502|503" gateway.err.log
```

### Context Around Errors

**Show 5 lines before and after error:**
```bash
grep -C 5 "ERROR" gateway.err.log
```

**Group errors by type:**
```bash
grep "ERROR" gateway.err.log | \
  sed 's/.*ERROR: //' | \
  sed 's/ at .*//' | \
  sort | uniq -c | sort -rn
```

## Timestamp Analysis

### Parse Timestamps

**ISO 8601 format:**
```bash
# Extract hour:minute
jq -r '.timestamp[11:16]' SESSION.jsonl

# Extract full timestamp
jq -r '.timestamp[0:19]' SESSION.jsonl
```

**Convert to epoch:**
```bash
date -d "2026-02-14T23:18:38Z" +%s
```

### Find Time Gaps

**Detect gaps > 5 minutes:**
```bash
jq -r '.timestamp' SESSION.jsonl | \
  awk '{
    if (prev) {
      cmd = "date -d " prev " +%s"
      cmd | getline t1
      close(cmd)
      cmd = "date -d " $0 " +%s"
      cmd | getline t2
      close(cmd)
      diff = t2 - t1
      if (diff > 300) print prev " -> " $0 " (" diff " seconds)"
    }
    prev = $0
  }'
```

## Advanced Patterns

### Extract Specific Fields

**Message content preview:**
```bash
jq -r 'select(.message.role == "user") | .message.content[0].text[0:100]' SESSION.jsonl
```

**Custom fields:**
```bash
jq -c '{id, timestamp: .timestamp[0:19], text: .message.content[0].text[0:50]}' SESSION.jsonl
```

### Correlate Session and Gateway

**Find all logs related to a session:**
```bash
SESSION_KEY="9e0c39c5-f122-484d-a7c2-518774537374"
grep "$SESSION_KEY" gateway.log
```

**Match message processing:**
```bash
MESSAGE_ID="ffb67afd"
grep "$MESSAGE_ID" gateway.log gateway.err.log
```

## Sanitization

Before sharing logs, remove:

**Personal identifiers:**
```bash
sed 's/id:[0-9]\+/id:REDACTED/' SESSION.jsonl
sed 's/user_[0-9]\+/user_REDACTED/' gateway.log
```

**Sensitive content:**
```bash
# Replace message text
jq '.message.content[0].text = "[REDACTED]"' SESSION.jsonl
```

**Tokens/keys:**
```bash
sed 's/token=[^ ]*/token=REDACTED/' gateway.log
sed 's/api_key=[^ ]*/api_key=REDACTED/' gateway.log
```

## Example Investigation

**Problem:** Find why message 2010 wasn't responded to

```bash
# 1. Find message 2010 in session log
grep -n "message_id: 2010" SESSION.jsonl
# Result: Line 260

# 2. Extract that message
sed -n '260p' SESSION.jsonl | jq '.'
# Result: Message at 23:18:38.610Z, id=ffb67afd

# 3. Check context (before/after)
sed -n '258,262p' SESSION.jsonl | jq -c '{line: input_line_number, id, parentId, type}'

# 4. Look for errors around that time
grep "23:18\|23:19" gateway.err.log
# Result: AbortError at 23:19:28

# 5. Find cache events
jq 'select(.type == "custom" and .customType == "openclaw.cache-ttl")' SESSION.jsonl | \
  jq -c '{id, timestamp: .timestamp[0:19]}'
# Result: cache-ttl at 23:18:38.603Z (7ms before message)

# Conclusion: Message arrived during cache transition, turn generation aborted
```
