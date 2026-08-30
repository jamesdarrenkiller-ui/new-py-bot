import logging,sys
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv
ROOT=Path(__file__).resolve().parents[1]; load_dotenv(ROOT/'.env')
from src.config import load_settings
settings=load_settings()
logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',handlers=[logging.StreamHandler(sys.stdout)])
log=logging.getLogger('codex-bot')
class Bot(commands.Bot):
    def __init__(self):
        intents=discord.Intents.default(); intents.message_content=True; intents.members=True
        super().__init__(command_prefix=commands.when_mentioned_or(settings.prefix),intents=intents,owner_id=settings.owner_id,case_insensitive=True,strip_after_prefix=True)
    async def setup_hook(self):
        for name in ('core','help','moderation','utility','fun','apis','ai','economy','music'):
            try: await self.load_extension(f'src.cogs.{name}')
            except Exception: log.exception('Failed to load cog %s',name)
        synced=await self.tree.sync(); log.info('Registered %d global slash commands.',len(synced)); log.info('Prefix commands use %r',settings.prefix)
    async def on_ready(self): log.info('Logged in as %s (%s)',self.user,self.user.id if self.user else '?'); log.info('Connected to %d guild(s).',len(self.guilds))
    async def on_message(self,message):
        if message.author.bot: return
        if message.content and not message.content.startswith((settings.prefix,'<@','<@!')):
            cog=self.get_cog('Core')
            if cog and (message.author.id in cog.noprefix or message.author.id==self.owner_id): message.content=settings.prefix+message.content
        await self.process_commands(message)
bot=Bot()
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound): return
    if isinstance(error,commands.NotOwner): return await ctx.send('❌ Only the bot owner can use this command.')
    if isinstance(error,(commands.MissingPermissions,commands.BotMissingPermissions)): return await ctx.send('❌ Missing required permissions.')
    if isinstance(error,commands.MissingRequiredArgument): return await ctx.send(f'❌ Missing argument: `{error.param.name}`.')
    if isinstance(error,commands.BadArgument): return await ctx.send('❌ Invalid argument.')
    log.exception('Prefix command error',exc_info=error); await ctx.send('❌ An unexpected error occurred.')
if __name__=='__main__': bot.run(settings.token,log_handler=None)
