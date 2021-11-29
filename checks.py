from discord.ext.commands import check
from discord.ext.commands.errors import NoPrivateMessage

def is_admin():
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessage()
        return ctx.author.id == 217998824671674368 or 885950589916286997 in [role.id for role in ctx.author.roles]
    return check(predicate)