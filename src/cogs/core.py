import time
from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands
from src.utils.common import embed
DATA_FILE=Path(__file__).resolve().parents[2]/'data'/'noprefix.txt'; DATA_FILE.parent.mkdir(exist_ok=True)
def load_ids():
    if not DATA_FILE.exists(): return set()
    return {int(x) for x in DATA_FILE.read_text().splitlines() if x.strip().isdigit()}
class Core(commands.Cog):
    def __init__(self,bot): self.bot=bot; self.started=time.time(); self.noprefix=load_ids()
    def save(self): DATA_FILE.write_text(''.join(f'{x}\n' for x in sorted(self.noprefix)))
    @app_commands.command(name='ping',description='Check bot latency')
    async def ping(self,i): await i.response.send_message(f'🏓 Pong! `{round(self.bot.latency*1000)}ms`')
    @commands.command(name='ping')
    async def prefix_ping(self,ctx): await ctx.send(f'🏓 Pong! `{round(self.bot.latency*1000)}ms`')
    @app_commands.command(name='botinfo',description='Show bot information')
    async def botinfo(self,i): await i.response.send_message(embed=embed('🤖 Bot Information',f'Servers: **{len(self.bot.guilds)}**\nLatency: **{round(self.bot.latency*1000)}ms**\nUptime: **{int(time.time()-self.started)}s**'))
    @commands.command(name='botinfo')
    async def prefix_botinfo(self,ctx): await ctx.send(embed=embed('🤖 Bot Information',f'Servers: **{len(self.bot.guilds)}**\nLatency: **{round(self.bot.latency*1000)}ms**'))
    @app_commands.command(name='userinfo',description='Show information about a member')
    async def userinfo(self,i,member:discord.Member|None=None):
        member=member or i.user; e=embed(f'👤 {member}'); e.set_thumbnail(url=member.display_avatar.url); e.add_field(name='ID',value=str(member.id)); e.add_field(name='Joined',value=discord.utils.format_dt(member.joined_at,'R') if member.joined_at else 'Unknown'); await i.response.send_message(embed=e)
    @commands.command(name='userinfo')
    async def prefix_userinfo(self,ctx,member:discord.Member|None=None): await ctx.send(f'👤 **{member or ctx.author}** (`{(member or ctx.author).id}`)')
    @app_commands.command(name='noprefix',description='Owner-only No Prefix management')
    @app_commands.describe(action='grant, revoke, or list',user='User')
    @app_commands.choices(action=[app_commands.Choice(name=x,value=x) for x in ('grant','revoke','list')])
    async def noprefix(self,i,action:app_commands.Choice[str],user:discord.User|None=None):
        if i.user.id!=self.bot.owner_id: return await i.response.send_message('❌ Only the bot owner can manage No Prefix.',ephemeral=True)
        if action.value=='list': return await i.response.send_message('**No Prefix Users**\n'+('\n'.join(f'<@{x}>' for x in sorted(self.noprefix)) or 'None'),ephemeral=True)
        if not user: return await i.response.send_message('❌ Provide a user.',ephemeral=True)
        if action.value=='grant': self.noprefix.add(user.id)
        else: self.noprefix.discard(user.id)
        self.save(); await i.response.send_message(f'✅ No Prefix {action.value}ed for {user.mention}.',ephemeral=True)
    @commands.command(name='noprefix')
    @commands.is_owner()
    async def prefix_noprefix(self,ctx,action:str,user:discord.User|None=None):
        action=action.lower()
        if action=='list': return await ctx.send('**No Prefix Users:** '+(', '.join(f'<@{x}>' for x in sorted(self.noprefix)) or 'None'))
        if action not in ('grant','revoke') or not user: return await ctx.send(f'Usage: `{ctx.prefix}noprefix <grant|revoke|list> [user]`')
        if action=='grant': self.noprefix.add(user.id)
        else: self.noprefix.discard(user.id)
        self.save(); await ctx.send(f'✅ No Prefix {action}ed for {user.mention}.')
async def setup(bot): await bot.add_cog(Core(bot))
