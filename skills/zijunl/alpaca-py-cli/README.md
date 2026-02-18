# Alpaca Trading (Python CLI) - OpenClaw Agent Skill

> **🤖 AI Agent Skill for OpenClaw**  
> Enable your AI agent to trade stocks and crypto via Alpaca Markets API using natural language commands.

[![ClawHub](https://img.shields.io/badge/ClawHub-alpaca--py--cli-blue)](https://clawhub.ai/skills/alpaca-py-cli)
[![GitHub](https://img.shields.io/badge/GitHub-zijunl%2Falpaca--py--cli-green)](https://github.com/zijunl/alpaca-py-cli)
[![Version](https://img.shields.io/badge/version-1.2.0-orange)](https://clawhub.ai/skills/alpaca-py-cli)

## 🤖 What is this?

This is an **OpenClaw Agent Skill** that gives your AI assistant the ability to:
- Check stock prices and market status
- Manage your trading portfolio
- Execute buy/sell orders
- View trading history and performance
- All through natural language conversation!

**Example conversation:**
```
You: "What's the current price of Apple stock?"
Agent: *runs alpaca quote AAPL* "AAPL is trading at $250.32"

You: "Buy 10 shares"
Agent: *runs alpaca buy AAPL 10* "✓ Order placed for 10 shares of AAPL"
```

## 🚀 Quick Install

### Via ClawHub (Recommended for OpenClaw users)

```bash
npm install -g clawhub
clawhub install alpaca-py-cli
```

### Manual Install

```bash
git clone https://github.com/zijunl/alpaca-py-cli.git
cd alpaca-py-cli
brew install python@3.11
/opt/homebrew/bin/pip3.11 install alpaca-py pytz
```

## ✨ Features

- 📈 Real-time stock quotes
- 💼 Portfolio management
- 📊 Account information
- 🔄 Order execution (market orders)
- 📅 Market calendar
- 📉 Portfolio history
- ⏰ Market status checking
- 🔐 Secure credential management
- 📝 Paper trading support
- 🤖 **Agent-friendly CLI interface**

## 🎯 Quick Start

1. Install dependencies:
   ```bash
   brew install python@3.11
   /opt/homebrew/bin/pip3.11 install alpaca-py pytz
   ```

2. Configure API keys:
   ```bash
   alpaca auth
   ```

3. Test it out:
   ```bash
   alpaca clock
   alpaca account
   alpaca quote AAPL
   ```

## 📚 Commands

```bash
alpaca auth          # Configure API keys
alpaca clock         # Market status
alpaca calendar      # Trading calendar
alpaca history       # Portfolio history
alpaca account       # Account information
alpaca quote AAPL    # Stock quotes
alpaca positions     # Current holdings
alpaca orders        # Order management
alpaca buy/sell      # Execute trades
alpaca cancel/close  # Cancel/close positions
```

## 🤖 For AI Agents

This skill is designed to be used by AI agents like OpenClaw. The agent can:
1. Understand natural language requests about trading
2. Translate them into appropriate CLI commands
3. Execute the commands and interpret results
4. Respond back in natural language

**Agent Usage Pattern:**
```python
# User: "What's my portfolio worth?"
# Agent executes:
alpaca account
# Agent reads output and responds: "Your portfolio is worth $105,234.56"
```

## 🔗 Links

- **ClawHub**: https://clawhub.ai/skills/alpaca-py-cli
- **GitHub**: https://github.com/zijunl/alpaca-py-cli
- **OpenClaw**: https://openclaw.ai
- **Alpaca Markets**: https://alpaca.markets
- **Python SDK Docs**: https://alpaca.markets/docs/python-sdk/

## 🛡️ Why This Skill?

This is a lightweight Python implementation of the Alpaca Trading CLI, designed to be:

- **Easy to install**: Just Python + pip packages
- **Cross-platform**: Works on macOS, Linux, Windows
- **Well-documented**: Clear examples and troubleshooting
- **Safe**: Emphasizes paper trading and credential security
- **Agent-friendly**: Designed specifically for AI agent automation
- **Natural language ready**: CLI output is easy for agents to parse

## 🆚 Differences from Other Alpaca Skills

- **alpaca-trading** (ClawHub): Uses `apcacli` (Rust CLI, third-party tool)
- **alpaca** (ClawHub): Uses Python scripts but different implementation
- **alpaca-py-cli** (this skill): Custom Python CLI optimized for AI agents with Homebrew Python support

## 🔒 Safety & Security

- Always test with paper trading first
- API keys stored in shell config (not in code)
- Interactive `alpaca auth` hides secret key input
- Market orders only (no complex order types to reduce risk)
- Confirmation required for `close-all` command
- Agent can't access your keys directly (uses environment variables)

## 📖 Documentation

Full documentation available in [SKILL.md](SKILL.md)

## 🤝 Contributing

Contributions welcome! Please open an issue or PR on GitHub.

## 📄 License

MIT License - Free to use, modify, and distribute

## 👤 Author

Created for the OpenClaw community by [@zijunl](https://github.com/zijunl)

## 💬 Support

- GitHub Issues: https://github.com/zijunl/alpaca-py-cli/issues
- OpenClaw Discord: https://discord.com/invite/clawd
- ClawHub: https://clawhub.ai/skills/alpaca-py-cli
