# Issue Reporting

Templates and guidelines for reporting bugs and problems with clear evidence.

## General Template

```markdown
**Title:** [Concise description of the bug]

**Description:**

### Summary
[1-2 sentence overview of the problem]

### Background (if needed)
[Context about the feature/system for readers unfamiliar with internals]

### Evidence
[Concrete evidence from logs, files, or system state]

**From session logs:**
```
[Quoted log entries with line numbers and timestamps]
```

**From gateway/error logs:**
```
[Quoted error messages with timestamps]
```

### Expected Behavior
[What should have happened]

### Actual Behavior
[What actually happened]

### Root Cause Analysis
[5 Whys or other analysis showing why the bug occurred]

1. [Direct cause with evidence]
2. [Deeper cause with evidence]
3. [Underlying issue with evidence]
4. [Systemic problem with evidence]
5. [Root cause]

### Proposed Solution
1. [Primary fix recommendation]
2. [Additional improvements]
3. [Prevention measures]

### Impact
- [User experience impact]
- [Frequency/severity assessment]
- [Affected components/channels]

### Reproducibility
[Unknown | Timing-dependent | Consistently reproducible with steps: ...]
```

## OpenClaw-Specific Template

For OpenClaw GitHub issues:

```markdown
**Title:** [Concise description - mention if it's gateway-core or channel-specific]

**Description:**

### Summary
[1-2 sentences describing the observable bug]

### Background: [Feature/System Name]

[Brief explanation of the feature for context, e.g.:]

OpenClaw uses [feature X] to [achieve Y]. When [condition Z]:
1. [Step 1]
2. [Step 2]
3. [Expected outcome]

This optimization/feature is important because [reason].

### Evidence
From session JSONL logs:

```
Line X: [description] at [timestamp] (message ID: [id])
Line Y: [description] at [timestamp] (parent ID: [id])
```

Gateway error log:
```
[timestamp]: [error message]
```

### Expected Behavior
All [actions] should [expected outcome], regardless of [condition].

### Actual Behavior
[Action] at line X was [what happened]. [Impact statement].

### Root Cause Analysis
Likely race condition in gateway core (affects all channels - Telegram, Discord, Signal, CLI, etc.):

1. [Step in process]
2. [Detection/trigger event]
3. [Action taken]
4. [Missing retry/recovery]
5. [Result - orphaned/lost data]

### Proposed Solution
1. [Primary solution with implementation hint]
2. [Secondary improvement]
3. [Monitoring/detection addition]

### Impact
- [User-facing problem]
- [Conversation/workflow disruption]
- [Required workaround]
- [Scope: which channels/components]

### Reproducibility
[Assessment and any clues about conditions]
```

## Sanitization Checklist

Before submitting, remove or redact:

- [ ] Personal identifiers (user IDs, phone numbers, email addresses)
- [ ] Real names (unless publicly associated with the project)
- [ ] Message content (replace with "[REDACTED]" or generic placeholders)
- [ ] Session keys and tokens
- [ ] API keys or credentials
- [ ] Private repository names or paths
- [ ] IP addresses or internal hostnames (replace with "127.0.0.1", "example.com")
- [ ] Specific file paths (use relative paths or "~/.openclaw/...")

**Safe to include:**
- Timestamps (adjust to UTC if needed)
- Message IDs (they're session-local, not sensitive)
- Error types and stack traces (without sensitive values)
- Log structure and format
- Component names and types

## Examples

### Example 1: Message Dropped During Cache Transition

**Title:** Message dropped during cache-TTL transition - no assistant turn generated

**Summary:**
User messages that arrive within milliseconds of a cache-TTL event are silently dropped without generating an assistant turn. The gateway does not retry message processing after cache transitions complete.

**Background: Prompt Caching in OpenClaw**

OpenClaw uses Anthropic's prompt caching feature to reduce costs and latency. When making API calls to Claude, frequently-reused content (system prompts, skill definitions, memory files, context documents) can be cached for up to 5 minutes. Cached tokens cost significantly less than uncached tokens.

The `openclaw.cache-ttl` events in session logs mark when cached prompt segments expire. When a cache expires during an active session:
1. Gateway detects the 5-minute TTL has passed
2. Next API call must re-cache the expired content
3. Cache write tokens are charged (more expensive than cache reads)

This optimization is critical for OpenClaw's economics - sessions load substantial context (skills, memory, system prompts) that would be expensive to re-send uncached on every turn.

**Evidence:**

From session JSONL logs:
```
Line 258: Assistant message at T+0ms (last successful turn)
Line 259: cache-ttl event at T+1260s.603ms
Line 260: User message at T+1260s.610ms (7ms after cache event)
Line 261: cache-ttl event at T+1485s (different parent chain)
Line 262: User message at T+1485s (user followup asking to process previous)
Line 263: Assistant response to line 262, thinking block shows "I don't see message [from line 260] in this current context"
```

Gateway error log:
```
T+1268s: [openclaw] Suppressed AbortError: AbortError: This operation was aborted
```

**Expected Behavior:**
All user messages should generate assistant turns, regardless of cache state transitions.

**Actual Behavior:**
Message at line 260 was logged to session JSONL but no assistant turn was generated. User had to send followup message 4 minutes later to get a response.

**Root Cause Analysis:**
Likely race condition in gateway core (affects all channels - Telegram, Discord, Signal, CLI, etc.):

1. Gateway starts processing user message
2. Detects cache expiry during turn generation
3. Aborts current operation for cache refresh
4. Does not retry message processing after cache update completes
5. Message remains in session log but orphaned from conversation tree

**Proposed Solution:**
1. Add retry logic for aborted turn generation
2. Queue incoming messages during cache transitions instead of aborting
3. Separate cache management from message processing pipeline
4. Add monitoring/alerting for dropped messages

**Impact:**
- Messages silently dropped create user confusion
- Lost context disrupts conversation continuity
- Users must manually retry, degrading experience
- Affects all communication channels (gateway-core issue)

**Reproducibility:**
Unknown - appears timing-dependent on cache-TTL coinciding with message arrival within ~10ms window.

---

### Example 2: Telegram Reply Chain Broken

**Title:** Telegram reply metadata not mapped to session parent chain

**Summary:**
When users reply to previous Telegram messages, the reply metadata is captured as text annotation but not used to set parentId in session messages, breaking conversation threading.

**Evidence:**

From session JSONL:
```
Line 260: Message 2010 (id: ffb67afd, parentId: 0a68f806)
Line 262: Message 2013 text contains "[Replying to Chunhua Liao id:2010]" but parentId: 3741da4b (not ffb67afd)
```

**Expected Behavior:**
When Telegram message 2013 replies to message 2010, the session should link them via parentId.

**Actual Behavior:**
Reply metadata appears only as text annotation. Session parent chain uses cache-ttl as parent instead of the actual message being replied to.

**Root Cause:**
The Telegram channel plugin does not:
1. Parse "[Replying to ... id:XXXX]" metadata
2. Look up message_id XXXX in session history
3. Find corresponding session message id
4. Set that as parentId

**Proposed Solution:**
Add reply resolution to Telegram plugin:
1. Extract reply message_id from metadata
2. Query session history for matching message_id annotation
3. Use found session id as parentId
4. Fallback to current behavior if lookup fails

**Impact:**
- Assistant cannot see conversation context when users reply
- Reduces utility of Telegram's reply feature
- Forces users to repeat context

**Reproducibility:**
Consistently reproducible - any Telegram reply will show this behavior.
