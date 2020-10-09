from discord.ext import commands
from datetime import datetime
import discord
import time


class GeneralCog(commands.Cog, name='General'):
    """Basic commands to check statistics and information"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['latency', 'delay', 'pong'])
    async def ping(self, ctx):
        """Displays the ping (latency) to and from Discord"""
        now = time.time()
        msg = await ctx.send(embed=discord.Embed(title=":ping_pong:  **WebSocket (API) latency: ``Pinging...`` | Bot latency: ``Pinging...``**", color=self.bot.embed_color))
        api_latency = int(self.bot.latency*1000)
        ping = int((time.time() - now)*100)
        await msg.edit(embed=discord.Embed(title=f":ping_pong:  **WebSocket (API) latency: ``{api_latency}ms`` | Bot latency: ``{ping}ms``**", color=self.bot.embed_color))


def setup(bot):
    bot.add_cog(GeneralCog(bot))

