import discord
from discord.ext import commands
from random import choice
import asyncio
from config import cluster_con


class buy(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users
        self.collshop = self.cluster.server.shop


    async def winner(self,ctx,participant,):
        winner = choice(participant)
        user = self.bot.get_user(winner)
        self.collusers.update_one({"user_id": user.id, "guild_id": ctx.guild.id},{"$inc":{"money": 500}})
        e = discord.Embed(title = "РЕЗУЛЬТАТЫ ЛОТЕРЕИ", description = f"В данной лотереи побеждает {user.mention}, и он получает заветные **500** <:hcoin:871123082029445130>", color = discord.Colour.dark_purple())
        e.set_thumbnail(url = user.avatar_url)
        e.set_image(url = "https://media.discordapp.net/attachments/870980591741456444/873720237198045244/lottery.png")
        channel = self.bot.get_channel(869603902906056765)
        
        await channel.send(f"{user.mention}", embed = e)
        for x in participant:
            user = self.bot.get_user(x)
            await user.send(embed = e)
            self.collusers.update_one({"user_id":user.id, "guild_id":ctx.guild.id},{"$set":{"lottery": 0}})

    async def check_lottery(self,ctx):
        amount = self.collusers.count_documents({"guild_id":ctx.guild.id, "lottery": 1})
        participant = []
        result = self.collusers.find({"guild_id":ctx.guild.id, "lottery": 1})
        
        for result in result:
            participant.append(result["user_id"])
        if amount == 0:
            ok = ""    
            return amount, ok, participant
        else:
            for x in participant:
                if x == ctx.author.id:
                    ok = "У вас уже приобретен билет!"
                    return amount, ok, participant
                else:
                    ok = "" 
            return amount, ok, participant
    @commands.command(aliases = ['lottery','лотерея'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __lottery(self, ctx):
        await ctx.message.delete(delay = 3)
        amount, ok, participant = await self.check_lottery(ctx)
        e = discord.Embed(title = f"Количество участников лотереи - {amount}/3 ", color = discord.Colour.dark_blue())
        e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        if ok != "":
            e.set_footer(text = ok)
        await ctx.send(embed = e)
        
    @__lottery.error
    async def __lottery_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            lottery = self.bot.get_command('__lottery')
            sec = round(lottery.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)

    @commands.command(aliases = ['buy','купить'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __buy(self, ctx, good = None):
        await ctx.message.delete(delay = 3)
        if good is None:
            e = discord.Embed(description = f"Введите номер товара!", color = discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        elif good.isnumeric() == False :
            e = discord.Embed(description = f"Такого товара не существует!", color = discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        elif self.collshop.count_documents({"guild_id":ctx.guild.id}) < int(good):
            e = discord.Embed(description = f"Такого товара не существует!", color = discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            if self.collshop.find_one({"guild_id":ctx.guild.id, "num": int(good)})["cost"] > self.collusers.find_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id})["money"]:
                e = discord.Embed(description = f"На вашем счету недостаточно средств!", color = discord.Colour.dark_red())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)

            elif int(good) == 1:
                if self.collusers.count_documents({"user_id":ctx.author.id, "guild_id":ctx.guild.id, "lottery": 1 }) == 1:
                    e = discord.Embed(description = f"Вы уже приобрели **Лотерейный билет**!", color = discord.Colour.dark_red())
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)
                else:
                    self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$inc":{"money":-100}})
                    self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$set":{"lottery":1}})
                    e = discord.Embed(description = f"Вы приобрели **Лотерейный билет**", color = discord.Colour.dark_green())
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)

                amount, ok, participant = await self.check_lottery(ctx)
                if amount >= 3:
                    await asyncio.sleep(10)
                    await self.winner(ctx, participant)
    @__buy.error
    async def __buy_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            buy = self.bot.get_command('__buy')
            sec = round(buy.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)

                    
def setup(bot):
    bot.add_cog(buy(bot)) 