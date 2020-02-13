import asyncio

class DisconnectTimer:
    def __init__(self, timeout, callback, ctx):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.create_task(self._job(ctx))

    async def _job(self, ctx):
        await asyncio.sleep(self._timeout)
        mins = int(self._timeout / 60)
        await ctx.send("No commands have been used for {} minutes. Disconnecting.".format(mins))
        await self._callback(ctx)
        await self.cancel()

    async def cancel(self):
        self._task.cancel()
