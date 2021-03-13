import os
from .abstract_plugin import AbstractPlugin
from discord.ext import commands
from src.utils.request import Request


class Trello(AbstractPlugin, name='Ideas'):

    @commands.command("idea", help="Got an amazing idea for me, I WANT TO HEAR ALL ABOUT IT")
    async def idea(self, ctx):
        idea = ctx.message.clean_content.replace(os.getenv('DISCORD_PREFIX') + "idea", "")

        author_name = ctx.author.name
        url = "https://api.trello.com/1/cards"
        params = {
            'key': os.getenv('TRELLO_API_KEY'),
            'token': os.getenv('TRELLO_API_TOKEN'),
            'idList': '604ab9e2028f1f3c06e42389',
            'name': "(%s) %s" % (author_name, idea),
        }

        response = Request().post(url, params=params)

        if not response:
            await ctx.send("Sorry something went wrong. Please try again later.....or not")
            return

        # thumbs up message

        await ctx.message.add_reaction('\U0001f44d')
