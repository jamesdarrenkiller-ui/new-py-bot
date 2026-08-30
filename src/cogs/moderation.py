from datetime import timedelta
import discord
from discord.ext import commands
from src.utils.common import embed
class Moderation(commands.Cog):
    def __init__(self,bot): self.bot=bot
    def hierarchy(self,ctx,member): return member==ctx.guild.owner or ctx.author==ctx.guild.owner or member.top_role<ctx.author.top_role
    @commands.hybrid_command(name='kick',description='Kick a member')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self,ctx,member:discord.Member,*,reason='No reason provided'):
        if member==ctx.author or not self.hierarchy(ctx,member): return await ctx.send('❌ You cannot kick that member.')
        await member.kick(reason=reason); await ctx.send(embed=embed('👢 Member Kicked',f'{member.mention}\n**Reason:** {reason}',0xED4245))
    @commands.hybrid_command(name='ban',description='Ban a member')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self,ctx,member:discord.Member,*,reason='No reason provided'):
        if member==ctx.author or not self.hierarchy(ctx,member): return await ctx.send('❌ You cannot ban that member.')
        await member.ban(reason=reason); await ctx.send(embed=embed('🔨 Member Banned',f'{member.mention}\n**Reason:** {reason}',0xED4245))
    @commands.hybrid_command(name='unban',description='Unban a user by ID')
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx,user_id:str,*,reason='No reason provided'):
        try: u=await self.bot.fetch_user(int(user_id)); await ctx.guild.unban(u,reason=reason)
        except (ValueError,discord.NotFound): return await ctx.send('❌ User is not banned or ID is invalid.')
        await ctx.send(f'✅ Unbanned **{u}**.')
    @commands.hybrid_command(name='softban',description='Softban a member')
    @commands.has_permissions(ban_members=True)
    async def softban(self,ctx,member:discord.Member,*,reason='No reason provided'):
        if not self.hierarchy(ctx,member): return await ctx.send('❌ You cannot softban that member.')
        await member.ban(reason=reason,delete_message_seconds=86400); await ctx.guild.unban(member,reason='Softban completed'); await ctx.send('🧹 Softban completed.')
    @commands.hybrid_command(name='timeout',description='Timeout a member')
    @commands.has_permissions(moderate_members=True)
    async def timeout(self,ctx,member:discord.Member,minutes:int,*,reason='No reason provided'):
        if minutes<1 or minutes>40320: return await ctx.send('❌ Duration must be 1–40320 minutes.')
        if not self.hierarchy(ctx,member): return await ctx.send('❌ You cannot timeout that member.')
        await member.timeout(discord.utils.utcnow()+timedelta(minutes=minutes),reason=reason); await ctx.send(f'⏳ Timed out {member.mention} for **{minutes}m**.')
    @commands.hybrid_command(name='untimeout',description='Remove timeout')
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self,ctx,member:discord.Member,*,reason='No reason provided'):
        await member.timeout(None,reason=reason); await ctx.send(f'✅ Removed timeout from {member.mention}.')
    @commands.hybrid_command(name='warn',description='Warn a member')
    @commands.has_permissions(moderate_members=True)
    async def warn(self,ctx,member:discord.Member,*,reason='No reason provided'): await ctx.send(embed=embed('⚠️ Warning',f'{member.mention}\n**Reason:** {reason}',0xFEE75C))
    @commands.hybrid_command(name='purge',description='Delete messages')
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx,amount:int):
        if not 1<=amount<=100: return await ctx.send('❌ Amount must be 1–100.')
        deleted=await ctx.channel.purge(limit=amount); await ctx.send(f'🧹 Deleted **{len(deleted)}** messages.',delete_after=5)
    @commands.hybrid_command(name='slowmode',description='Set channel slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self,ctx,seconds:int):
        if not 0<=seconds<=21600: return await ctx.send('❌ Seconds must be 0–21600.');
        await ctx.channel.edit(slowmode_delay=seconds); await ctx.send(f'🐢 Slowmode: **{seconds}s**.')
    @commands.hybrid_command(name='lock',description='Lock current channel')
    @commands.has_permissions(manage_channels=True)
    async def lock(self,ctx):
        o=ctx.channel.overwrites_for(ctx.guild.default_role); o.send_messages=False; await ctx.channel.set_permissions(ctx.guild.default_role,overwrite=o); await ctx.send('🔒 Channel locked.')
    @commands.hybrid_command(name='unlock',description='Unlock current channel')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self,ctx):
        o=ctx.channel.overwrites_for(ctx.guild.default_role); o.send_messages=None; await ctx.channel.set_permissions(ctx.guild.default_role,overwrite=o); await ctx.send('🔓 Channel unlocked.')
    @commands.hybrid_command(name='nick',description='Change nickname')
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self,ctx,member:discord.Member,*,nickname=None): await member.edit(nick=nickname); await ctx.send(f'✅ Nickname updated for {member.mention}.')
async def setup(bot): await bot.add_cog(Moderation(bot))
