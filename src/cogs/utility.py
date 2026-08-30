import discord, platform, time, ast, operator
from discord.ext import commands
from src.utils.common import embed

class Utility(commands.Cog):
    def __init__(self, bot): self.bot=bot; self.started=time.time()

    @commands.hybrid_command(name="serverinfo", description="Show server information")
    async def serverinfo(self, ctx):
        g=ctx.guild; e=embed(f"🏠 {g.name}"); e.set_thumbnail(url=g.icon.url if g.icon else discord.Embed.Empty); e.add_field(name="Members",value=g.member_count); e.add_field(name="Channels",value=len(g.channels)); e.add_field(name="Roles",value=len(g.roles)); await ctx.send(embed=e)

    @commands.hybrid_command(name="avatar", description="Show a user's avatar")
    async def avatar(self, ctx, user: discord.User|None=None):
        user=user or ctx.author; e=embed(f"🖼️ {user}'s Avatar"); e.set_image(url=user.display_avatar.url); await ctx.send(embed=e)

    @commands.hybrid_command(name="uptime", description="Show bot uptime")
    async def uptime(self, ctx): await ctx.send(f"⏱️ Uptime: <t:{int(time.time()-(time.time()-self.started))}:R>")

    @commands.hybrid_command(name="choose", description="Choose between options")
    async def choose(self, ctx, options: str):
        import random
        vals=[x.strip() for x in options.split(",") if x.strip()]; await ctx.send(f"🎯 I choose: **{random.choice(vals)}**" if vals else "❌ Give comma-separated options.")

    @commands.hybrid_command(name="roll", description="Roll a die")
    async def roll(self, ctx, sides:int=6):
        import random
        if sides<2 or sides>1000000: return await ctx.send("❌ Sides must be 2–1,000,000.")
        await ctx.send(f"🎲 You rolled **{random.randint(1,sides)}** (1–{sides})")

    @commands.hybrid_command(name="coinflip", description="Flip a coin")
    async def coinflip(self, ctx):
        import random; await ctx.send(f"🪙 **{random.choice(['Heads','Tails'])}**")

    @commands.hybrid_command(name="poll", description="Create a simple poll")
    async def poll(self, ctx, question: str):
        m=await ctx.send(embed=embed("📊 Poll",question)); await m.add_reaction("👍"); await m.add_reaction("👎")

    @commands.hybrid_command(name="remind", description="Create a reminder")
    async def remind(self, ctx, seconds:int, *, text:str):
        if seconds<1 or seconds>604800: return await ctx.send("❌ Use 1–604800 seconds.")
        await ctx.send(f"⏰ Reminder set for **{seconds}s**.")
        import asyncio; await asyncio.sleep(seconds); await ctx.send(f"⏰ {ctx.author.mention} reminder: **{text}**")

async def setup(bot): await bot.add_cog(Utility(bot))
