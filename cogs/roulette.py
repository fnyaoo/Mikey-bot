import discord
from discord.ext import commands
from random import randint
from config import cluster_con


class roulette(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['roulette', 'рулетка'])
    @commands.cooldown(1, 60*60*20, commands.BucketType.user)
    async def __roulette(self, ctx, num:int = None):
        await ctx.message.delete(delay = 3)
        if num == None:
            e = discord.Embed(title = "Испытай свою удачу", description = f"Попробуй угадать случайное число от **1** до **10** и получи **1000** <:hcoin:871123082029445130>", color = discord.Colour.dark_magenta())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
            ctx.command.reset_cooldown(ctx)
        elif num > 11 or num < 1:
            e = discord.Embed(description = f"Введите число от **1** до **10**", color = discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
            ctx.command.reset_cooldown(ctx)
            return
        else:
            luckynum = randint(1,10)
            if num == luckynum:
                self.collusers.update_one({"user_id": ctx.author.id, "guild_id":ctx.guild.id},{"$inc":{"money":1000}})
                e = discord.Embed(title = "Поздравляем!", description = f"Ты угадал число **{luckynum}** и получил **1000** <:hcoin:871123082029445130> на свой счёт", color = discord.Colour.dark_green())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)
            else:
                e = discord.Embed(title = f"Твоё число - {num}", description = f"Ты не смог угадать число **{luckynum}**, но не расстраивайся, лучше приходи через **20ч**", color = discord.Colour.orange())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)

    @__roulette.error
    async def __roulette_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete(delay = 3)
            daily = self.bot.get_command('__roulette')
            n = daily.get_cooldown_retry_after(ctx)
            hours = int(n/10*10/60/60)
            minutes = int((n - (hours*60*60))/60)


            embed = discord.Embed(description = f"""Вы пытаетесь слишком рано! \nПриходите через **{hours}ч.{minutes}м.**, чтобы снова испытать свою удачу""", color = discord.Colour.dark_red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = embed)

            
def setup(bot):
    bot.add_cog(roulette(bot)) 