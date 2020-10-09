import discord


class Hourglass:
    """Simple way of adding an hourglass reaction to a message to indicate that the process takes a while"""

    def __init__(self, message: discord.Message, member: discord.Member):
        self.message = message
        self.member = member

    async def __aenter__(self):
        try:
            await self.message.add_reaction('\N{HOURGLASS}')
        except:
            pass
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.message.remove_reaction('\N{HOURGLASS}', self.member)
        except:
            pass

