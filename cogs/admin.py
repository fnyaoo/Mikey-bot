import discord
from discord.ext import commands
from checks import is_admin

class admin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command(aliases = ['admin'])
    @is_admin()
    async def __admin(self, ctx):
        await ctx.message.delete(delay = 3)
        await ctx.send("https://tenor.com/view/mda-admin-discord-ebalo-gif-19939672")

        
def setup(bot):
    bot.add_cog(admin(bot)) 