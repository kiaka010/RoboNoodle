from .abstract_plugin import AbstractPlugin
from discord.ext import commands
from src.utils.request import Request
import logging
import json
import random

loggerr = logging.getLogger("discord.dogging")



class Nsfw(AbstractPlugin):
    image_urls = [
        "https://i.pinimg.com/474x/f5/7c/44/f57c44cf25f4dbf69c80cd52655a941c.jpg",
        "https://i.pinimg.com/474x/5c/23/72/5c237225bfeef95458aee071cb319162.jpg",
        "https://i.pinimg.com/474x/f4/e4/9c/f4e49c8d5cf5c530f0c5033074c5eb07.jpg",
        "https://i.pinimg.com/474x/79/f5/bf/79f5bf782e17452569207cad5ad3fa66.jpg",
        "https://i.pinimg.com/474x/47/0f/a2/470fa25acecd64ca7b096ab29b2b873e.jpg",
        "https://i.pinimg.com/474x/35/70/a8/3570a809f849531f21349c56b90aca60.jpg",
        "https://i.pinimg.com/474x/1e/7d/a8/1e7da85ade571514252087b44163b296.jpg",
        "https://i.pinimg.com/474x/b6/d3/14/b6d314c8347be843b6ce397b9a9529c2.jpg",
        "https://i.pinimg.com/474x/3b/60/53/3b6053c0ab621c5cbe5ac2ec136a7a45.jpg",
        "https://i.pinimg.com/474x/2a/f0/5a/2af05a65fac67594e17ac217464ce873.jpg",
        "https://i.pinimg.com/474x/a8/e6/00/a8e600f56a8fdcc1e1401c56f1c39f1e.jpg",
        "https://i.pinimg.com/474x/94/e9/54/94e954241666ad67d37f13a64143e32c.jpg",
        "https://i.pinimg.com/474x/1d/41/76/1d4176262c38ca044abfd6d5b063bfc0.jpg",
        "https://i.pinimg.com/474x/e4/97/8b/e4978bf7343025057383c3aa88e250a9.jpg",
        "https://i.pinimg.com/474x/60/58/7f/60587f17dff3e18ba7934f743b28584a.jpg",
        "https://i.pinimg.com/474x/69/f7/16/69f71674b85dcd1eadc48c6026a1f543.jpg",
        "http://www.elftown.com/stuff/aj/92105/1533429873.jpg"

    ]

    @commands.command("noodlefans", help="Kinky noodle goodness (i am so sorry)")
    async def noodlefans(self, ctx):

        await ctx.send("|| %s ||" % random.choice(self.image_urls))
