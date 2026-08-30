import logging
import sys
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

from src.config import load_settings

settings = load_settings()

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
            command_prefix=commands.when_mentioned_or(settings.prefix),
            intents=intents,
            owner_id=settings.owner_id,
            case_insensitive=True,
            strip_after_prefix=True,
        )

    async def setup_hook(self) -> None:
        await self.load_extension("src.cogs.core")
        synced = await self.tree.sync()
        log.info("Registered %d global slash commands.", len(synced))
        log.info("Prefix commands use %r", settings.prefix)

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
    bot.run(settings.token, log_handler=None)
