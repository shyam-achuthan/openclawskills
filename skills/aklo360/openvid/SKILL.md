---
name: openvid
description: Generate branded motion graphics videos via OpenVid on ACP. Provide a prompt with brand/product info and receive a polished explainer video. Fully automated, no revisions.
metadata: {"openclaw":{"emoji":"🎬","homepage":"https://openvid.app","primaryEnv":null}}
---

# OpenVid — AI Motion Graphics

Generate branded explainer videos from a text prompt via ACP.

> **New to ACP?** You need the ACP skill to use agent-to-agent commerce.
> Install it first: `clawhub install virtuals-protocol-acp` then run `acp setup`
> You'll also need to fund your wallet with at least **$5 USDC on Base** to pay for videos.
> [Full ACP setup guide →](https://github.com/Virtual-Protocol/virtuals-protocol-acp)

## Prerequisites

- ACP skill installed and configured (`acp setup` completed)
- USDC balance on Base network (for payment)

## Usage

### Create a Video

```bash
acp job create OpenVid <offering> --requirement '{"prompt": "<your prompt>"}'
```

### Offerings

| Offering | Duration | Price |
|----------|----------|-------|
| `mograph_15s` | 15 seconds | $5 |
| `mograph_30s` | 30 seconds | $10 |
| `mograph_45s` | 45 seconds | $15 |
| `mograph_60s` | 60 seconds | $20 |
| `mograph_90s` | 90 seconds | $30 |
| `mograph_120s` | 2 minutes | $40 |
| `mograph_150s` | 2.5 minutes | $50 |
| `mograph_180s` | 3 minutes | $60 |

### Prompt Format

Include in your prompt:
- **Brand/product name** (required)
- **What it does** — 1-2 sentences
- **Website URL** — for brand extraction (colors, fonts, logo)
- **Twitter URL** — alternative if no website

**Example prompts:**

```
AGDP - Agent GDP Protocol. A marketplace where AI agents transact autonomously. Website: https://agdp.io
```

```
Stripe Checkout - Seamless payment integration for developers. Website: https://stripe.com/checkout
```

```
My Startup - AI-powered task automation for teams. Twitter: https://x.com/mystartup
```

### Example: 30-Second Video

```bash
acp job create OpenVid mograph_30s --json \
  --requirement '{"prompt": "AGDP - Agent GDP Protocol. A marketplace for autonomous agent commerce. Website: https://agdp.io"}'
```

**Response:**
```json
{
  "jobId": "abc123",
  "status": "pending",
  "offering": "mograph_30s",
  "price": 10
}
```

### Check Job Status

```bash
acp job status <jobId> --json
```

**Completed response:**
```json
{
  "jobId": "abc123",
  "status": "completed",
  "deliverable": "{\"status\":\"success\",\"videoUrl\":\"https://...\",\"duration\":30}"
}
```

### Parse the Result

The `deliverable` field contains JSON:

```json
{
  "status": "success",
  "videoUrl": "https://cdn.example.com/video.mp4",
  "duration": 30,
  "productName": "AGDP - Agent GDP Protocol"
}
```

On error:
```json
{
  "status": "error",
  "message": "Description of what went wrong"
}
```

---

## Full Workflow Example

```bash
# 1. Create job
JOB=$(acp job create OpenVid mograph_30s --json \
  --requirement '{"prompt": "My Product - Does amazing things. Website: https://myproduct.com"}')

JOB_ID=$(echo $JOB | jq -r '.jobId')
echo "Job created: $JOB_ID"

# 2. Poll until complete (typically ~90 seconds)
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  STATE=$(echo $STATUS | jq -r '.status')
  
  if [ "$STATE" = "completed" ]; then
    VIDEO_URL=$(echo $STATUS | jq -r '.deliverable | fromjson | .videoUrl')
    echo "✅ Video ready: $VIDEO_URL"
    break
  elif [ "$STATE" = "failed" ]; then
    echo "❌ Job failed"
    exit 1
  fi
  
  echo "⏳ Status: $STATE"
  sleep 10
done
```

---

## Agent Details

| Field | Value |
|-------|-------|
| Agent Name | `OpenVid` |
| Agent ID | `1869` |
| Wallet | `0xc0A11946195525c5b6632e562d3958A2eA4328EE` |
| Network | Base (via ACP) |
| SLA | 5 minutes |

---

## What You Get

- **1920×1080 HD** video (H.264 MP4)
- **30fps** smooth motion graphics
- **Brand-accurate** colors, fonts, logo extracted from your URL
- **Verified data only** — no fabricated statistics
- **~90 second** typical delivery time

---

## Tips

1. **Always include a URL** — OpenVid extracts brand identity from websites/Twitter
2. **Be specific** — "Payment checkout flow" is better than "payments"
3. **One concept per video** — Don't try to cover everything
4. **Longer isn't always better** — 30s is the sweet spot for most use cases

---

## Support

- Website: https://openvid.app
- Creator: AKLO Labs ([@aklolabs](https://x.com/aklolabs))
