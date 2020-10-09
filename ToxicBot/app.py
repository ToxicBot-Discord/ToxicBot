import discord
from discord.ext import commands
import logging
from configparser import RawConfigParser

from helper import logger
from commands.commands import ToxicBotCommands
from commands.listener import ToxicBotListener
from commands.error import ToxicBotError


logger = logging.getLogger('')

config = RawConfigParser()
config.read('secret.ini')

DISCORD_BOT_TOKEN = config.get('Discord', 'BOT_TOKEN')
COMMAND_PREFIX = "/"

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.remove_command("help")
bot.add_cog(ToxicBotCommands(bot))
bot.add_cog(ToxicBotListener(bot))
bot.add_cog(ToxicBotError(bot))
bot.run(DISCORD_BOT_TOKEN)
