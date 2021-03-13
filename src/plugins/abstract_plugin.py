from logging import Logger
from discord.ext import commands


class AbstractPlugin(commands.Cog):

    logger: Logger

    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger
