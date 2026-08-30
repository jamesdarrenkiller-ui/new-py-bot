# Veyronix — All-In-One Python Discord Bot

**Veyronix** is a modular `discord.py` all-in-one Discord bot with slash commands and `.` prefix commands.

> **Made by James**

## ✨ Veyronix Features

- Slash commands with startup registration logs
- Matching `.` prefix commands
- Owner-only No Prefix system
- Interactive `/help` category dropdown
- Moderation tools
- Music powered by Lavalink V4 + Spotify integration
- Economy system
- Groq AI features
- TMDB movie/TV features
- CoinGecko cryptocurrency features
- OpenWeather weather features
- Giphy/Memer/Ksoft media features
- MongoDB persistence
- Centralized environment-based configuration

## 📚 Veyronix Command Modules

### 🤖 Core
`ping` • `botinfo` • `userinfo` • `serverinfo` • `avatar` • `uptime` • `help`

### 👑 No Prefix
`noprefix grant` • `noprefix revoke` • `noprefix list`

No Prefix access can **only** be granted or revoked by the Veyronix bot owner.

### 🔨 Moderation
`ban` • `unban` • `kick` • `softban` • `timeout` • `untimeout` • `warn` • `purge` • `slowmode` • `lock` • `unlock` • `nick`

### 🎵 Music
`join` • `leave` • `play` • `pause` • `resume` • `skip` • `stop` • `queue` • `shuffle` • `volume` • `nowplaying` • `loop`

### 💰 Economy
`balance` • `daily` • `work` • `pay` • `leaderboard`

### 🧠 AI
`ai` • `summarize`

### 🌐 API Commands
`weather` • `crypto` • `gif` • `movie`

### 🎉 Fun & Utility
`8ball` • `rps` • `rate` • `joke` • `truthordare` • `choose` • `roll` • `coinflip` • `poll` • `remind`

## ⌨️ Command Modes

Every implemented command is designed to work in both forms:

```text
Slash:  /ping
Prefix: .ping
```

Veyronix globally syncs its application commands during startup. The console reports the number of slash commands registered.

## 🔐 Configuration

Copy `.env.example` to `.env` and configure Veyronix with your own credentials.

**Never commit `.env` or real API keys, passwords, database credentials, or authentication cookies to GitHub.**

### Services used by Veyronix

- Discord Bot Token
- MongoDB
- Spotify
- Groq
- TMDB
- Twitter/X
- CoinGecko
- OpenWeather
- Giphy
- Memer
- Ksoft
- Yandex
- Lavalink V4 nodes

## 🚀 Run Veyronix

```bash
pip install -r requirements.txt
python -m src.main
```

## 📁 Project

```text
new-py-bot/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── cogs/
│   ├── utils/
│   └── services/
├── data/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚠️ Credentials

If a credential has been exposed publicly, rotate it before deploying Veyronix. Keep production secrets in environment variables or your hosting provider's secret manager.

---

**Veyronix** • Python Discord Bot  
**Made by James**