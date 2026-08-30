import random, discord
from discord.ext import commands
from src.utils.common import embed

class Fun(commands.Cog):
    def __init__(self, bot): self.bot=bot
    @commands.hybrid_command(name="8ball", description="Ask the magic 8-ball")
    async def eightball(self, ctx, question:str): await ctx.send(embed=embed("🎱 Magic 8-Ball", random.choice(["Yes.","No.","Definitely.","Probably.","Ask again later.","It is uncertain."])))
    @commands.hybrid_command(name="rps", description="Play rock paper scissors")
    async def rps(self, ctx, choice:str):
        choice=choice.lower(); choices=["rock","paper","scissors"]
        if choice not in choices: return await ctx.send("❌ Choose rock, paper, or scissors.")
        bot=random.choice(choices); result="draw" if choice==bot else ("win" if (choice,bot) in [("rock","scissors"),("paper","rock"),("scissors","paper")] else "lose")
        await ctx.send(f"✊ You: **{choice}** | 🤖: **{bot}** → **{result.upper()}**")
    @commands.hybrid_command(name="rate", description="Rate something")
    async def rate(self, ctx, *, thing:str): await ctx.send(f"⭐ **{thing}** gets **{random.randint(1,10)}/10**")
    @commands.hybrid_command(name="joke", description="Tell a joke")
    async def joke(self, ctx): await ctx.send(random.choice(["Why did the developer go broke? Because they used up all their cache.","Why do programmers prefer dark mode? Because light attracts bugs.","I would tell you a UDP joke, but you might not get it."]))
    @commands.hybrid_command(name="truthordare", description="Truth or dare")
    async def truthordare(self, ctx): await ctx.send(random.choice(["Truth: What is your most unusual hobby?","Truth: What is a skill you want to learn?","Dare: Send a funny GIF.","Dare: Change your status to something silly for 5 minutes."]))

async def setup(bot): await bot.add_cog(Fun(bot))
