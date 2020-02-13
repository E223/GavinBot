import asyncio
import discord
import logging
import random
import os
from discord.ext import commands
from dotenv import load_dotenv
from errors import errors
from errors.ErrorHandler import ErrorHandler
from modules.DisconnectTimer import DisconnectTimer
from os import listdir
from os.path import isfile, join

load_dotenv(dotenv_path='.env')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
LAUGH_PATH = os.getenv('LAUGH_PATH')
QUESTION_PATH = os.getenv('QUESTION_PATH')
RESPONSE_PATH = os.getenv('RESPONSE_PATH')
TEST_PATH = os.getenv('TEST_PATH')

clips = {
    "laugh": LAUGH_PATH,
    "question": QUESTION_PATH,
    "response": RESPONSE_PATH,
    "test": TEST_PATH
}

logger = logging.getLogger('gavin')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='logs/error.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
logger.addHandler(handler)


class Gavin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_volume = 0.5
        self.playing_file_name = ""
        self.disconnect_time = 300

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        """Plays a random test clip"""
        file = self.get_random_file(TEST_PATH)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Playing clip: {}'.format(self.playing_file_name))

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot"""
        await ctx.send('Shutting Down.')
        await ctx.bot.logout()

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """
        Joins a specified voice channel, or, if no channel is specified and the user
        running the command is in a voice channel, joins the channel they are currently in.
        """
        global timer
        if channel is not None:
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)

            timer = DisconnectTimer(self.disconnect_time, self.stop, ctx)
            return await channel.connect()

        if ctx.author.voice:
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(ctx.author.voice.channel)

            timer = DisconnectTimer(self.disconnect_time, self.stop, ctx)
            return await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.command()
    async def question(self, ctx):
        """Plays a random Gavin question"""
        file = self.get_random_file(QUESTION_PATH)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Playing clip: {}'.format(self.playing_file_name))

    @commands.command()
    async def response(self, ctx):
        """Plays a random Gavin response"""
        file = self.get_random_file(RESPONSE_PATH)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Playing clip: {}'.format(self.playing_file_name))

    @commands.command()
    async def laugh(self, ctx):
        """Plays a random Gavin laugh"""
        file = self.get_random_file(LAUGH_PATH)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Playing clip: {}'.format(self.playing_file_name))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        self.last_volume = volume / 100
        ctx.voice_client.source.volume = self.last_volume

        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        self.playing_file_name = ""
        await ctx.voice_client.disconnect()

    @commands.command()
    async def list(self, ctx, list_name):
        """Lists the audio clips for the specified list name"""
        list_name = list_name.lower()
        if list_name not in clips:
            return await ctx.send("Invalid command")

        path = clips[list_name]
        files = [f for f in listdir(path) if isfile(join(path, f))]

        embed = discord.Embed(
            title=list_name.capitalize() + ' List',
            colour=discord.Colour.blue(),
        )

        embed.add_field(name='Clips', value="\n".join(files), inline=False)
        await ctx.send(embed=embed)

    @test.before_invoke
    @laugh.before_invoke
    @question.before_invoke
    @response.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
            raise errors.InvalidUserState("Author not connected to a voice channel.")

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    def get_random_file(self, path):
        """Gets a random file from a specified path"""
        files = [f for f in listdir(path) if isfile(join(path, f))]
        file_name = random.choice(files)
        self.playing_file_name = file_name

        return path + file_name


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description='Gavin sound samples')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))

bot.add_cog(Gavin(bot))
bot.add_cog(ErrorHandler(bot))
bot.run(DISCORD_TOKEN)
