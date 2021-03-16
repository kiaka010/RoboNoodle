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
        breed = breed.lower() if breed else None
        sub_breed = sub_breed.lower() if sub_breed else None
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

        message_group = []
        message = '```'
        for breed in self.dog_breeds:
            if len(message) + len(breed) + 5 >= 2000:  # added two for space and comma - 2000 is discord message limit
                message += '```'
                message_group.append(message)
                message = '```'

            message += f" {breed},"
            if self.dog_breeds[breed]:
                for sub_breed in self.dog_breeds[breed]:
                    if len(message) + len(breed) + len(sub_breed) + 6 >= 2000:  # added three for space and comma - 2000 is discord message limit
                        message += '```'
                        message_group.append(message)
                        message = '```'
                    message += f" {sub_breed} {breed},"

        message += '```'
        message_group.append(message)
        await ctx.send("Its quite a large list so let me just slide that into your DM's :wink:")

        for out_message in message_group:
            await ctx.author.send(out_message)
