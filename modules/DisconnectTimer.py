import asyncio

class DisconnectTimer:
    def __init__(self, timeout, callback, ctx):
        self.timeout_seconds = timeout
        self.timeout_minutes = int(timeout / 60)
        self.callback = callback
        self.task = asyncio.create_task(self.job(ctx))

    async def job(self, ctx):
        await asyncio.sleep(self.timeout)
        await ctx.send("No commands have been used for {} minutes. Disconnecting.".format(self.timeout_minutes))
        await self.callback(ctx)
        await self.cancel()

    async def cancel(self):
        self.task.cancel()
