import discord
from discord import Colour as color
from discord.ext import commands
from config import cluster_con


class shop(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users
        self.collshop = self.cluster.server.shop

    @commands.command(aliases=['additem','addshop'])
    @commands.has_role(821153000834859018)
    async def __additem(self, ctx, cost:int = None, *good):
        # print(good)
        s= ""
        for item in good:
            s = s + item + ' '
        good = s[:len(s)-1]

        if cost is None:
            await ctx.send(embed = discord.Embed(
                color = color.gold(),
                description = f"**{ctx.author}** введите стоимость товара!"
            ))
        elif cost < 0:
            await ctx.send(embed = discord.Embed(
                color = color.gold(),
                description = f"**{ctx.author}** введите стоимость товара большую нуля!"
            ))
        elif good == "":
            await ctx.send(embed = discord.Embed(
                color = color.gold(),
                description = f"**{ctx.author}** введите название товара!"
            ))
        else:
            num = self.collshop.count_documents({"guild_id":ctx.guild.id}) + 1
            values = {
                "num": num,
                "guild_id": ctx.guild.id,
                "good": good,
                "cost": cost
            }

            self.collshop.insert_one(values)

            e=discord.Embed(description = f"Вы успешно добавили товар **{good}** стоимостью **{cost}**", color = color.dark_green())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)

        await ctx.message.delete(delay = 3)

    @commands.command(aliases = ['removeshop','removeitem'])
    @commands.has_role(821153000834859018)
    async def __removeshop(self, ctx, num:int = None):
        if num is None:
            e = discord.Embed(description = "Введите номер товара, который вы хотите удалить!", color = discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        elif self.collshop.count_documents({"guild_id":ctx.guild.id,"num":num}) == 0:
            e = discord.Embed(description = "Такой товар не был обнаружен!", color = discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            result = self.collshop.find({"guild_id":ctx.guild.id,"num":num})
            for result in result:
                good = result["good"]
                cost = result["cost"]
            
            self.collshop.remove({"guild_id":ctx.guild.id, "num":num})
            e = discord.Embed(description = f"Товар **{good}** стоимостью **{cost}** был удален из магазина", color = discord.Colour.dark_green())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
    
    @commands.command(aliases = ['shop','магазин'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __shop(self, ctx):
        embed = discord.Embed(title = 'Магазин сервера', color = discord.Colour.dark_blue())
        counter = ""
        good = ""
        cost = ""
        row = self.collshop.find({"guild_id":ctx.guild.id})
        
        for row in row:
            counter = row["num"]
            good += f"{counter}. {row['good']}\n"
            cost += f"{row['cost']} <:hcoin:871123082029445130>\n"
        
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        embed.add_field(name = "Товар", value = f"{good}")
        embed.add_field(name = "Цена", value = f"{cost}")
        embed.set_footer(text = "Чтобы купить товар, введите !buy *номер товара*")
        embed.set_image(url = "https://media.discordapp.net/attachments/870980591741456444/873683628108959795/magaz.png")
        await ctx.send(embed = embed)

        await ctx.message.delete(delay = 3)

    @__shop.error
    async def __shop_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            shop = self.bot.get_command('__shop')
            sec = round(shop.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)


def setup(bot):
    bot.add_cog(shop(bot)) 