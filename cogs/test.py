import discord
from discord.ext import commands
from config import cluster_con
import requests
import io


from PIL import Image

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'


class tst(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users
        self.collvoice = self.cluster.server.voicecounter

    @commands.command(aliases = ['tt'])
    async def test(self,ctx):

        await ctx.message.delete(delay = 1)
        await ctx.send("hfghfghfghfg")
        
def setup(bot):
    bot.add_cog(tst(bot)) 