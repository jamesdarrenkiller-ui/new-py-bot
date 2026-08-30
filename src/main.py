import os
import sys
import logging
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("BOT_OWNER_ID", "0"))
PREFIX = os.getenv("PREFIX", ".")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not configured")
if not OWNER_ID:
    raise RuntimeError("BOT_OWNER_ID is not configured")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("codex-bot")


class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=commands.when_mentioned_or(PREFIX),
            intents=intents,
            owner_id=OWNER_ID,
            case_insensitive=True,
            strip_after_prefix=True,
        )

    async def setup_hook(self) -> None:
        # Cogs are added here as the project grows.
        await self.load_extension("src.cogs.core")
        synced = await self.tree.sync()
        log.info("Registered %d global slash commands.", len(synced))
        log.info("Prefix commands use %r", PREFIX)

    async def on_ready(self) -> None:
        log.info("Logged in as %s (%s)", self.user, self.user.id if self.user else "?")
        log.info("Connected to %d guild(s).", len(self.guilds))


bot = Bot()


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
        return
    if isinstance(error, commands.NotOwner):
        await ctx.send("Only the bot owner can use this command.")
        return
    log.exception("Prefix command error", exc_info=error)
    await ctx.send("An unexpected error occurred.")


if __name__ == "__main__":
    bot.run(TOKEN, log_handler=None)
