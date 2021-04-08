import os
import random
import discord
from discord.ext import commands
import logging
import aiocron
from src.utils.request import Request
from src.plugins import *
from src.plugins.HelpCommandOverride import HelpCommandOverride

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')
logger = logging.getLogger("discord")
bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, help_command=HelpCommandOverride())


async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')


####### All here are needed to create a custom regex setup of acting upon specific messages
# @bot.event
# async def on_message(msg):
#     logger.info("in on_message #1")
#     await bot.process_commands(msg)
#
# @bot.listen()
# async def on_message(msg):
#     logger.info("pebcak")
#     await msg.add_reaction('\U0001f44d')
#######

@bot.command("dankerbeef", help="Looking for a Danker Beef video, look no further")
async def dankerbeef(ctx):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': os.getenv('YOUTUBE_API_KEY'),
        'channelId': 'UCsv2pj6rM1hM5YloMDZdGwA',
        'order': "date",
        'maxResults': 200
    }
    response = Request().get(url, params=params, expire_after=3600)

    if not response:
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return

    video_list = []
    video_list += response.json()['items']

    if 'nextPageToken' in response.json():
        while 'nextPageToken' in response.json():
            logger.info("Requesting next page %s" % response.json()['nextPageToken'])
            params['pageToken'] = response.json()['nextPageToken']
            response = Request().get(url, params=params, expire_after=3600)

            if not response:
                await ctx.send("Sorry something went wrong. Please try again later.....or not")
                return
            if response.json()['items']:
                video_list += response.json()['items']

    random_video = random.choice(video_list)
    await ctx.send("https://www.youtube.com/watch?v=%s" % random_video['id']['videoId'])


# @aiocron.crontab('* * * * *')  # every min
@aiocron.crontab('1 0 * * *')  # 1 min past midnight
async def midnight_process():
    channel = bot.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
    await channel.send("Enjoy your daily Danker Beef vid")

    await dankerbeef(channel)


@aiocron.crontab('0 19 * * *')  # 0 min past 7pm
async def kuu_appreciation():
    channel = bot.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
    await channel.send("<@461055013582798859> This is your daily reminder that you're a very good girl")


def main():
    logger.setLevel(logging.DEBUG)
    logging.getLogger('discord').setLevel(logging.DEBUG)

    logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    rootLogger = logging.getLogger()

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    logger.info("Starting")
    install_cogs()
    bot.run(TOKEN)


def install_cogs():
    bot.add_cog(DadJoke(bot, logger))
    bot.add_cog(Compliment(bot, logger))
    bot.add_cog(Roast(bot, logger))
    bot.add_cog(Pickup(bot, logger))
    bot.add_cog(Trello(bot, logger))
    bot.add_cog(Doggo(bot, logger))
    bot.add_cog(Nsfw(bot, logger))
    bot.add_cog(FerdoLove(bot, logger))
    bot.add_cog(Voice(bot, logger))
    # bot.add_cog(DankerBeef(bot, logger))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Exiting System")
