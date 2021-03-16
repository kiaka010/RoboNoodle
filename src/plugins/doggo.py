from .abstract_plugin import AbstractPlugin
from discord.ext import commands
from src.utils.request import Request
import logging
import json
import random

loggerr = logging.getLogger("discord.dogging")


class Doggo(AbstractPlugin):

    dog_breeds = {}

    def __init__(self, bot, logger):
        with open('src/data/ceo_dog_breed_list.json') as f:
            self.dog_breeds = json.load(f)
        loggerr.info("here ready to make a request")
        super().__init__(bot, logger)

    @commands.command("doggo", help="Feed your addiction of cute dogs")
    async def doggo(self, ctx, breed: str = None, sub_breed: str = None):
        loggerr.info(self.dog_breeds)
        url = "https://dog.ceo/api/breeds/image/random"
        if breed and not sub_breed:
            if breed in self.dog_breeds:
                if self.dog_breeds[breed]:  # if there are sub breeds take a random one:
                    url = "https://dog.ceo/api/breed/%s/%s/images/random" % (breed, random.choice(self.dog_breeds[breed]))
                else:
                    url = "https://dog.ceo/api/breed/%s/images/random" % breed
            else:
                await ctx.send("Sorry, I don't recognise %s.  Please check doggo-breeds for a full list" % breed)
                await ctx.send("Here is a random dog instead")
                url = "https://dog.ceo/api/breeds/image/random"

        elif breed and sub_breed:
            if sub_breed in self.dog_breeds and breed in self.dog_breeds[sub_breed]:
                # breed and sub breed in reverse
                url = "https://dog.ceo/api/breed/%s/%s/images/random" % (sub_breed, breed)
            else:
                await ctx.send("Sorry, I don't recognise %s %s.  Please check doggo-breeds for a full list" % (breed, sub_breed))
                await ctx.send("Here is a random dog instead")
                url = "https://dog.ceo/api/breeds/image/random"

        headers = {
            'Accept': 'application/json'
        }

        response = Request().get(url, headers=headers)

        if not response:
            await ctx.send("Sorry something went wrong. Please try again later.....or not")
            return

        dog_pic = response.json()['message']

        await ctx.send(dog_pic)

    @commands.command("doggo-breeds", help="Get a full list of all the dog breed images you could ever need")
    async def doggo_breeds(self, ctx):
        await ctx.send("Here is a full list all the dog breeds you can ask for (not like you need more right?)")

        message = '```'
        for breed in self.dog_breeds:
            if self.dog_breeds[breed] and len(self.dog_breeds[breed]) == 1:
                message += f" {self.dog_breeds[breed][0]} {breed},"
            elif self.dog_breeds[breed]:
                for sub_breed in self.dog_breeds[breed]:
                    message += f" {sub_breed} {breed},"
            else:
                message += f" {breed},"
        message += '```'
        await ctx.send(message)
