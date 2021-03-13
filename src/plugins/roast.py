from .abstract_plugin import AbstractPlugin
from discord.ext import commands
from src.utils.request import Request
from src.utils.message_utils import MessageUtils


class Roast(AbstractPlugin):

    @commands.command("roast", help="Are you evil... actually don't answer that.  I'll be evil for you")
    async def roast(self, ctx):

        url = "https://www.rappad.co/api/battles/random_insult"
        headers = {
            'Accept': 'application/json'
        }
        response = Request().get(url, headers=headers)

        if not response:
            await ctx.send("Sorry something went wrong. Please try again later.....or not")
            return

        insult = MessageUtils.gather_mentions(ctx.message) + response.json()['insult']

        await ctx.send(insult)
