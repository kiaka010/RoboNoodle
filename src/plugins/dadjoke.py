from .abstract_plugin import AbstractPlugin
from discord.ext import commands
from src.utils.request import Request
from src.utils.message_utils import MessageUtils


class DadJoke(AbstractPlugin):

    @commands.command("dadjoke", help="Daddy is here to help bring you some joy ..... via bad jokes")
    async def dadjoke(self, ctx):
        url = "https://icanhazdadjoke.com/"
        headers = {
            'Accept': 'application/json'
        }
        response = Request().get(url, headers=headers)

        if not response:
            await ctx.send("Sorry something went wrong. Please try again later.....or not")
            return

        joke = MessageUtils.gather_mentions(ctx.message) + response.json()['joke']

        await ctx.send(joke)
