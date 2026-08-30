import os
import time
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "noprefix.txt"
DATA_FILE.parent.mkdir(exist_ok=True)


def load_noprefix_ids() -> set[int]:
    if not DATA_FILE.exists():
        return set()
    values: set[int] = set()
    for line in DATA_FILE.read_text(encoding="utf-8").splitlines():
        try:
            values.add(int(line.strip()))
        except ValueError:
            continue
    return values


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.started = time.time()
        self.noprefix = load_noprefix_ids()

    def save_noprefix(self) -> None:
        DATA_FILE.write_text(
            "".join(f"{user_id}\n" for user_id in sorted(self.noprefix)),
            encoding="utf-8",
        )

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.id in self.noprefix or ctx.author.id == self.bot.owner_id

    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"🏓 Pong! `{round(self.bot.latency * 1000)}ms`")

    @commands.command(name="ping")
    async def prefix_ping(self, ctx: commands.Context) -> None:
        await ctx.send(f"🏓 Pong! `{round(self.bot.latency * 1000)}ms`")

    @app_commands.command(name="botinfo", description="Show bot information")
    async def botinfo(self, interaction: discord.Interaction) -> None:
        uptime = int(time.time() - self.started)
        embed = discord.Embed(title="🤖 Bot Information")
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)))
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)} ms")
        embed.add_field(name="Uptime", value=f"{uptime}s")
        embed.add_field(name="Python", value=f"{os.sys.version_info.major}.{os.sys.version_info.minor}")
        await interaction.response.send_message(embed=embed)

    @commands.command(name="botinfo")
    async def prefix_botinfo(self, ctx: commands.Context) -> None:
        uptime = int(time.time() - self.started)
        await ctx.send(f"🤖 **Bot Info** • Servers: `{len(self.bot.guilds)}` • Latency: `{round(self.bot.latency * 1000)}ms` • Uptime: `{uptime}s`")

    @app_commands.command(name="userinfo", description="Show information about a member")
    @app_commands.describe(member="Member to inspect")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member | None = None) -> None:
        member = member or interaction.user
        embed = discord.Embed(title=f"👤 {member}")
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=str(member.id))
        embed.add_field(name="Joined", value=discord.utils.format_dt(member.joined_at, style="R") if member.joined_at else "Unknown")
        await interaction.response.send_message(embed=embed)

    @commands.command(name="userinfo")
    async def prefix_userinfo(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        member = member or ctx.author
        await ctx.send(f"👤 **{member}** (`{member.id}`)")

    @app_commands.command(name="noprefix", description="Owner-only: grant, revoke, or list no-prefix users")
    @app_commands.describe(action="Action", user="User to grant/revoke")
    @app_commands.choices(action=[
        app_commands.Choice(name="grant", value="grant"),
        app_commands.Choice(name="revoke", value="revoke"),
        app_commands.Choice(name="list", value="list"),
    ])
    async def noprefix(self, interaction: discord.Interaction, action: app_commands.Choice[str], user: discord.User | None = None) -> None:
        if interaction.user.id != self.bot.owner_id:
            await interaction.response.send_message("Only the bot owner can manage No Prefix.", ephemeral=True)
            return
        if action.value == "list":
            names = [f"<@{uid}> (`{uid}`)" for uid in sorted(self.noprefix)] or ["None"]
            await interaction.response.send_message("**No Prefix Users**\n" + "\n".join(names), ephemeral=True)
            return
        if user is None:
            await interaction.response.send_message("Provide a user.", ephemeral=True)
            return
        if action.value == "grant":
            self.noprefix.add(user.id)
            message = f"✅ Granted No Prefix to {user.mention}."
        else:
            self.noprefix.discard(user.id)
            message = f"✅ Revoked No Prefix from {user.mention}."
        self.save_noprefix()
        await interaction.response.send_message(message, ephemeral=True)

    @commands.command(name="noprefix")
    @commands.is_owner()
    async def prefix_noprefix(self, ctx: commands.Context, action: str, user: discord.User | None = None) -> None:
        if action.lower() == "list":
            await ctx.send("**No Prefix Users:** " + (", ".join(f"<@{uid}>" for uid in sorted(self.noprefix)) or "None"))
            return
        if user is None or action.lower() not in {"grant", "revoke"}:
            await ctx.send(f"Usage: `{ctx.prefix}noprefix <grant|revoke|list> [user]`")
            return
        if action.lower() == "grant":
            self.noprefix.add(user.id)
            text = f"✅ Granted No Prefix to {user.mention}."
        else:
            self.noprefix.discard(user.id)
            text = f"✅ Revoked No Prefix from {user.mention}."
        self.save_noprefix()
        await ctx.send(text)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Core(bot))
