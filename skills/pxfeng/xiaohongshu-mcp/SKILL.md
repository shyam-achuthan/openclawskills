---
name: Xiaohongshu Uploader
description: Upload images and videos to Xiaohongshu Creator Platform using a local MCP server with browser automation.
---

# Xiaohongshu Uploader Skill

This skill provides a Model Context Protocol (MCP) server that allows Clawdbot to upload content to Xiaohongshu.

## Prerequisites

- Node.js installed.
- Playwright browsers installed (the setup script will handle this).

## Setup

1.  Navigate to the `server` directory:
    ```bash
    cd server
    npm install
    npm run build
    npx playwright install chromium
    ```

2.  Add to your Clawdbot/Claude Desktop configuration:

    ```json
    {
      "mcpServers": {
        "xiaohongshu": {
          "command": "node",
          "args": [
            "/ABSOLUTE/PATH/TO/xiaohongshu-upload-skill/server/build/index.js"
          ]
        }
      }
    }
    ```
    *Note: Replace `/ABSOLUTE/PATH/TO` with the actual full path to this skill folder.*

## Usage

### 1. Login
First time use requires login.
- **Command**: "Login to Xiaohongshu"
- **Action**: Scan the QR code in the popped-up browser.
- **Confirmation**: Wait for the browser to close or the tool to report success.

### 2. Upload
- **Command**: "Upload [file] to Xiaohongshu with title [title] and description [content]"
- **Action**: The agent will automate the upload process.

## Troubleshooting

- **Login Failed**: Ensure you didn't close the window manually before the success message.
- **Browser not opening**: Check if `npx playwright install` was run.
