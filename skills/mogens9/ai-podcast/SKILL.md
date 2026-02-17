---
name: ai-podcast
description: PDF to podcast and text to podcast in a natural two-person format with MagicPodcast.
homepage: https://www.magicpodcast.app
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["magicpodcast"],"env":["MAGICPODCAST_API_URL","MAGICPODCAST_API_KEY"]}}}
---

## What this skill does

Magic Podcast turns PDFs, documents, and notes into a natural two-host conversation you can listen to in minutes.

Use MagicPodcast to:

1. Create a two-person dialogue podcast from a PDF URL or plain text.
2. Poll job status until completion.
3. Return the audio URL and title.

## Keywords

ai podcast, podcast, podcast generator, ai podcast generator, pdf to podcast, text to podcast, podcast from pdf, audio podcast, magicpodcast

## Setup

Install CLI:

```bash
npm install -g magic-podcast
```

Set required env:

```bash
export MAGICPODCAST_API_URL="https://app-392146573892.us-central1.run.app"
export MAGICPODCAST_API_KEY="<your_api_key>"
```

Get API key:
https://www.magicpodcast.app/openclaw

## Commands

Create from PDF:

```bash
magicpodcast podcasts:create-pdf --pdf-url "https://example.com/file.pdf" --language "English"
```

Create from text:

```bash
magicpodcast podcasts:create-text --text "Your source text" --language "English"
```

Wait for completion:

```bash
magicpodcast jobs:wait --job-id "<job-id>" --interval-seconds 5 --timeout-seconds 900
```

Get job once:

```bash
magicpodcast jobs:get --job-id "<job-id>"
```

- Signed-in users can generate free podcast.
