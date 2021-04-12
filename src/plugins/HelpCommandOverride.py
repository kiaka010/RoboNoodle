from discord.ext.commands.help import DefaultHelpCommand
import logging
logger = logging.getLogger("discord.help")


class HelpCommandOverride(DefaultHelpCommand):

    def __init__(self, **options):
        super().__init__(**options)
        logger.info(options)
        self.command_attrs['name'] = 'robohelp'
        self.command_attrs['aliases'] = ['help']
        self.no_category = "Default"
        self.width = 100
