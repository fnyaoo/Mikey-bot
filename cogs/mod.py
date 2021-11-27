import discord
from discord.ext import commands
from config import cluster_con
import asyncio

class Moderate(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['mute'])
    async def __mute(self, ctx, member:discord.Member):
        await ctx.message.delete()
        try:
            mute_role = discord.utils.get(ctx.guild.roles, id=756543331491905576)

        except:
            mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        else:
            await ctx.guild.create_role(name = "Muted")
            mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
            # mute_role.edit_role_positions(positions = 2)

        await member.add_roles(mute_role)
        await member.edit(mute = True)
        await ctx.send(f"{ctx.author} gave role mute to {member}")

        # if "h" in time_mute:
        #     asyncio.sleep(time_mute[:1] * 3600)
        #     await member.remove_roles(mute_role)
        #     await member.edit(mute = False)
        # elif "m" in time_mute:
        #     asyncio.sleep(time_mute[:1] * 60)
        #     await member.remove_roles(mute_role)
        #     await member.edit(mute = False)
        # else:
        #     pass


        """Временный мут
        Также вы можете сделать временный мут, для этого используйте модуль asyncio и метод sleep (asyncio.sleep).
        Пусть функция принимает параметр time_mute. Поставьте условие if "h" in time_mute:
        То есть, если вы пишите: !mute @user 1h, и в переменной time_mute находит букву "h" значит asyncio.sleep(time_mute[:1] * 3600)
        
        """
        
def setup(bot):
    bot.add_cog(Moderate(bot)) 