from discord.ext import tasks, commands

class DisconnectTimer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.state = 0
        self.timeout_minutes = 10
        
    async def start(self, ctx):
        self.check_disconnect.start(ctx)
    
    async def restart(self, ctx):
        self.check_disconnect.restart(ctx)

    async def stop(self):
        self.state = 0
        self.check_disconnect.stop()

    @tasks.loop(minutes=10)
    async def check_disconnect(self, ctx):
        if self.state != 0:
            await ctx.send("No commands have been used for {} minutes. Disconnecting.".format(self.timeout_minutes))
            await self.bot.get_cog('Gavin').stop(ctx)
        else:
            self.state = 1
            
    @check_disconnect.after_loop
    async def reset_state(self):
        self.state = 0