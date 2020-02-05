"""
This code has no issues whatsoever, there is no possible room for improvement,
it is perfect in every way imaginable.
"""

import json
import discord
import random
from discord.ext import commands
from os import listdir
from os.path import isfile, join

clips = {
    'prefix': './clips/',
    'laugh': 'laughs/',
    'question': 'questions/',
    'response': 'responses/',
    'testing': 'testing/'
}


class Gavin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_volume = 0.5
        self.playing_file_name = ""

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        """Plays a random test clip"""
        path = clips['prefix'] + clips['testing']
        file = self.get_random_file(path)

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
        if channel is not None:
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)

            return await channel.connect()

        if ctx.author.voice:
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(ctx.author.voice.channel)

            return await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.command()
    async def question(self, ctx):
        """Plays a random Gavin question"""
        path = clips['prefix'] + clips['question']
        file = self.get_random_file(path)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Playing clip: {}'.format(self.playing_file_name))

    @commands.command()
    async def response(self, ctx):
        """Plays a random Gavin response"""
        path = clips['prefix'] + clips['response']
        file = self.get_random_file(path)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Playing clip: {}'.format(self.playing_file_name))

    @commands.command()
    async def laugh(self, ctx):
        """Plays a random Gavin laugh"""
        path = clips['prefix'] + clips['laugh']
        file = self.get_random_file(path)

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
        command = list_name.lower()
        if clips[command] is None:
            return await ctx.send("Invalid command")

        path = clips['prefix'] + clips[list_name]
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
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
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

with open('config.json') as config:
    data = json.load(config)
    bot.run(data['bot']['token'])
