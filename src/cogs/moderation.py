import discord
from discord.ext import commands
from src.utils.common import embed

class Moderation(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.hybrid_command(name="kick", description="Kick a member")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if member == ctx.author or member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(embed=embed("❌ Cannot kick", "You cannot kick this member."), ephemeral=True if getattr(ctx, 'interaction', None) else False)
        await member.kick(reason=reason); await ctx.send(embed=embed("👢 Member Kicked", f"{member.mention} was kicked.\n**Reason:** {reason}", 0xED4245))

    @commands.hybrid_command(name="ban", description="Ban a member")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if member == ctx.author or (member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner):
            return await ctx.send(embed=embed("❌ Cannot ban", "You cannot ban this member."))
        await member.ban(reason=reason); await ctx.send(embed=embed("🔨 Member Banned", f"{member.mention} was banned.\n**Reason:** {reason}", 0xED4245))

    @commands.hybrid_command(name="unban", description="Unban a user by ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: str, *, reason: str = "No reason provided"):
        try: user = await self.bot.fetch_user(int(user_id))
        except (ValueError, discord.NotFound): return await ctx.send("❌ Invalid user ID.")
        try: await ctx.guild.unban(user, reason=reason)
        except discord.NotFound: return await ctx.send("❌ That user is not banned.")
        await ctx.send(embed=embed("✅ User Unbanned", f"{user.mention} was unbanned.\n**Reason:** {reason}", 0x57F287))

    @commands.hybrid_command(name="softban", description="Ban and immediately unban a member")
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.ban(reason=reason); await ctx.guild.unban(member, reason="Softban completed")
        await ctx.send(embed=embed("🧹 Softban", f"{member.mention} was softbanned.\n**Reason:** {reason}", 0xED4245))

    @commands.hybrid_command(name="timeout", description="Timeout a member")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason: str = "No reason provided"):
        if minutes < 1 or minutes > 40320: return await ctx.send("❌ Duration must be 1–40320 minutes.")
        await member.timeout(discord.utils.utcnow() + discord.timedelta(minutes=minutes), reason=reason)
        await ctx.send(embed=embed("⏳ Member Timed Out", f"{member.mention} for **{minutes} minutes**.\n**Reason:** {reason}"))

    @commands.hybrid_command(name="untimeout", description="Remove a member timeout")
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.timeout(None, reason=reason); await ctx.send(embed=embed("✅ Timeout Removed", member.mention))

    @commands.hybrid_command(name="warn", description="Warn a member")
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await ctx.send(embed=embed("⚠️ Warning", f"{member.mention} has been warned.\n**Reason:** {reason}", 0xFEE75C))

    @commands.hybrid_command(name="purge", description="Delete messages")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount < 1 or amount > 100: return await ctx.send("❌ Amount must be 1–100.")
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 Deleted **{len(deleted)}** messages.", delete_after=5)

    @commands.hybrid_command(name="slowmode", description="Set channel slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if not 0 <= seconds <= 21600: return await ctx.send("❌ Seconds must be 0–21600.")
        await ctx.channel.edit(slowmode_delay=seconds); await ctx.send(f"🐢 Slowmode set to **{seconds}s**.")

    @commands.hybrid_command(name="lock", description="Lock the current channel")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role); overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite); await ctx.send("🔒 Channel locked.")

    @commands.hybrid_command(name="unlock", description="Unlock the current channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role); overwrite.send_messages = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite); await ctx.send("🔓 Channel unlocked.")

    @commands.hybrid_command(name="nick", description="Change a member nickname")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nickname: str | None = None):
        await member.edit(nick=nickname); await ctx.send(f"✅ Nickname updated for {member.mention}.")

async def setup(bot): await bot.add_cog(Moderation(bot))
