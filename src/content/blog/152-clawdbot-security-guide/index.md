---
title: 'ClawdBot: Setup Guide + How to NOT Get Hacked'
summary: 'What ClawdBot is, how to set it up, and the security configuration most guides skip that will prevent your server from becoming an open door'
date: 'Jan 26 2026'
tags:
  - Security
  - AI
  - Self-Hosted
  - Infrastructure
---

# ClawdBot: Setup Guide + How to NOT Get Hacked

ClawdBot is an open-source AI assistant that runs on your own server and connects to messaging apps like Telegram, WhatsApp, or Discord. You text it, it texts back. It can read your emails, manage files, run shell commands, and act on your behalf.

This is obviously dangerous. You're giving an AI shell access to a server, API tokens to your email and calendar, and an interface anyone can potentially message. A scan of ClawdBot instances running on VPS providers shows many with the gateway port open with zero authentication. API keys, email access, file permissions - exposed directly to the internet. Most setup guides focus on getting it running. This one shows you also how to not get hacked.

## The Setup (Secure Version)

From fresh Ubuntu VPS to hardened private AI server. Do it in this order.

### 1) Lock Down SSH

→ Keys only, no passwords, no root login.

```bash
sudo nano /etc/ssh/sshd_config
# Set explicitly:
PasswordAuthentication no
PermitRootLogin no
```

```bash
sudo sshd -t && sudo systemctl reload ssh
```

### 2) Default-Deny Firewall

→ Block everything incoming by default.

```bash
sudo apt install ufw -y
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw enable
```

### 3) Brute-Force Protection

→ Auto-ban IPs after failed login attempts.

```bash
sudo apt install fail2ban -y
sudo systemctl enable --now fail2ban
```

### 4) Install Tailscale

→ Your private VPN mesh network. This is what makes everything reachable only from your devices.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

### 5) SSH Only via Tailscale

→ No more public SSH exposure.

```bash
# Verify Tailscale is working first!
tailscale status

# Allow SSH only from Tailscale network
sudo ufw allow from 100.64.0.0/10 to any port 22 proto tcp

# Remove the public SSH rule
sudo ufw delete allow OpenSSH
```

### 6) Web Ports Private Too

→ ClawdBot gateway only accessible from your devices.

```bash
sudo ufw allow from 100.64.0.0/10 to any port 443 proto tcp
sudo ufw allow from 100.64.0.0/10 to any port 80 proto tcp
```

### 7) Install Node.js 22

→ ClawdBot requires version 22+. Ubuntu's default is older.

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
```

### 8) Install ClawdBot

```bash
npm install -g clawdbot && clawdbot doctor
```

### 9) Lock ClawdBot to Owner Only

→ Only you can message the bot. Add this to your ClawdBot config:

```json
{
  "dmPolicy": "allowlist",
  "allowFrom": ["YOUR_TELEGRAM_ID"],
  "groupPolicy": "allowlist"
}
```

Never add ClawdBot to group chats. Every person in that chat can issue commands to your server through the bot.

### 10) Enable Sandbox Mode

→ Runs risky operations in a container instead of your actual system.

Check the security docs and enable isolation. If something goes wrong, the blast radius is contained.

### 11) Whitelist Commands

→ Don't let the agent run arbitrary commands. Explicitly list only what it needs:

```json
{
  "allowedCommands": ["git", "npm", "curl"],
  "blockedCommands": ["rm -rf", "sudo", "chmod"]
}
```

If the agent gets hijacked through prompt injection, it can only execute what you've whitelisted.

### 12) Scope API Tokens

→ When connecting GitHub, Gmail, Google Drive: do not use full-access tokens.

Give minimum permissions. Read-only where possible. If something goes wrong, damage is limited to what that specific token could do.

### 13) Fix Credential Permissions

→ Don't leave secrets world-readable.

```bash
chmod 700 ~/.clawdbot/credentials
chmod 600 .env
```

### 14) Run Security Audit

→ Catches issues you missed. Don't skip this.

```bash
clawdbot security audit --deep
```

If this fails, do not deploy. Fix whatever it flags first.

## Verify Everything

```bash
sudo ufw status
ss -tulnp
tailscale status
clawdbot doctor
```

Result should be:
- No public SSH
- No public web ports
- Server only reachable via Tailscale
- Bot responds only to you

## Create Telegram Bot

1. Open Telegram, search for @BotFather
2. Send `/newbot`, follow prompts
3. Copy the token it gives you
4. Get your user ID from @userinfobot
5. Enter both in `clawdbot onboard --install-daemon`

### Approve Pairing

After setup, message your bot on Telegram. It won't respond yet.

```bash
clawdbot pairing list telegram
clawdbot pairing approve telegram YOUR_CODE
```

Now it should respond.

## A Note on Prompt Injection

Someone in the ClawdBot community tested this. They sent an email from a random address to an account ClawdBot had access to. The email contained hidden instructions. ClawdBot followed them and deleted all emails. Including the trash folder.

This wasn't theoretical. It happened.

Claude Opus 4.5 is specifically recommended because Anthropic trained it to resist prompt injection (internal testing shows ~99% resistance). That helps, but it's one layer. The command whitelisting, sandboxing, and scoped API tokens are the others.

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

The security docs are worth reading.
