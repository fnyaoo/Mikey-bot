import discord
from discord.ext import commands
from config import cluster_con
from checks import is_admin

class twitch(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['addstream'])
    @is_admin()
    async def __addstream(self, ctx, nick:str):
        await ctx.message.delete(delay = 3)
        if nick is None:
            e = discord.Embed()

        
def setup(bot):
    bot.add_cog(twitch(bot)) 