import discord
from discord.ext import commands
import logging
from configparser import RawConfigParser

from helper import logger
from commands.commands import ToxicBotGeneralCommands
from commands.listener import ToxicBotListener
from commands.error import ToxicBotError
from commands.admin import ToxicBotAdminCommands
from database.create import CreateTables


logger = logging.getLogger("")

config = RawConfigParser()
config.read("secret.ini")

DISCORD_BOT_TOKEN = config.get("DISCORD", "BOT_TOKEN")
COMMAND_PREFIX = "/"

create_table = CreateTables()
create_table.createSchema()

logger.info("Database created successfully")

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.remove_command("help")
bot.add_cog(ToxicBotGeneralCommands(bot))
bot.add_cog(ToxicBotListener(bot))
bot.add_cog(ToxicBotError(bot))
bot.add_cog(ToxicBotAdminCommands(bot))
bot.run(DISCORD_BOT_TOKEN)
