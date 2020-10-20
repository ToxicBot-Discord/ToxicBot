from discord import errors
from discord.ext import commands
from constants.messages import ONLY_PRIVATE_DMS, NOT_BOT_OWNER
from helper import embed as embedded
import logging


logger = logging.getLogger("")


class ToxicBotError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):  # If a private command is sent to a public channel
            await ctx.channel.send(embed=embedded.error(ONLY_PRIVATE_DMS.format(user=ctx.author.mention)))
            return
        elif isinstance(error, commands.NotOwner):  # If user issues commands that can only be issued by the admin
            await ctx.channel.send(embed=embedded.error(NOT_BOT_OWNER.format(user=ctx.author.mention)))
            return
        elif isinstance(error, errors.Forbidden):
            logger.error(str(error))
            return
        else:  # Catch generic exception
            logger.error(str(error))
