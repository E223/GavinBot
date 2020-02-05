import json
import discord
import random
from discord.ext import commands
from os import listdir
from os.path import isfile, join

clips = {
    'prefix': './clips/',
    'laughs': 'laughs/',
    'question': 'questions/',
    'response': 'responses/',
    'testing': 'testing/'
}


class Gavin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_volume = 0.5
        self.playing_song = ""

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        """Plays a random test clip"""
        path = clips['prefix'] + clips['testing']
        files = [f for f in listdir(path) if isfile(join(path, f))]
        file_name = random.choice(files)
        file = path + file_name

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        self.playing_song = file
        await ctx.send('Playing clip: {}'.format(file_name))

    @commands.command()
    async def question(self, ctx):
        """Plays a random Gavin question"""
        path = clips['prefix'] + clips['questions']
        files = [f for f in listdir(path) if isfile(join(path, f))]
        file_name = random.choice(files)
        file = path + file_name

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        self.playing_song = file
        await ctx.send('Playing clip: {}'.format(file_name))

    @commands.command()
    async def response(self, ctx):
        """Plays a random Gavin response"""
        path = clips['prefix'] + clips['responses']
        files = [f for f in listdir(path) if isfile(join(path, f))]
        file_name = random.choice(files)
        file = path + file_name

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        self.playing_song = file
        await ctx.send('Playing clip: {}'.format(file_name))

    @commands.command()
    async def laugh(self, ctx):
        """Plays a random Gavin laugh"""
        path = clips['prefix'] + clips['laughs']
        files = [f for f in listdir(path) if isfile(join(path, f))]
        file_name = random.choice(files)
        file = path + file_name

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=self.last_volume)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        self.playing_song = file
        await ctx.send('Playing clip: {}'.format(file_name))

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

        self.playing_song = ""
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

    @staticmethod
    def get_random_file(path):
        """Gets a random file from a specified path"""
        files = [f for f in listdir(path) if isfile(join(path, f))]
        file_name = random.choice(files)
        return path + file_name


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Gavin sound samples')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))

bot.add_cog(Gavin(bot))

with open('config.json') as config:
    data = json.load(config)
    bot.run(data['bot']['token'])
