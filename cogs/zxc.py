from random import randint
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter, MemberNotFound
from PIL import Image, ImageDraw, ImageFont
import asyncio
import io
import requests
from config import cluster_con
from checks import is_admin
zxcList = []


class Zxc(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['zxc','duel','зхц','дуэль'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def __zxc(self, ctx, rawMember, rawAmount):
        await ctx.message.delete(delay = 3)
        global zxcList
        converter = MemberConverter()

        try:
            member = await converter.convert(ctx, rawMember)
            amount = rawAmount

        except MemberNotFound:
            member = await converter.convert(ctx, rawAmount)
            amount = rawMember


        if member == ctx.author:
            e = discord.Embed(description = f"Укажите пользователя, которому хотите бросить вызов", color = discord.Colour.dark_red()).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
            ctx.command.reset_cooldown(ctx)
        else:
            if amount == "all":
                amount = self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["money"]
            elif amount == "uall":
                amount = self.collusers.find_one({"user_id": member.id, "guild_id": ctx.guild.id})["money"]
            elif amount.isnumeric() == True:
                amount = int(amount)
            else:
                e = discord.Embed(description = f"Неверная ставка!", color=discord.Colour.dark_red())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)
                ctx.command.reset_cooldown(ctx)
                return
            if f"{member}" in zxcList:
                e = discord.Embed(description = f"У данного пользователя есть незаконченная игра, дождитесь результатов.", color = discord.Colour.dark_red()).set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                ctx.command.reset_cooldown(ctx)
                await ctx.send(embed = e)
            elif f"{ctx.author}" in zxcList:
                e = discord.Embed(description = f"У вас есть незаконченная игра, дождитесь результатов.", color = discord.Colour.dark_red()).set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                ctx.command.reset_cooldown(ctx)
                await ctx.send(embed = e)
            elif self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["zxcskin"] == "":
                e = discord.Embed(description = f"У вас нет персонажа для игр", color=discord.Colour.dark_red())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                e.set_footer(text = "Чтобы приобрести введите !zxcshop")
                await ctx.send(embed = e)
            elif self.collusers.find_one({"user_id":member.id,"guild_id":ctx.guild.id})["zxcskin"] == "":
                e = discord.Embed(description = f"У пользователя нет персонажа для игр", color=discord.Colour.dark_red())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                e.set_footer(text = "Чтобы приобрести введите !zxcshop")
                await ctx.send(embed = e)
            elif amount < 100:
                e = discord.Embed(description = f"Минимальная ставка **100** <:hcoin:871123082029445130>", color=discord.Colour.dark_red()).set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)
            elif self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["money"] < amount:
                e = discord.Embed(description = f"""У вас недостаточно <:hcoin:871123082029445130> на счету\n```\nНеобходимо: {amount}\nНедостаточно: {amount - self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["money"]}```""", color=discord.Colour.dark_red())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)
            elif self.collusers.find_one({"user_id": member.id, "guild_id": ctx.guild.id})["money"] < amount:
                e = discord.Embed(description = f"""У пользователя {member.mention} недостаточно <:hcoin:871123082029445130> на счету
                    \n```\nНеобходимо: {amount}\nНедостаточно: {amount - self.collusers.find_one({"user_id": member.id, "guild_id": ctx.guild.id})["money"]}```""",
                     color=discord.Colour.dark_red())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)
            
            else:

                zxcList.append(f"{member}")
                zxcList.append(f"{ctx.author}")

                e = discord.Embed(description = f"Бросает вам вызов на сумму **{amount}** <:hcoin:871123082029445130>", color = discord.Color.dark_green())
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                e.set_footer(text="Сможете ли вы доказать, что сильнее его?")
                msg = await ctx.send(f"{member.mention}", embed = e)
                yes = "<:yes:870307647285526528>"
                no = "<:no:870308083434422354>"
                await msg.add_reaction(emoji=yes)
                await msg.add_reaction(emoji=no)
                emojis = [yes, no]

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == member and str(reaction.emoji) in emojis, timeout=20.0)

                except asyncio.TimeoutError:
                    await msg.delete()
                    time = discord.Embed(description = f"Пользователь **{member.mention}** отказался от вызова(тайм-аут)", color=discord.Colour.dark_gold())
                    time.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed = time)
                    zxcList.remove(f"{member}")
                    zxcList.remove(f"{ctx.author}")
                    ctx.command.reset_cooldown(ctx)

                else:
                    if str(reaction.emoji) == yes:
                        await msg.delete()
                        channel = self.bot.get_channel(880487426949279815)
                        PlayerOneUrl = self.collusers.find_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id})["zxcskin"]
                        PlayerTwoUrl = self.collusers.find_one({"user_id":member.id,"guild_id":ctx.guild.id})["zxcskin"]
                        fightUrl = "https://media.discordapp.net/attachments/870980591741456444/880081427146878976/zxc.png"
                        
                        imgPlayerOne = Image.open(requests.get(PlayerOneUrl, stream=True).raw)
                        imgPlayerTwo = Image.open(requests.get(PlayerTwoUrl, stream=True).raw)
                        imgFight = Image.open(requests.get(fightUrl, stream=True).raw)
                        
                        imgFight.paste(imgPlayerOne, (30,50), imgPlayerOne)
                        imgFight.paste(imgPlayerTwo, (700,50), imgPlayerTwo)

                        with io.BytesIO() as image_binary:
                            imgFight.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            e = discord.Embed(description = f"Да начнетcя великая битва между **{ctx.author.mention}** и **{member.mention}**", color = discord.Colour.magenta())
                            
                            image = await channel.send(f"{ctx.author} and {member}", file=discord.File(fp=image_binary, filename='fight.png'))
                            attachment = await channel.fetch_message(image.id)

                            e.set_image(url = attachment.attachments[0])
                            fight = await ctx.send(embed = e)

                        await asyncio.sleep(3)
                        e = discord.Embed(description = f"Битва начнется через **3...**", color = discord.Colour.magenta())
                        e.set_image(url = attachment.attachments[0])
                        await fight.edit(embed = e)
                        await asyncio.sleep(1)
                        e = discord.Embed(description = f"Битва начнется через **2...**", color = discord.Colour.magenta())
                        e.set_image(url = attachment.attachments[0])
                        await fight.edit(embed = e)
                        await asyncio.sleep(1)
                        e = discord.Embed(description = f"Битва начнется через **1...**", color = discord.Colour.magenta())
                        e.set_image(url = attachment.attachments[0])
                        await fight.edit(embed = e)

                        random = randint(1,100)
                        winMoney = round(amount*0.98)
                        
                        if random < 50:
                            winPlayer = Image.open(requests.get(PlayerOneUrl, stream=True).raw)
                            winNick = u"{}".format(ctx.author)
                            self.collusers.update_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id},{"$inc":{"money":winMoney}})
                            self.collusers.update_one({"user_id":member.id,"guild_id":ctx.guild.id},{"$inc":{"money":-amount}})

                            self.collusers.update_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id},{"$inc":{"zxcstat.win":winMoney}})
                            self.collusers.update_one({"user_id":member.id,"guild_id":ctx.guild.id},{"$inc":{"zxcstat.lose":amount}})
                            
                            e = discord.Embed(description = f"А вот и наш победитель - {ctx.author.mention}\nИ он забирает себе - **{winMoney}** <:hcoin:871123082029445130>", color = discord.Colour.magenta())
                        else:
                            winPlayer = Image.open(requests.get(PlayerTwoUrl, stream=True).raw)
                            winNick = u"{}".format(member)
                            self.collusers.update_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id},{"$inc":{"money":-amount}})
                            self.collusers.update_one({"user_id":member.id,"guild_id":ctx.guild.id},{"$inc":{"money":winMoney}})

                            self.collusers.update_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id},{"$inc":{"zxcstat.lose":amount}})
                            self.collusers.update_one({"user_id":member.id,"guild_id":ctx.guild.id},{"$inc":{"zxcstat.win":winMoney}})

                            e = discord.Embed(description = f"А вот и наш победитель - {member.mention}\n\nИ он забирает себе - **{winMoney}** <:hcoin:871123082029445130>", color = discord.Colour.magenta())
                        
                        winnerUrl = "https://media.discordapp.net/attachments/880116888380796999/881717672667140127/winner.png"
                        imgWinner = Image.open(requests.get(winnerUrl, stream=True).raw)
                        imgWinner.paste(winPlayer, (80,60), winPlayer)
                        draw = ImageDraw.Draw(imgWinner) 
                        selected_size = 1
                        for size in range(1, 150):
                            arial = ImageFont.truetype("DejaVuSans.ttf", size=size)
                            w, h = arial.getsize(winNick) 
                            if w > 400 or h > 60:
                                break
                        selected_size = size
                    
                        font = ImageFont.truetype("DejaVuSans.ttf", selected_size)
                        w, h = font.getsize(winNick)
                        draw.text((982-w//2, 183-h//2), winNick, fill="white", font=font, ancor="mm")

                        with io.BytesIO() as image_binary:
                            imgWinner.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            
                            image = await channel.send(f"winner", file=discord.File(fp=image_binary, filename='winner.png'))
                            attachment = await channel.fetch_message(image.id)

                            e.set_image(url = attachment.attachments[0])
                            
                            await fight.edit(embed = e)

                        zxcList.remove(f"{member}")
                        zxcList.remove(f"{ctx.author}")
                        ctx.command.reset_cooldown(ctx)

                    else:
                        await msg.delete()
                        no = discord.Embed(description = f"Пользователь **{member.mention}** отказался от вызова", color=discord.Colour.dark_gold())
                        no.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        await ctx.send(embed = no)
                        zxcList.remove(f"{member}")
                        zxcList.remove(f"{ctx.author}")
                        ctx.command.reset_cooldown(ctx)



    @commands.command(aliases = ['zxcshop'])
    async def __zxcshop(self, ctx):
        await ctx.message.delete(delay = 3)
        zxcshop = discord.Embed(description = f"Добро пожаловать в **ZXC магазин**", color=discord.Colour.dark_blue())
        zxcshop.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        zxcshop.set_image(url = "https://media.discordapp.net/attachments/880116888380796999/880159058026463242/zxcshop.png")
        zxcshop.set_footer(text="Чтобы купить персонажа - !zxcbuy *№*")
        await ctx.send(embed = zxcshop)


    @commands.command(aliases = ['zxcbuy'])
    async def __zxcbuy(self, ctx, num:int=0):
        await ctx.message.delete(delay = 3)
        zxcSkins = [
            'https://media.discordapp.net/attachments/880116888380796999/881619070531809300/sf1.png',
            'https://media.discordapp.net/attachments/880116888380796999/881619074348638248/sf2.png',
            'https://media.discordapp.net/attachments/880116888380796999/881619075053285446/sf3.png',
            'https://media.discordapp.net/attachments/880116888380796999/881619078710698005/sf4.png',
            'https://media.discordapp.net/attachments/880116888380796999/881619080216469524/sf5.png'
        ]
        zxcCost = [
            250,
            500,
            1000,
            4001,
            11111,
            25000
        ]
        if num == 0 or num > 6 or num < 0 :
            e = discord.Embed(description = f"Введите корректный номер персонажа", color=discord.Colour.dark_red())
            e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
            return
        if self.collusers.find_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id})["money"] < zxcCost[num-1]:
            e = discord.Embed(description = f"""У вас недостаточно средств\n\
                ```\nНеобходимо: {zxcCost[num-1]}\nНедостаточно: {zxcCost[num-1] - self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["money"]}```""", color=discord.Colour.dark_red())
            e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            if self.collusers.find_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id})["zxcskin"] == zxcSkins[num-1]:
                e = discord.Embed(description = f"У вас уже стоит данный персонаж!", color = discord.Color.dark_gold())
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed = e)
            else:
                e = discord.Embed(description = f"Вы уверены, что хотите купить персонажа по номером **{num}**?", color = discord.Color.dark_green())
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                e.set_footer(text=f"Стоимость: {zxcCost[num-1]}")
                if num != 6:
                    e.set_thumbnail(url = zxcSkins[num-1])
                msg = await ctx.send(embed = e)
                yes = "<:yes:870307647285526528>"
                no = "<:no:870308083434422354>"
                await msg.add_reaction(emoji=yes)
                await msg.add_reaction(emoji=no)
                emojis = [yes, no]

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in emojis, timeout=20.0)

                except asyncio.TimeoutError:
                    for remoji in emojis:
                        await msg.clear_reaction(remoji)

                else:
                    if str(reaction.emoji) == yes:
                        for remoji in emojis:
                            await msg.clear_reaction(remoji)
                        if num == 6:
                            
                            self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$inc":{"money":-zxcCost[num-1]}})
                            e = discord.Embed(description = f"Вы успешно приобрели **кастомного персонажа** <:lov_vctry:840440655616540682>\nЧтобы установить **кастомного персонажа** напишите в ЛС <@!217998824671674368>", color=discord.Colour.dark_green())
                            e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                            await msg.edit(embed = e)
                        else:
                            self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$inc":{"money":-zxcCost[num-1]}})
                            self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$set":{"zxcskin":zxcSkins[num-1]}})
            
                            e = discord.Embed(description = f"Вы успешно приобрели персонажа под номером **{num}** <:lov_vctry:840440655616540682>", color=discord.Colour.dark_green()) 
                            e.set_thumbnail(url = zxcSkins[num-1])
                            e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                            await msg.edit(embed = e)
                    else:
                        for remoji in emojis:
                            await msg.clear_reaction(remoji)


    @commands.command(aliases = ['zxcstat','hp'])
    async def __zxcstat(self, ctx, member:discord.Member = None):   
        await ctx.message.delete(delay=3)
        
        if member is None or member == ctx.author:
            if self.collusers.find_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id})["zxcskin"] == "":
                e = discord.Embed(description = f"У вас не установлен персонаж для игр.", color=discord.Colour.dark_red())
                e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                await ctx.send(embed = e)
            else:
                e = discord.Embed(description = f"Ваша статистика:", color=discord.Colour.dark_magenta())
                e.add_field(name="Выиграно:", value=f"""{self.collusers.find_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id})["zxcstat"]["win"]} <:hcoin:871123082029445130>""")
                e.add_field(name="Проиграно:", value=f"""{self.collusers.find_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id})["zxcstat"]["lose"]} <:hcoin:871123082029445130>""")
                e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                e.set_thumbnail(url=self.collusers.find_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id})["zxcskin"])
                await ctx.send(embed = e)
        else:
            if self.collusers.find_one({"user_id":member.id,"guild_id":ctx.guild.id})["zxcskin"] == "":
                e = discord.Embed(description = f"У {member.mention} не установлен персонаж для игр.", color=discord.Colour.dark_red())
                e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                await ctx.send(embed = e)
            else:
                e = discord.Embed(description = f"Статистика пользователя {member.mention}:", color=discord.Colour.dark_magenta())
                e.add_field(name="Выиграно:", value=f"""{self.collusers.find_one({"user_id":member.id,"guild_id":ctx.guild.id})["zxcstat"]["win"]} <:hcoin:871123082029445130>""")
                e.add_field(name="Проиграно:", value=f"""{self.collusers.find_one({"user_id":member.id,"guild_id":ctx.guild.id})["zxcstat"]["lose"]} <:hcoin:871123082029445130>""")
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                e.set_thumbnail(url=self.collusers.find_one({"user_id":member.id,"guild_id":ctx.guild.id})["zxcskin"])
                await ctx.send(embed = e)

    @__zxc.error
    async def zxc_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            ctx.command.reset_cooldown(ctx)
        if isinstance(error, commands.CommandOnCooldown):
            e = discord.Embed(description = f"У вас есть незаконченная игра, дождитесь результатов.", color=discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
            await ctx.message.delete(delay = 3)

def setup(bot):
    bot.add_cog(Zxc(bot)) 