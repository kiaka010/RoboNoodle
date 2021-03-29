from .abstract_plugin import AbstractPlugin
from discord.ext import commands
from src.utils.request import Request
from src.utils.message_utils import MessageUtils


class Compliment(AbstractPlugin):

    @commands.command("givelove", aliases=['give-love', 'compliment'], help="Give someone the compliment they deserve")
    async def givelove(self, ctx):
        url = "https://complimentr.com/api"
        headers = {
            'Accept': 'application/json'
        }

        response = Request().get(url, headers=headers)

        if not response:
            await ctx.send("Sorry something went wrong. Please try again later.....or not")
            return

        compliment = MessageUtils.gather_mentions(ctx.message) + response.json()['compliment']

        await ctx.send(compliment)

        return compliment
