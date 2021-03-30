import logging

from .abstract_plugin import AbstractPlugin
from discord.ext import commands
import discord
import ffmpeg
import os
from src.utils.request import Request
from bs4 import BeautifulSoup

class Voice(AbstractPlugin):

    async def _get_message(self, ctx, message):
        self.logger.info(message[:1])
        self.logger.info(message[1:])
        if os.getenv('DISCORD_PREFIX') == message[:1]:
            if " " in message[1:]:
                command, query = message[1:].split(" ", 1)
            else:
                command = message[1:]

            self.logger.info('Found cascade command')
            response = await ctx.invoke(self.bot.get_command(command))
            self.logger.info(response)
            if response:
                return response

        return ctx.message.clean_content.replace(os.getenv('DISCORD_PREFIX') + "say", "")\
            .replace(os.getenv('DISCORD_PREFIX') + "speak", "")\
            .replace(os.getenv('DISCORD_PREFIX') + "play", "")\
            .replace("@", "")


    @commands.command(aliases=['speak', 'play'], help="Make me say something, or speak another command")
    async def say(self, ctx, *, message):

        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel for this to work")
            return
        channel = ctx.author.voice.channel

        new_message = await self._get_message(ctx, message)

        # Female
        # url = 'https://readloud.net/english/american/2-girl-s-voice-sally.html'
        
        # Male 
        url = 'https://readloud.net/english/australian/48-male-voice-russell.html'

        data = {
            'but': "submit",
            'but1': new_message
        }

        response = Request().post(url, data=data, expire_after=1800)
        if not response:
            await ctx.send("Sorry something went wrong. Please try again later.....or not")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.findAll("source")
        # self.logger.info(content[0]['src'])
        # self.logger.info(content)
        if not content:
            self.logger.info("Content Not found")
            return
        self.logger.info(content[0])
        if not content[0]['src']:
            self.logger.info("Src Not found")
            return

        audio_path = content[0]['src']
        self.logger.info(audio_path)

        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)

        audio_source = discord.FFmpegPCMAudio('https://readloud.net' + audio_path, options='-filter:a "atempo=0.85"')


        # maybe better join example
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            voice_client = await channel.connect()

        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)

        await ctx.message.add_reaction('\U0001f44d')

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
