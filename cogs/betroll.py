import discord
from discord.ext import commands
from random import randint
from config import cluster_con

lose = 0

class betroll(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['br', 'betroll'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def __betroll(self, ctx, amount):
        global lose
        await ctx.message.delete(delay = 3)
        if amount == "all":
            amount = self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["money"]
        elif amount.isnumeric() == True:
            amount = int(amount)
        else:
            e = discord.Embed(description = f"Неверная ставка!", color=discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
            return
        
        if amount < 5:
            e = discord.Embed(description = f"Минимальная ставка **5** <:hcoin:871123082029445130>", color=discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        elif amount > 500:
            e = discord.Embed(description = f"Максимальная ставка **500** <:hcoin:871123082029445130>", color=discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        elif self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["money"] < amount:
            e = discord.Embed(description = f"У вас недостаточно <:hcoin:871123082029445130> на счету", color=discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"money":-amount}})
            rand = randint(21,102)

            if lose > 3:
                lose = 0
                # print(lose)
            else:
                rand = rand - 20
                # print(lose)
            if rand < 51:
                e = discord.Embed(description = f"Выпало число **{rand}**, к сожалению, ты проиграл... ", color=discord.Colour.dark_red())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                e.set_footer(text = "｀、ヽ(×﹏×)ヽ☂ヽ｀、")
                await ctx.send(embed = e)
                lose +=1
            elif rand < 71:
                won = round(amount*1.5)
                self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"money":won}})
                e = discord.Embed(description = f"Выпало число **{rand}**, ты выиграл **{won}** <:hcoin:871123082029445130>", color=discord.Colour.dark_green())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                e.set_footer(text = "☆*ヾ(-∀・* )*+☆")
                await ctx.send(embed = e)
            elif rand < 86:
                won = round(amount*2)
                self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"money":won}})
                e = discord.Embed(description = f"Выпало число **{rand}**, ты выиграл **{won}** <:hcoin:871123082029445130>", color=discord.Colour.dark_green())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                e.set_footer(text = "☆*ヾ(-∀・* )*+☆")
                await ctx.send(embed = e)
            elif rand < 100:
                won = round(amount*3.5)
                self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"money":won}})
                e = discord.Embed(description = f"Выпало число **{rand}**, ты выиграл **{won}** <:hcoin:871123082029445130>", color=discord.Colour.dark_green())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                e.set_footer(text = "☆*ヾ(-∀・* )*+☆")
                await ctx.send(embed = e)
            elif rand < 102:
                won = round(amount*5)
                self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"money":won}})
                e = discord.Embed(description = f"Выпало число **{rand}**, ты выиграл **{won}** <:hcoin:871123082029445130>", color=discord.Colour.dark_green())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                e.set_footer(text = "☆*ヾ(-∀・* )*+☆")
                await ctx.send(embed = e)
        

    @__betroll.error
    async def bomber_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            give = self.bot.get_command('__betroll')
            sec = round(give.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)


def setup(bot):
    bot.add_cog(betroll(bot)) 