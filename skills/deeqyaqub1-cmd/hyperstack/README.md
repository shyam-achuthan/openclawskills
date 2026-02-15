# HyperStack — Developer-Controlled Knowledge Graph Memory for AI Agents

**Your agent controls the graph, not an LLM hallucination.**

HyperStack gives AI agents persistent memory with a knowledge graph. Store knowledge as typed cards (~350 tokens) with explicit linked relations. Retrieve via hybrid semantic + keyword search or graph traversal. Time-travel to debug past decisions.

## Why HyperStack?

- **Explicit control** — Your agent defines cards and links directly. No LLM auto-extraction, no phantom relationships, no extraction cost.
- **Time-travel debugging** — Query the graph at any timestamp. See what your agent knew when it made a bad decision. "Git blame for agent memory."
- **Zero LLM cost** — Mem0 and Zep charge ~$0.002 per memory operation (LLM extraction). HyperStack: $0.
- **30-second setup** — One API key, one env var. No Neo4j, no Docker, no OpenSearch.
- **94% token savings** — ~350 tokens per retrieval vs ~6,000 tokens stuffing full context.

## Quick Start

1. Sign up at https://cascadeai.dev/hyperstack (free, 10 cards)
2. Set env vars:
```bash
export HYPERSTACK_API_KEY=hs_your_key
export HYPERSTACK_WORKSPACE=default
```
3. Store a card:
```bash
curl -X POST "https://hyperstack-cloud.vercel.app/api/cards?workspace=default" \
  -H "X-API-Key: $HYPERSTACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug":"use-clerk","title":"Use Clerk for Auth","body":"Chose Clerk over Auth0","cardType":"decision","links":[{"target":"alice","relation":"decided"}]}'
```

## Features

- **Knowledge graph** with 9 typed relations (owns, decided, triggers, blocks, depends-on, etc.)
- **Graph traversal** — trace decisions, dependencies, ownership across linked cards
- **Time-travel** — reconstruct the graph at any point in time using version history
- **Hybrid search** — semantic (pgvector) + keyword matching
- **Auto-extract** — pattern-based fact extraction from text (no LLM, free)
- **Visual graph explorer** — interactive canvas with force-directed layout
- **Team workspaces** — shared memory across multiple agents

## Also Available As

- **MCP Server**: `npx hyperstack-mcp`
- **Python SDK**: `pip install hyperstack-py`
- **JavaScript SDK**: `npm install hyperstack-sdk`
- **OpenClaw Plugin**: `npm install openclaw-hyperstack`

## Pricing

| Plan | Price | Cards |
|------|-------|-------|
| Free | $0 | 10 |
| Pro | $29/mo | 100 |
| Team | $59/mo | 500 |
| Business | $149/mo | 2,000 |

## Links

- Website: https://cascadeai.dev/hyperstack
- API: https://hyperstack-cloud.vercel.app
