import os, aiohttp, discord
from discord.ext import commands
from src.utils.common import embed

class APIs(commands.Cog):
    def __init__(self, bot): self.bot=bot
    async def get_json(self,url,headers=None,params=None):
        async with aiohttp.ClientSession() as s:
            async with s.get(url,headers=headers,params=params,timeout=15) as r:
                if r.status!=200: return None
                return await r.json()

    @commands.hybrid_command(name="weather", description="Get current weather")
    async def weather(self, ctx, *, city:str):
        key=os.getenv("OPENWEATHER_API_KEY")
        if not key: return await ctx.send("❌ OpenWeather is not configured.")
        d=await self.get_json("https://api.openweathermap.org/data/2.5/weather",params={"q":city,"appid":key,"units":"metric"})
        if not d: return await ctx.send("❌ Weather lookup failed.")
        e=embed(f"🌦️ Weather — {d['name']}",f"**{d['weather'][0]['description'].title()}**"); e.add_field(name="Temperature",value=f"{d['main']['temp']}°C"); e.add_field(name="Feels like",value=f"{d['main']['feels_like']}°C"); e.add_field(name="Humidity",value=f"{d['main']['humidity']}%"); await ctx.send(embed=e)

    @commands.hybrid_command(name="crypto", description="Get cryptocurrency price")
    async def crypto(self, ctx, coin:str):
        d=await self.get_json("https://api.coingecko.com/api/v3/simple/price",params={"ids":coin.lower(),"vs_currencies":"usd","include_24hr_change":"true"})
        if not d or coin.lower() not in d: return await ctx.send("❌ Coin not found.")
        x=d[coin.lower()]; await ctx.send(embed=embed(f"🪙 {coin.upper()}",f"Price: **${x['usd']:,.6f}**\n24h: **{x.get('usd_24h_change',0):.2f}%**"))

    @commands.hybrid_command(name="gif", description="Search Giphy")
    async def gif(self, ctx, *, query:str):
        key=os.getenv("GIPHY_API_KEY")
        if not key: return await ctx.send("❌ Giphy is not configured.")
        d=await self.get_json("https://api.giphy.com/v1/gifs/search",params={"api_key":key,"q":query,"limit":10,"rating":"pg"})
        if not d or not d.get("data"): return await ctx.send("❌ No GIF found.")
        await ctx.send(d["data"][0]["images"]["original"]["url"])

    @commands.hybrid_command(name="movie", description="Search TMDB for a movie")
    async def movie(self, ctx, *, title:str):
        key=os.getenv("TMDB_API_KEY")
        if not key: return await ctx.send("❌ TMDB is not configured.")
        d=await self.get_json("https://api.themoviedb.org/3/search/movie",params={"api_key":key,"query":title})
        if not d or not d.get("results"): return await ctx.send("❌ Movie not found.")
        x=d["results"][0]; e=embed(f"🎬 {x['title']}",x.get('overview') or 'No overview.'); e.add_field(name="Release",value=x.get('release_date') or 'Unknown'); e.add_field(name="Rating",value=str(x.get('vote_average','N/A'))); await ctx.send(embed=e)

async def setup(bot): await bot.add_cog(APIs(bot))
