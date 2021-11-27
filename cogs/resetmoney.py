import discord
from discord.ext import commands
import asyncio
from config import cluster_con

class resetmoney(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['resetmoney','moneyreset'])
    @commands.has_role(821153000834859018)
    async def __resetmoney(self,ctx):
        await ctx.message.delete(delay = 3)
        embed = discord.Embed(title = "Вы уверены, что хотите обнулить деньги на сервере?", color=0xffff00)

        yes = "<:yes:870307647285526528>"
        no = "<:no:870308083434422354>"
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(emoji=yes)
        await msg.add_reaction(emoji=no)
        await ctx.message.delete(delay = 3)
        emojis = [yes, no]

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in emojis, timeout=10.0)

        except asyncio.TimeoutError:
            for remoji in emojis:
                await msg.clear_reaction(remoji)
            time = discord.Embed(title = "Действие отменено(тайм-аут)", color=0xff0000)
            await msg.edit(embed = time)
            

        else:
            if str(reaction.emoji) == yes:
                self.collusers.update_many({"guild_id":ctx.guild.id},{"$set":{"money": 0}})
                for remoji in emojis:
                    await msg.clear_reaction(remoji)
                yes = discord.Embed(title = "Обнуление прошло успешно", color=0x1ec88f)
                await msg.edit(embed = yes)
            else:
                for remoji in emojis:
                    await msg.clear_reaction(remoji)
                no = discord.Embed(title = "Действие отменено", color=0xff0000)
                await msg.edit(embed = no)

def setup(bot):
    bot.add_cog(resetmoney(bot))