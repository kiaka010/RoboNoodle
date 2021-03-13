from discord import Message
import logging

logger = logging.getLogger("discord.utils")


class MessageUtils:

    @staticmethod
    def gather_mentions(message: Message):
        """
        Return a tagged string of user ids found as mentions in a message
        :param message:
        :return: string
        """

        if not message.mentions:
            return ""

        response = ""
        for mention in message.mentions:
            response += "<@%s> " % mention.id

        return response
