from .abstract_plugin import AbstractPlugin
from discord.ext import commands
from src.utils.request import Request
from src.utils.message_utils import MessageUtils
from bs4 import BeautifulSoup


class Pickup(AbstractPlugin):

    @commands.command("pickup", help="Struggling with love? I've got the perfect msg for you (success not guaranteed)")
    async def pickup(self, ctx):

        url = "http://www.pickuplinegen.com/"

        response = Request().get(url)

        if not response:
            await ctx.send("Sorry something went wrong. Please try again later.....or not")
            return

        pickup = MessageUtils.gather_mentions(ctx.message)

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select("#content")[0]
        pickup += content.text.strip()

        await ctx.send(pickup)

        return pickup
