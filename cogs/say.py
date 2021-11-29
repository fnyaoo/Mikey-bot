import discord
from discord.ext import commands
from config import cluster_con
from checks import is_admin
import json

class SayCommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['say'])
    @is_admin()
    async def __say(self, ctx, *, message):
        await ctx.message.delete(delay = 3)
        try:
            dict = json.loads(message)
            e = discord.Embed(title = dict['title'], description = dict['description'], color = dict['color'])
            e.set_image(url = dict['image'])
            await ctx.send(embed = e)
        except Exception as e:
            await ctx.send(message)


        
def setup(bot):
    bot.add_cog(SayCommand(bot)) 