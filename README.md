# CodeX All-In-One Python Discord Bot

A modular `discord.py` bot with slash + `.` prefix commands.

## Command modules
- Core: `ping`, `botinfo`, `userinfo`, `noprefix`
- Help: interactive category dropdown
- Moderation: `ban`, `unban`, `kick`, `softban`, `timeout`, `untimeout`, `warn`, `purge`, `slowmode`, `lock`, `unlock`, `nick`
- Music: `join`, `leave`, `play`, `pause`, `resume`, `skip`, `stop`, `queue`, `shuffle`, `volume`, `nowplaying`, `loop`
- Economy: `balance`, `daily`, `work`, `pay`, `leaderboard`
- AI: `ai`, `summarize`
- APIs: `weather`, `crypto`, `gif`, `movie`
- Fun/utility: `8ball`, `rps`, `rate`, `joke`, `truthordare`, `serverinfo`, `avatar`, `uptime`, `choose`, `roll`, `coinflip`, `poll`, `remind`

## Behavior
- Every implemented command is available as both a slash command and a `.` prefix command through hybrid commands.
- Slash commands are globally synced at startup and the console reports the number registered.
- No Prefix can only be granted/revoked by the bot owner.
- Secrets belong in `.env`; never commit real credentials.

## Configuration
Copy `.env.example` to `.env` and fill in Discord, API, MongoDB, Spotify and Lavalink credentials.

## Run
```bash
pip install -r requirements.txt
python -m src.main
```
