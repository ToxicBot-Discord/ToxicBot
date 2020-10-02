from discord.ext import commands

from constants.messages import REMOVAL_MESSAGE, PERSONAL_MESSAGE_AFTER_REMOVAL, INFO_MESSAGE
from helper.misc import handleViolations

class ToxicBotCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    async def info(self, ctx):
        member = ctx.author
        channel = ctx.channel
        await ctx.send(INFO_MESSAGE.format(username=member.name))
