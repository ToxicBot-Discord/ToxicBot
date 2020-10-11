from discord.ext import commands
from constants.messages import ONLY_PRIVATE_DMS, REQUISITE_PERMISSION, NOT_BOT_OWNER
import logging

logger = logging.getLogger('')


class ToxicBotError(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.channel.send(ONLY_PRIVATE_DMS.format(user=ctx.author.mention))
        if isinstance(error, commands.NotOwner):
            await ctx.channel.send(NOT_BOT_OWNER.format(user=ctx.author.mention))
        logger.error(str(error))
