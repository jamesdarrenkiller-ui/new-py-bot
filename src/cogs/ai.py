import os, aiohttp, discord
from discord.ext import commands
from src.utils.common import embed

class AI(commands.Cog):
    def __init__(self, bot): self.bot=bot; self.index=0
    def keys(self): return [x.strip() for x in os.getenv('GROQ_API_KEYS','').split(',') if x.strip()]
    @commands.hybrid_command(name="ai", description="Ask the AI a question")
    async def ai(self, ctx, *, prompt:str):
        keys=self.keys()
        if not keys: return await ctx.send("❌ Groq is not configured.")
        key=keys[self.index % len(keys)]; self.index += 1
        headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"}
        payload={"model":os.getenv("GROQ_MODEL","llama-3.1-8b-instant"),"messages":[{"role":"user","content":prompt}],"temperature":0.7}
        async with aiohttp.ClientSession() as s:
            async with s.post("https://api.groq.com/openai/v1/chat/completions",headers=headers,json=payload,timeout=45) as r:
                if r.status!=200: return await ctx.send(f"❌ AI request failed (`{r.status}`).")
                d=await r.json()
        text=d["choices"][0]["message"]["content"]
        for i in range(0,len(text),1900): await ctx.send(embed=embed("🤖 AI",text[i:i+1900]))

    @commands.hybrid_command(name="summarize", description="Summarize text with AI")
    async def summarize(self, ctx, *, text:str): await self.ai.callback(self, ctx, "Summarize this clearly:\n"+text)

async def setup(bot): await bot.add_cog(AI(bot))
