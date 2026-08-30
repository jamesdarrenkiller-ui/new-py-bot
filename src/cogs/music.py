import os, json, asyncio
import discord
from discord.ext import commands
import wavelink
from src.utils.common import embed

class MusicPlayer(wavelink.Player):
    def __init__(self, *args, **kwargs): super().__init__(*args, **kwargs); self.queue=wavelink.Queue(); self.loop_mode='off'
    async def next_track(self):
        if self.loop_mode=='track' and getattr(self,'current',None): return await self.play(self.current)
        if self.loop_mode=='queue' and getattr(self,'current',None): await self.queue.put_wait(self.current)
        if self.queue.is_empty: return
        await self.play(await self.queue.get_wait())

class Music(commands.Cog):
    def __init__(self,bot): self.bot=bot; self.nodes_ready=False
    async def cog_load(self):
        raw=os.getenv('LAVALINK_NODES_JSON','[]')
        try: nodes=json.loads(raw)
        except json.JSONDecodeError: nodes=[]
        for n in nodes:
            try:
                await wavelink.Pool.connect(client=self.bot, nodes=[wavelink.Node(uri=f"{'https' if n.get('secure') else 'http'}://{n['host']}:{n['port']}", password=n['password'], identifier=n.get('name',n['host']))])
            except Exception as e: print(f'Lavalink node failed: {n.get("name")}: {e}')
        self.nodes_ready=True
    async def player(self,ctx):
        if not ctx.author.voice: await ctx.send('❌ Join a voice channel first.'); return None
        p=ctx.voice_client
        if not isinstance(p,MusicPlayer): p=await ctx.author.voice.channel.connect(cls=MusicPlayer)
        return p
    @commands.hybrid_command(name='join',description='Join your voice channel')
    async def join(self,ctx):
        if not ctx.author.voice: return await ctx.send('❌ Join a voice channel first.')
        await ctx.author.voice.channel.connect(cls=MusicPlayer); await ctx.send('🎵 Joined your voice channel.')
    @commands.hybrid_command(name='leave',description='Leave the voice channel')
    async def leave(self,ctx):
        if ctx.voice_client: await ctx.voice_client.disconnect(); await ctx.send('👋 Disconnected.')
    @commands.hybrid_command(name='play',description='Play a song or URL')
    async def play(self,ctx,*,query:str):
        p=await self.player(ctx)
        if not p: return
        tracks=await wavelink.Playable.search(query)
        if not tracks: return await ctx.send('❌ No results found.')
        track=tracks[0]; await p.queue.put_wait(track)
        if not p.playing: await p.play(await p.queue.get_wait())
        await ctx.send(embed=embed('▶️ Added to Queue',f'**{track.title}**\n{getattr(track,"uri","")}'))
    @commands.hybrid_command(name='pause',description='Pause playback')
    async def pause(self,ctx):
        if ctx.voice_client: await ctx.voice_client.pause(True); await ctx.send('⏸️ Paused.')
    @commands.hybrid_command(name='resume',description='Resume playback')
    async def resume(self,ctx):
        if ctx.voice_client: await ctx.voice_client.pause(False); await ctx.send('▶️ Resumed.')
    @commands.hybrid_command(name='skip',description='Skip the current track')
    async def skip(self,ctx):
        if ctx.voice_client: await ctx.voice_client.stop(); await ctx.send('⏭️ Skipped.')
    @commands.hybrid_command(name='stop',description='Stop and clear the queue')
    async def stop(self,ctx):
        if ctx.voice_client: ctx.voice_client.queue.clear(); await ctx.voice_client.stop(); await ctx.send('⏹️ Stopped.')
    @commands.hybrid_command(name='queue',description='Show the music queue')
    async def queue(self,ctx):
        p=ctx.voice_client; items=list(p.queue) if p else []
        await ctx.send(embed=embed('🎶 Queue','\n'.join(f'`{i+1}.` {t.title}' for i,t in enumerate(items)) or 'Queue is empty.'))
    @commands.hybrid_command(name='shuffle',description='Shuffle the queue')
    async def shuffle(self,ctx):
        if not ctx.voice_client: return await ctx.send('❌ Not playing.')
        ctx.voice_client.queue.shuffle(); await ctx.send('🔀 Queue shuffled.')
    @commands.hybrid_command(name='volume',description='Set volume')
    async def volume(self,ctx,percent:int):
        if not 0<=percent<=1000: return await ctx.send('❌ Volume must be 0–1000.')
        if ctx.voice_client: await ctx.voice_client.set_volume(percent); await ctx.send(f'🔊 Volume: **{percent}%**')
    @commands.hybrid_command(name='nowplaying',description='Show current track')
    async def nowplaying(self,ctx):
        p=ctx.voice_client; await ctx.send(embed=embed('🎧 Now Playing',f'**{p.current.title}**' if p and p.current else 'Nothing is playing.'))
    @commands.hybrid_command(name='loop',description='Set loop mode')
    @commands.choices(mode=[discord.app_commands.Choice(name=x,value=x) for x in ['off','track','queue']])
    async def loop(self,ctx,mode:discord.app_commands.Choice[str]):
        if not ctx.voice_client: return await ctx.send('❌ Not playing.')
        ctx.voice_client.loop_mode=mode.value; await ctx.send(f'🔁 Loop mode: **{mode.value}**')

async def setup(bot): await bot.add_cog(Music(bot))
