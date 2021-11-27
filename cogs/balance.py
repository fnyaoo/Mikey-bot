import discord
from discord.ext import commands
from config import cluster_con

class Balance(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['$','balance','bal','money','деньги','баланс'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __balance(self, ctx, member: discord.Member = None):
        await ctx.message.delete(delay = 3)
        if member is None or member == ctx.author:
            e = discord.Embed(description = f"""Ваш баланс: \n\n**{self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})['money']}** <:hcoin:871123082029445130>""", color=0xa3d4ff)
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            e = discord.Embed(description = f"""Баланс пользователя **{member}**: \n\n **{self.collusers.find_one({"user_id": member.id, "guild_id": ctx.guild.id})['money']}** <:hcoin:871123082029445130>""", color=0xa3d4ff)
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)

        
        
    @__balance.error
    async def __balance_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            balance = self.bot.get_command('__balance')
            sec = round(balance.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)   
            
def setup(bot):
    bot.add_cog(Balance(bot))