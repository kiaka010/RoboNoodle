import os

import discord
import requests
from discord.ext import commands
import logging
from src.plugins.compliment import *

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')
logger = logging.getLogger("discord")
bot = commands.Bot(command_prefix=PREFIX)


async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')


@bot.command("idea")
async def idea(ctx):
    idea = ctx.message.clean_content.replace(PREFIX + "idea", "")

    author_name = ctx.author.name
    url = "https://api.trello.com/1/cards"
    params = {
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN'),
        'idList': '604ab9e2028f1f3c06e42389',
        'name': "(%s) %s" % (author_name, idea),
    }
    logger.info(params)
    response = requests.request('POST', url, params=params)
    logger.info(response)

    if response.status_code != 200:
        logger.error("A compliment Request Failed")
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return

    # thumbs up message

    await ctx.message.add_reaction('\U0001f44d')


@bot.command("compliment")
async def compliment(ctx):
    await givelove.invoke(ctx)


@bot.command("give-love")
async def give_love(ctx):
    await givelove.invoke(ctx)


@bot.command("givelove")
async def givelove(ctx):
    # logger.info(ctx.channel.members)
    url = "https://complimentr.com/api"
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers)

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


@bot.command("roast")
async def roast(ctx):

    url = "https://www.rappad.co/api/battles/random_insult"
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers)
    logger.info(response)

    if response.status_code != 200:
        logger.error("A Roast Battle Request Failed")
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return

    insult = ""
    if ctx.message.mentions:
        for mention in ctx.message.mentions:
            logger.info(mention)
            insult += "<@%s> " % mention.id
    insult += response.json()['insult']

    await ctx.send(insult)


def main():
    # logging.basicConfig(level=logging.DEBUG)

    logger.setLevel(logging.DEBUG)
    # logger.info(TOKEN)
    # logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', filename='')
    logging.getLogger('discord').setLevel(logging.DEBUG)

    logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(filename="logs.txt")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    logger.info("Starting")
    
    # logger.info(TOKEN)
    bot.run(TOKEN)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Exiting System")