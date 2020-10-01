import discord
from discord.ext import commands
import logging
from configparser import RawConfigParser

import logger
from commands import ToxicBotCommands
from listener import ToxicBotListener
from error import ToxicBotError


logger = logging.getLogger('')

config = RawConfigParser()
config.read('secrets.ini')

DISCORD_BOT_TOKEN = config.get('Discord', 'BOT_TOKEN')
COMMAND_PREFIX = "/"


bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.add_cog(ToxicBotCommands(bot))
bot.add_cog(ToxicBotListener(bot))
bot.add_cog(ToxicBotError(bot))
bot.run(DISCORD_BOT_TOKEN)
