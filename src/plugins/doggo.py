from .abstract_plugin import AbstractPlugin
from discord.ext import commands
from src.utils.request import Request
# import logging
# import json
#
# loggerr = logging.getLogger("discord.dogging")


class Doggo(AbstractPlugin):

    # dog_breeds = {}
    # def __init__(self, bot, logger):
    #     with open('data/ceo_dog_breed_list.json') as f:
    #         self.dog_breeds = json.load(f)
    #     loggerr.info("here ready to make a request")
    #     super().__init__(bot, logger)

    @commands.command("doggo", help="Feed your addiction of cute dogs")
    async def doggo(self, ctx, breed: str = None, sub_breed: str = None):
        # loggerr.info(self.dog_breeds)
        url = "https://dog.ceo/api/breeds/image/random"
        # if breed and not sub_breed and breed in self:
        #     url = "https://dog.ceo/api/breed/%s/image/random" % breed
        # if breed and sub_breed:
        #     url = "https://dog.ceo/api/breed/%s/%s/image/random" % (sub_breed, breed)

        headers = {
            'Accept': 'application/json'
        }

        response = Request().get(url, headers=headers)

        if not response:
            await ctx.send("Sorry something went wrong. Please try again later.....or not")
            return

        dog_pic = response.json()['message']

        await ctx.send(dog_pic)

    # @commands.command("doggo-breeds", help="Feed your addiction of cute dogs")
    # async def doggo(self, ctx):
    #     """
    #     List of dog breeds to be added
    #     :param ctx:
    #     :return:
    #     """
    #
    #     return ''

# def setup(bot):
#     bot.add_cog(Doggo(bot))
