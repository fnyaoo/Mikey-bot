import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter, MemberNotFound

class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(821153000834859018)
    async def clear(self, ctx, number = 10):

            try:
                limit = int(number) + 1
            except:
                return await ctx.send("Введите корректно количество сообщений", delete_after = 3)
           
            await ctx.channel.purge(limit=limit)
            await ctx.send(embed = discord.Embed(color=discord.Colour.dark_red(),description = f"Было удалено **{limit-1}** сообщений!"),delete_after = 3)
      

def setup(bot):
    bot.add_cog(clear(bot))