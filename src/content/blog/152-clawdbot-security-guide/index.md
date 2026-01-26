---
title: 'ClawdBot: Setup Guide + How to NOT Get Hacked'
summary: 'What ClawdBot is, how to set it up, and the security configuration most guides skip that will prevent your server from becoming an open door'
date: 'Jan 26 2026'
draft: false
tags:
  - Security
  - AI
  - Self-Hosted
  - Infrastructure
---

# ClawdBot: Setup Guide + How to NOT Get Hacked

ClawdBot is an open-source AI assistant that runs on your own server and connects to messaging apps like Telegram, WhatsApp, or Discord. You text it, it texts back. It can read your emails, manage files, run shell commands, and act on your behalf.

While this is great, it's obviously dangerous. You're giving an AI access to a lot, if not all, sensitive information, and you even allow it to act on your behalf. Most setup guides focus on getting it running. This one shows you how to get it runnings but focuses on not getting hacked.

## What ClawdBot Does

A few things make ClawdBot different from ChatGPT or Claude's web interface:

**Persistent memory.** It remembers conversations from weeks ago. Preferences. Context you mentioned once. It builds understanding over time rather than starting fresh each session.

**Proactive messaging.** Normal AI waits for you to open it. ClawdBot can message you first: "You have 3 urgent emails" or "That meeting starts in 20 minutes."

**Takes actions.** Not just answers questions. It sends emails, moves files, controls your browser, fills out forms. You give it access to tools and it uses them.

**Runs 24/7 on your infrastructure.** Your data stays on your server. No third-party storing your conversations.

Cost is roughly $25-50/month: a $5 VPS plus a Claude API subscription.

## Why This Is a Security Problem

You're giving an AI agent:
- Shell access to a server
- API tokens to your email, calendar, files
- An interface anyone can potentially message

A scan of ClawdBot instances running on VPS providers shows many of them have the gateway port open with zero authentication. These servers have API keys, email access, file permissions - exposed directly to the internet.

This is a credentials breach waiting to happen.

### Prompt Injection

And that's just the infrastructure side. There's also the AI vulnerability: prompt injection.

Someone in the ClawdBot community tested this. They sent an email from a random address to an account ClawdBot had access to. The email contained hidden instructions. ClawdBot followed them and deleted all emails. Including the trash folder.

This wasn't theoretical. It happened.

The UK's National Cyber Security Centre has stated that prompt injection is "impossible to eliminate entirely" from LLMs. OWASP ranks it as the #1 vulnerability in AI applications.

Claude Opus 4.5 is specifically recommended because Anthropic trained it to resist prompt injection (internal testing shows ~99% resistance). That helps, but it's one layer. You need the others too.

## Security Configuration

Before connecting ClawdBot to anything important, configure these settings:

### 1. Enable Sandbox Mode

By default, agents can run commands directly on your OS.

Check the security docs and enable isolation. This runs risky operations in a container instead of your actual system. If something goes wrong, the blast radius is contained.

### 2. Run the Security Audit

```bash
clawdbot security audit
```

If this fails, do not deploy. Fix whatever it flags first.

### 3. Whitelist Commands

Don't let the agent run arbitrary commands. Explicitly list only what it needs:

```json
{
  "allowedCommands": ["git", "npm", "curl"],
  "blockedCommands": ["rm -rf", "sudo", "chmod"]
}
```

If the agent gets hijacked through prompt injection, it can only execute what you've whitelisted.

### 4. Scope API Tokens

When connecting GitHub, Gmail, Google Drive: do not use full-access tokens.

Give minimum permissions. Read-only where possible. If something goes wrong, damage is limited to what that specific token could do.

### 5. Private Conversations Only

Never add ClawdBot to group chats. Every person in that chat can issue commands to your server through the bot.

### 6. Dedicated Phone Number for WhatsApp

WhatsApp doesn't have a "bot" concept like Telegram. If you use WhatsApp, use a separate number. Your personal number connected to ClawdBot is unnecessary risk.

## Securing the Gateway

This is very important. The gateway is how ClawdBot exposes its interface. By default, if you open the port, it's accessible to anyone.

**Do not expose the gateway port directly to the internet without authentication.**

Two approaches that work:

### Option A: Cloudflare Tunnel + Zero Trust

Your server never exposes any ports publicly.

Cloudflare Tunnel creates an outbound connection from your server to Cloudflare's network. Traffic routes through Cloudflare, which handles authentication before anything reaches your server.

Set up Zero Trust policies to require login (Google, GitHub, email OTP). ClawdBot is only reachable after authenticating through Cloudflare.

No open ports. No direct exposure.

### Option B: Nginx Reverse Proxy + HTTPS + Auth

Put Nginx in front of the gateway with HTTPS and basic auth:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        auth_basic "Restricted";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

The gateway should never be reachable without authentication.

## Setup Overview

Once security is configured, the setup is straightforward.

### 1. Get a VPS

Hetzner, DigitalOcean, or similar. Cheapest tier (~$5/month) with 2GB RAM is enough.

### 2. Install Node.js 22

ClawdBot requires version 22+. Ubuntu's default is older.

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
```

### 3. Install ClawdBot

```bash
curl -fsSL https://clawd.bot/install.sh | bash
```

Or via npm:

```bash
npm install -g clawdbot@latest
```

### 4. Run Setup Wizard

```bash
clawdbot onboard --install-daemon
```

The wizard asks for:
- Auth method (API key for Anthropic)
- Model selection (choose Opus 4.5 for prompt injection resistance)
- Messaging channel (Telegram is easiest)
- Daemon installation (yes - keeps it running)

### 5. Create Telegram Bot

1. Open Telegram, search for @BotFather
2. Send `/newbot`, follow prompts
3. Copy the token it gives you
4. Get your user ID from @userinfobot
5. Enter both in the wizard

Restricting to your user ID means only you can message the bot.

### 6. Approve Pairing

After setup, message your bot on Telegram. It won't respond yet.

In terminal:

```bash
clawdbot pairing list telegram
clawdbot pairing approve telegram YOUR_CODE
```

Now it should respond.

### 7. Verify

```bash
clawdbot status
clawdbot health
```

Green checkmarks means it's working.

## Common Errors

**"no auth configured"** - Re-run `clawdbot onboard` and set up authentication again.

**Bot not responding** - You forgot to approve pairing. Run `clawdbot pairing list telegram` then approve.

**"node: command not found"** - Node.js isn't installed. Run the nodesource install command.

**Gateway won't start** - Run `clawdbot doctor` to see what's broken.

## Resources

- Docs: https://docs.clawd.bot
- Security guide: https://docs.clawd.bot/gateway/security
- Getting started: https://docs.clawd.bot/start/getting-started
- Troubleshooting: https://docs.clawd.bot/help/troubleshooting
- GitHub: https://github.com/clawdbot/clawdbot

The security docs are worth reading. Actually reading them, not skimming.
