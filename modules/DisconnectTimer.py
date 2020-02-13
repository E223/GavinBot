import asyncio

class DisconnectTimer:
    def __init__(self, timeout, callback, ctx):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job(ctx))

    async def _job(self, ctx):
        await asyncio.sleep(self._timeout)
        while ctx.voice_client is not None and len(ctx.voice_client.channel.members) > 1:
            await asyncio.sleep(self._timeout)

        await ctx.send("No one has been in voice with me for 5 minutes :(")
        await ctx.send("Disconnecting")
        await self._callback(ctx)
        await self.cancel()

    def cancel(self):
        self._task.cancel()
