import discord
from discord.ext import commands
from random import randint
from config import cluster_con

class daily(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['daily', 'timely', 'дань', 'награда'])
    @commands.cooldown(1, 60*60*8, commands.BucketType.user)
    async def __daily(self,ctx):

        daily = randint(50,150)
        self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$inc":{"money":daily}})
        embed = discord.Embed(description = f"""Вам было начислено **{daily}** <:hcoin:871123082029445130> \nПриходите через **8 часов** за новой наградой!""", color=discord.Colour.dark_green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        # url = ctx.author.avatar_url
        # embed.set_thumbnail(url=url)
        await ctx.send(embed = embed)

        await ctx.message.delete(delay = 3)

    @__daily.error
    async def __daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            daily = self.bot.get_command('__daily')
            n = daily.get_cooldown_retry_after(ctx)
            hours = int(n/10*10/60/60)
            minutes = int((n - (hours*60*60))/60)


            embed = discord.Embed(description = f"""Вы пытаетесь слишком рано! \nПриходите через **{hours}ч.{minutes}м.** за новой ежедневной наградой""", color = discord.Colour.dark_red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = embed)

            await ctx.message.delete(delay = 3)

def setup(bot):
    bot.add_cog(daily(bot))