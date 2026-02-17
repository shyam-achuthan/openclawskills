---
name: evidence-based-investigation
description: "Investigate problems using evidence-based analysis with session logs, error logs, and 5 Whys methodology. Use when debugging OpenClaw issues, analyzing system failures, tracing message delivery problems, or conducting root cause analysis that requires hard evidence from logs, files, or system state rather than assumptions."
---

# Evidence-Based Investigation

Investigate problems systematically using hard evidence from logs, files, and system state.

## Core Principles

1. **Evidence over assumptions**: Every claim must be backed by log entries, file contents, or observable state
2. **Follow the data trail**: Trace IDs, timestamps, and parent chains through session logs
3. **5 Whys with citations**: Each "why" answer must cite specific evidence
4. **Document clearly**: Write findings that others can verify independently

## Investigation Workflow

### 1. Identify the Problem

Define the observable issue with specifics:
- What was expected?
- What actually happened?
- When did it occur? (exact timestamps)
- What evidence shows the problem exists?

**Decision Point Analysis:**
Before investigating technical failures, check if the problem stems from a bad decision:
- Was the right tool/approach chosen for the task?
- Were there obvious warning signs (file extensions, error messages, constraints)?
- What information was available at decision time?
- What alternatives should have been considered?
- Did the decision violate known best practices?

Example: Using `web_fetch` on a `.pdf` URL is a decision error, not a technical failure.

### 2. Gather Evidence

**Session Logs:**
```bash
# Find relevant messages by ID or timestamp
jq 'select(.id == "MESSAGE_ID")' ~/.openclaw/agents/AGENT/sessions/SESSION.jsonl

# Trace message chain by parentId
jq 'select(.id == "ID" or .parentId == "ID")' SESSION.jsonl

# Filter by timestamp range
jq 'select(.timestamp >= "2026-02-14T23:18:00Z" and .timestamp <= "2026-02-14T23:20:00Z")' SESSION.jsonl
```

**Gateway Logs:**
```bash
# Search by timestamp
grep "2026-02-14T23:18" ~/.openclaw/logs/gateway.log

# Find errors around time
grep -C 10 "2026-02-14T23:18" ~/.openclaw/logs/gateway.err.log
```

**System State:**
```bash
# Check process state
ps aux | grep openclaw

# Check file timestamps
ls -la --time-style=full-iso FILE
```

### 3. Analyze with 5 Whys

See [5-whys.md](references/5-whys.md) for detailed methodology.

**Step A: Check Decision Points First**

Before analyzing technical "why", verify the approach was sound:
```
Decision Point 1: Was the chosen tool/method appropriate?
Evidence: [URL/context/constraints visible at decision time]
Assessment: [Correct choice / Wrong tool / Missing validation]

Decision Point 2: Were there warning signs that should have triggered different action?
Evidence: [File extension, error message, documentation, constraints]
Assessment: [Warning heeded / Warning ignored / No warning available]
```

**Step B: Technical 5 Whys**

Only after validating decision points, run technical analysis:

```
Why 1: Why did X happen?
Evidence: [specific log entry, file content, timestamp]
Answer: Because Y

Why 2: Why did Y occur?
Evidence: [specific log entry, file content, timestamp]
Answer: Because Z

... continue to root cause
```

**Critical:** If Step A reveals a decision error, the root cause is the bad decision, not the technical failure that followed.

### 4. Document Findings

Structure findings clearly:

**Evidence Section:**
- Quote exact log entries
- Include timestamps
- Show file paths and line numbers
- Link related evidence

**Analysis Section:**
- 5 Whys with evidence citations
- Root cause identification
- Impact assessment

**Recommendations:**
- Proposed fixes
- Prevention measures
- Monitoring improvements

### 5. Report Issues

See [issue-reporting.md](references/issue-reporting.md) for templates.

Include:
- Clear title describing the bug
- Summary of observable behavior
- Evidence from logs/files (sanitized)
- Root cause analysis
- Proposed solutions
- Reproducibility assessment

## Log Analysis Techniques

See [log-analysis.md](references/log-analysis.md) for detailed patterns.

**Session JSONL:**
```bash
# Extract message chain
jq -c '{id, parentId, role: .message.role, type, timestamp: .timestamp[0:19]}' SESSION.jsonl

# Find gaps in chain
jq -r '.id + " -> " + .parentId' SESSION.jsonl | grep "MISSING_ID"
```

**Timestamp Correlation:**
```bash
# Find events within 1 second
awk '/23:18:[0-9][0-9]/' gateway.log
```

## Common Pitfalls

- **Speculation without evidence**: Always cite sources
- **Incomplete evidence**: Check all relevant logs (session, gateway, error)
- **Missing context**: Look before and after the problem timestamp
- **Assuming causation**: Correlation needs additional evidence
- **Sanitization failures**: Remove personal info before sharing

## Example Investigations

### Example 1: Technical Failure (Message Delivery)

**Problem:** User message 2010 was not responded to

**Evidence:**
```
Line 260: User message at 23:18:38.610Z (message ID: ffb67afd)
Line 259: cache-ttl event at 23:18:38.603Z (7ms before)
Gateway error log: AbortError at 23:19:28.082Z
```

**Decision Point Analysis:**
- Tool choice: Message sending via session API (correct)
- No decision errors identified - technical investigation needed

**5 Whys:**
1. Why no response? → No assistant turn generated (evidence: no message after line 260)
2. Why no turn? → Turn generation aborted (evidence: AbortError in logs)
3. Why aborted? → Cache transition interrupted processing (evidence: 7ms timing)
4. Why does cache interrupt? → No queue handling during cache refresh
5. Root: Gateway lacks message queue for cache transitions

**Result:** GitHub issue filed with evidence, engaged community for solutions

---

### Example 2: Decision Point Failure (PDF Extraction)

**Problem:** PDF fetch returned binary data instead of text

**Evidence:**
```
URL: https://resources.anthropic.com/hubfs/guide.pdf (ends in .pdf)
Tool used: web_fetch (HTML extraction tool)
Result: extractor: "raw", binary data returned
```

**Decision Point Analysis:**
- **Decision Error Identified:** Used `web_fetch` on `.pdf` URL
- **Warning Signs:** 
  - URL clearly ends in `.pdf` extension
  - Tool description states "HTML → markdown/text"
  - No PDF parsing capability documented
- **Evidence at decision time:** URL extension visible, tool docs available
- **Should have:** Used browser tool or download + PDF parser
- **Root Cause:** Wrong tool selection, not tool limitation

**5 Whys (Not Needed):**
Technical "why web_fetch failed" is irrelevant - the decision to use it was wrong from the start.

**Result:** 
- Update investigation skill to check decision points first
- Update skill-engineer to validate tool choice against input type
- Add pre-execution validation (URL extension → tool mapping)
