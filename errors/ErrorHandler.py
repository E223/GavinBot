import logging
from discord.ext import commands
from errors import errors

logger = logging.getLogger('gavin')


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError, errors.InvalidUserState)
        error_attribute = getattr(error, 'original', error)

        if isinstance(error_attribute, ignored):
            return

        logger.error(error, exc_info=True)
