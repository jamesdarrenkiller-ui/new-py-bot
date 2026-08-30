import sqlite3, os
from discord.ext import commands
from src.utils.common import embed

DB=os.path.join(os.path.dirname(__file__),'..','..','data','economy.db')
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot=bot; self.db=sqlite3.connect(DB); self.db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, balance INTEGER NOT NULL DEFAULT 0)'); self.db.commit()
    def balance(self,uid):
        row=self.db.execute('SELECT balance FROM users WHERE id=?',(uid,)).fetchone()
        if not row: self.db.execute('INSERT INTO users(id,balance) VALUES(?,0)',(uid,)); self.db.commit(); return 0
        return row[0]
    def add(self,uid,n): self.balance(uid); self.db.execute('UPDATE users SET balance=balance+? WHERE id=?',(n,uid)); self.db.commit()
    @commands.hybrid_command(name='balance',description='Show your balance')
    async def balance_cmd(self,ctx,user=None):
        u=user or ctx.author; await ctx.send(embed=embed('💰 Balance',f'{u.mention} has **{self.balance(u.id):,} coins**.'))
    @commands.hybrid_command(name='daily',description='Claim daily coins')
    async def daily(self,ctx): self.add(ctx.author.id,1000); await ctx.send('🎁 You received **1,000 coins**!')
    @commands.hybrid_command(name='work',description='Work for coins')
    async def work(self,ctx):
        import random; n=random.randint(100,500); self.add(ctx.author.id,n); await ctx.send(f'💼 You earned **{n:,} coins**!')
    @commands.hybrid_command(name='pay',description='Pay another user')
    async def pay(self,ctx,user,amount:int):
        if amount<=0 or self.balance(ctx.author.id)<amount: return await ctx.send('❌ Invalid amount or insufficient balance.')
        self.add(ctx.author.id,-amount); self.add(user.id,amount); await ctx.send(f'💸 Sent **{amount:,} coins** to {user.mention}.')
    @commands.hybrid_command(name='leaderboard',description='Show richest users')
    async def leaderboard(self,ctx):
        rows=self.db.execute('SELECT id,balance FROM users ORDER BY balance DESC LIMIT 10').fetchall(); text='\n'.join(f'**{i}.** <@{uid}> — `{bal:,}`' for i,(uid,bal) in enumerate(rows,1)) or 'No users yet.'; await ctx.send(embed=embed('🏆 Economy Leaderboard',text))
async def setup(bot): await bot.add_cog(Economy(bot))
