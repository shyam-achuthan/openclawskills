# Skill: OpenExec — Governed Deterministic Execution

## Summary

OpenExec provides a governed execution interface for AI agents that must perform real-world actions.

It enforces a strict invariant:

> No execution occurs without external governance approval.

This skill separates reasoning, authorization, and execution into independent layers.

---

## Category

Infrastructure / Governance / Execution

---

## What This Skill Does

- Accepts structured execution requests
- Requires explicit governance approval (via ClawShield)
- Executes actions deterministically
- Emits immutable execution receipts (via ClawLedger)

---

## What This Skill Does NOT Do

- Does not define policy
- Does not grant permissions
- Does not reason autonomously
- Does not self-authorize execution
- Does not override governance decisions

---

## Architecture Context

This skill operates within a three-layer governed execution system:

- OpenExec — Deterministic execution engine
- ClawShield — Governance and approval gate
- ClawLedger — Immutable witness ledger

Each layer is independent and replaceable.

---

## Inputs

Structured execution request:

```json
{
  "action": "string",
  "parameters": {},
  "requested_by": "agent-id",
  "timestamp": "ISO-8601"
}
```

---

## Outputs

```json
{
  "status": "executed | denied",
  "execution_id": "uuid",
  "receipt_hash": "string",
  "timestamp": "ISO-8601"
}
```
