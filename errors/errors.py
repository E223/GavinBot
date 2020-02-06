from discord.ext.commands import CommandError


class InvalidUserState(CommandError):
    def __init__(self, message=None, *args):
        super().__init__(message, *args)
