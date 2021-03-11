import os

import requests
from discord.ext import commands
import logging

PREFIX = os.getenv('DISCORD_PREFIX')
logger = logging.getLogger("discord")

bot = commands.Bot(command_prefix=PREFIX)


@bot.command("compliment", pass_context=True)
async def compliment(ctx):
    await givelove.invoke(ctx)


@bot.command("give-love")
async def give_love(ctx):
    await givelove.invoke(ctx)


@bot.command("givelove")
async def givelove(ctx):
    url = "https://complimentr.com/api"
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers)
    logger.info(response)

    if response.status_code != 200:
        logger.error("A compliment Request Failed")
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return

    compliment = ""
    if ctx.message.mentions:
        for mention in ctx.message.mentions:
            logger.info(mention)
            compliment += "<@%s> " % mention.id
    compliment += response.json()['compliment']

    await ctx.send(compliment)
