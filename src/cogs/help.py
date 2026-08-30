import discord
from discord.ext import commands
from src.utils.common import embed

class HelpSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot=bot
        options=[discord.SelectOption(label='Core',emoji='🤖',value='core'),discord.SelectOption(label='Moderation',emoji='🔨',value='moderation'),discord.SelectOption(label='Music',emoji='🎵',value='music'),discord.SelectOption(label='Economy',emoji='💰',value='economy'),discord.SelectOption(label='AI',emoji='🧠',value='ai'),discord.SelectOption(label='Fun',emoji='🎉',value='fun'),discord.SelectOption(label='APIs',emoji='🌐',value='apis'),discord.SelectOption(label='Utility',emoji='🛠️',value='utility')]
        super().__init__(placeholder='Choose a command category…',options=options)
    async def callback(self,interaction):
        names={'core':'Core','moderation':'Moderation','music':'Music','economy':'Economy','ai':'AI','fun':'Fun','apis':'APIs','utility':'Utility'}
        prefix={'core':['ping','botinfo','userinfo','noprefix'],'moderation':['ban','unban','kick','softban','timeout','untimeout','warn','purge','slowmode','lock','unlock','nick'],'music':['join','leave','play','pause','resume','skip','stop','queue','shuffle','volume','nowplaying','loop'],'economy':['balance','daily','work','pay','leaderboard'],'ai':['ai','summarize'],'fun':['8ball','rps','rate','joke','truthordare'],'apis':['weather','crypto','gif','movie'],'utility':['serverinfo','avatar','uptime','choose','roll','coinflip','poll','remind']}[self.values[0]]
        await interaction.response.edit_message(embed=embed(f'{self.options[[o.value for o in self.options].index(self.values[0])].emoji} {names[self.values[0]]}', '\n'.join(f'`/{x}`  •  `.{x}`' for x in prefix)),view=self.view)
class HelpView(discord.ui.View):
    def __init__(self,bot): super().__init__(timeout=180); self.add_item(HelpSelect(bot))
class Help(commands.Cog):
    def __init__(self,bot): self.bot=bot
    @commands.hybrid_command(name='help',description='Open the bot help menu')
    async def help(self,ctx): await ctx.send(embed=embed('📚 Help Menu','Select a category below to see its commands.'),view=HelpView(self.bot))
async def setup(bot): await bot.add_cog(Help(bot))
