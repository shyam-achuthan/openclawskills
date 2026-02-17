# 5 Whys Methodology

The 5 Whys technique identifies root causes by asking "why" iteratively, drilling down from symptoms to underlying issues.

## Core Rules

1. **Evidence-based answers only**: Every "why" answer must cite specific evidence
2. **No speculation**: If you can't cite evidence, mark it as hypothesis and gather more data
3. **Stop at root cause**: May take fewer or more than 5 iterations
4. **Multiple paths possible**: Complex issues may have multiple root causes

## Template

```
Problem: [Observable issue with evidence]

Why 1: Why did [symptom] happen?
Evidence: [Log entry, file content, timestamp, system state]
Answer: Because [direct cause]

Why 2: Why did [direct cause] occur?
Evidence: [Log entry, file content, timestamp, system state]
Answer: Because [deeper cause]

Why 3: Why did [deeper cause] happen?
Evidence: [Log entry, file content, timestamp, system state]
Answer: Because [underlying issue]

Why 4: Why did [underlying issue] exist?
Evidence: [Log entry, file content, timestamp, system state]
Answer: Because [systemic problem]

Why 5 (Root Cause): Why did [systemic problem] exist?
Evidence: [Log entry, file content, timestamp, system state]
Answer: [Root cause - design flaw, missing feature, race condition, etc.]
```

## Evidence Citation Format

**Good citations:**
```
Evidence: Session log line 260 shows user message at 23:18:38.610Z with role="user"
Evidence: Gateway error log "AbortError: This operation was aborted" at 23:19:28.082Z
Evidence: Cache-TTL event at line 259, timestamp 23:18:38.603Z (7ms before message)
```

**Bad citations (speculation):**
```
Evidence: The system probably crashed
Evidence: It might have been a network issue
Evidence: Cache was likely full
```

## When to Stop

Stop when you reach:
- **Design limitation**: "Feature X was not implemented"
- **Race condition**: "Process A and B conflict when simultaneous"
- **Configuration error**: "Setting Y was misconfigured"
- **Resource constraint**: "System ran out of memory/connections/etc"

## Multiple Root Causes

Some problems have multiple contributing factors:

```
Problem: Message dropped

Path 1 (Timing):
Why 1 → Why 2 → Root: No queue during cache transitions

Path 2 (Architecture):
Why 1 → Why 2 → Root: No retry logic for aborted operations

Path 3 (Monitoring):
Why 1 → Why 2 → Root: No alerting for dropped messages
```

Document all paths and recommend addressing each.

## Example: Message 2010 Delivery Failure

**Problem:** User message 2010 received at 15:18 PST was not responded to

**Why 1:** Why didn't assistant respond to message 2010?
- **Evidence:** Session log line 260 shows user message at 23:18:38.610Z, but no assistant message follows (line 261 is cache-ttl, line 262 is next user message at 23:22:23)
- **Answer:** The gateway did not generate an assistant turn for message 2010

**Why 2:** Why didn't the gateway generate an assistant turn?
- **Evidence:** 
  - Cache-TTL event at line 259: 23:18:38.603Z
  - Message 2010 at line 260: 23:18:38.610Z (7ms later)
  - Gateway error log: "AbortError: This operation was aborted" at 23:19:28.082Z
- **Answer:** Turn generation was aborted during execution

**Why 3:** Why was turn generation aborted?
- **Evidence:** 
  - Error occurred 50 seconds after message arrival
  - Cache-TTL event happened at exact same timestamp as message
  - No other gateway activity between 23:14 and 23:34
- **Answer:** Cache expiry handling interrupted message processing

**Why 4:** Why does cache expiry interrupt message processing?
- **Evidence:**
  - Message logged to session JSONL (proof receipt worked)
  - Parent chain broken: message 2013 points to new cache-ttl (line 261), not message 2010 (line 260)
  - User had to manually retry 4 minutes later
- **Answer:** Gateway lacks queue handling for in-flight messages during cache transitions

**Why 5 (Root Cause):** Why doesn't gateway queue in-flight messages during cache transitions?
- **Evidence:** Community member reported similar issue with pruning mode transitions (GitHub comment)
- **Answer:** Gateway was designed assuming cache transitions occur between turns (safe moments), not during active message processing. Missing feature: message queue or double-buffer for state transitions.

**Recommendation:** 
1. Add message queue to hold incoming messages during cache operations
2. Implement retry logic for aborted turn generation
3. Add monitoring/alerting for dropped messages
4. Consider double-buffer pattern as suggested by community
