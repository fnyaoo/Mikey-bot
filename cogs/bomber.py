import discord
from discord.ext import commands
from PIL import Image
from dislash import ActionRow, Button, ButtonStyle
from random import choice, randint
import requests
import io
from config import cluster_con

class bomber(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users
        self.collbomber = self.cluster.server.bomber

    @commands.command(aliases=['bomber','techies','b'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def __bomber(self, ctx, amount = None):

        await ctx.message.delete(delay = 3)

        if amount is None:
            e = discord.Embed(description = f"Введите вашу ставку!",color=discord.Colour.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
            ctx.command.reset_cooldown(ctx)
        elif amount.isnumeric() == False:
            e = discord.Embed(description = f"Неверная ставка!",color=discord.Colour.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
            ctx.command.reset_cooldown(ctx)
        elif int(amount) < 5:
            e = discord.Embed(description = f"Минимальная ставка **5** <:hcoin:871123082029445130>",color=discord.Colour.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
            ctx.command.reset_cooldown(ctx)
        elif int(amount) > 500:
            e = discord.Embed(description = f"Максимальная ставка **500** <:hcoin:871123082029445130>",color=discord.Colour.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
            ctx.command.reset_cooldown(ctx)
        elif self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["money"] < int(amount):
            e = discord.Embed(description = f"На вашем счету недостаточно средств!",color=discord.Colour.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
            ctx.command.reset_cooldown(ctx)   
        else:
            amount = int(amount)

            self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"money":-amount}})
            
            xmine = [90, 270, 450, 625, 805, 985]
            ymine = [130, 275, 420, 565]
            xpole = [70,250,430,609,788,969]
            redUrl = "https://media.discordapp.net/attachments/870980591741456444/881947358609420348/red.png"
            greenUrl = "https://media.discordapp.net/attachments/870980591741456444/881947351856607292/green.png"
            mineUrl = "https://media.discordapp.net/attachments/870980591741456444/881947355233026158/mine.png"
            boomUrl = "https://media.discordapp.net/attachments/870980591741456444/881947344369754142/boom.png"
            winimgUrl = "https://media.discordapp.net/attachments/870980591741456444/881947364833763368/win.png"
            gameoverUrl = "https://media.discordapp.net/attachments/870980591741456444/881947348127875112/game_over.png"
            red = Image.open(requests.get(redUrl, stream=True).raw).resize((167,571))
            green = Image.open(requests.get(greenUrl, stream=True).raw).resize((167,571))
            mine = Image.open(requests.get(mineUrl, stream=True).raw).resize((128,128))
            boom = Image.open(requests.get(boomUrl, stream=True).raw).resize((960,587))
            winimg = Image.open(requests.get(winimgUrl, stream=True).raw).resize((614,633))
            gameover = Image.open(requests.get(gameoverUrl, stream=True).raw).resize((585,301))



            channel = self.bot.get_channel(870268215484375063)

            # Make a row of buttons
            row_of_buttons = ActionRow(
                Button(
                    style=ButtonStyle.blurple,
                    label="1",
                    custom_id="1"
                ),
                Button(
                    style=ButtonStyle.blurple,
                    label="2",
                    custom_id="2"
                ),
                Button(
                    style=ButtonStyle.blurple,
                    label="3",
                    custom_id="3"
                ),
                Button(
                    style=ButtonStyle.blurple,
                    label="4",
                    custom_id="4"
                ),
                Button(
                    style=ButtonStyle.green,
                    label="Закончить игру",
                    custom_id="5"
                )
                
            )
            

            e = discord.Embed(title = f"Bomber", description = f"**Правила:**\n Вы должны угадать в какой клетке **НЕТ** мины, чтобы пройти в следующий столбик.\n Если вы не угадаете, то игра для вас закончится.", color = discord.Colour.random())
            e.set_image(url="https://media.discordapp.net/attachments/870980591741456444/879807302998310912/bomber.png")
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)    
            msg = await ctx.send(embed = e, components = [row_of_buttons])

            on_click = msg.create_click_listener(timeout=30)
            
            @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
            async def on_wrong_user(inter):
                await inter.reply("Это не ваша игра", ephemeral=True)

            
            @on_click.from_user(ctx.author)
            async def on_test_button(inter):
                await inter.respond(type = 6)
                button_text = inter.clicked_button.label
                await msg.edit(components=[])
                attemp = self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["bombattemp"] + 1
                comp = self.collbomber.find_one({"attemp":attemp})["computer"]
                player = self.collbomber.find_one({"attemp":attemp})["player"]


                if button_text == "Закончить игру":
                    attemp = self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["bombattemp"]
                    multiplier = self.collbomber.find_one({"attemp":attemp})["multiplier"]
                    won = round(amount*multiplier)
                    self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"money": won}})
                    self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$set":{"bombattemp": 0}})

                    bomberImgUrl = msg.embeds[0].image.url

                    edit = Image.open(requests.get(bomberImgUrl, stream=True).raw)
                    edit.paste(gameover,(310,208),gameover)


                    with io.BytesIO() as image_binary:
                        edit.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        image = await channel.send(f"{ctx.author}", file=discord.File(fp=image_binary, filename='bomber.png'))   
                        attachment = await channel.fetch_message(image.id)
                

                    if attemp == 0:
                        e = discord.Embed(title = "Игра окончена!", description=f"Вы закончили игру так и не начав играть <:thinking:848954241581711370> \nВаши средства были возвращенны на ваш счет <a:cat_ok:871130289886363778>", color = discord.Colour.dark_green())
                        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url) 
                        e.set_image(url = attachment.attachments[0])
                    else:
                        e = discord.Embed(title = "Игра окончена!", description=f"Вы закончили игру и смогли выиграть **{won}** <:hcoin:871123082029445130>", color = discord.Colour.dark_green())
                        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url) 
                        e.set_image(url = attachment.attachments[0])

                    await msg.edit(embed = e, components=[])
                    on_click.kill()
                    ctx.command.reset_cooldown(ctx)

                else: 
                    
                    chance = randint(0, 100)
                    lose = chance - comp
                    win = lose - player

                    if lose < 0:
                        bomberImgUrl = msg.embeds[0].image.url

                        edit = Image.open(requests.get(bomberImgUrl, stream=True).raw)
                        edit.paste(red, (xpole[attemp-1], 129), red)
                        edit.paste(mine, (xmine[attemp-1],ymine[int(button_text)-1]), mine)
                        edit.paste(boom,(123,83),boom)

                        with io.BytesIO() as image_binary:
                            edit.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            image = await channel.send(f"{ctx.author}", file=discord.File(fp=image_binary, filename='bomber.png'))   
                            attachment = await channel.fetch_message(image.id)
                            

                        e = discord.Embed(description = f"Вы выбрали **{button_text}** и там оказалась мина! Вы проиграли!", color = discord.Colour.dark_red())
                        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        e.set_footer(text = "Увы, вам не повезло...",icon_url="https://media.discordapp.net/attachments/870980591741456444/870980634217156658/pngaaa.com-653394.png")
                        e.set_image(url = attachment.attachments[0])
                        await msg.edit(content = None, embed = e, components=[])
                        self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$set":{"bombattemp": 0}})
                        on_click.kill()
                        ctx.command.reset_cooldown(ctx)

                    elif win <= 0:
                        ymas = [130, 275, 420, 565]
                        ymas.pop(int(button_text)-1)

                        bomberImgUrl = msg.embeds[0].image.url

                        edit = Image.open(requests.get(bomberImgUrl, stream=True).raw)

                        edit.paste(green, (xpole[attemp-1], 129), green)
                        edit.paste(mine, (xmine[attemp-1],choice(ymas)), mine)

                        with io.BytesIO() as image_binary:
                            edit.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            image = await channel.send(f"{ctx.author}", file=discord.File(fp=image_binary, filename='bomber.png'))   
                            attachment = await channel.fetch_message(image.id)

                        e = discord.Embed(description = f"Вы выбрали **{button_text}** и там не оказалось мины!\nВыберите следующую ячейку или заберите выигрыш.", color = discord.Colour.orange())
                        e.set_image(url = attachment.attachments[0])
                        multiplier = self.collbomber.find_one({"attemp":attemp})["multiplier"]
                        won = round(amount*multiplier)
                        e.set_footer(text = f"Ваш выигрыш составляет - {won}")
                        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"bombattemp": 1}})
                        await msg.edit(content = None, embed = e, components = [row_of_buttons]) 
                        
                        if attemp == 6:
                            bomberImgUrl = msg.embeds[0].image.url

                            edit = Image.open(requests.get(bomberImgUrl, stream=True).raw)

                            edit.paste(winimg, (308, 41), winimg)

                            with io.BytesIO() as image_binary:
                                edit.save(image_binary, 'PNG')
                                image_binary.seek(0)
                                image = await channel.send(f"{ctx.author}", file=discord.File(fp=image_binary, filename='bomber.png'))   
                                attachment = await channel.fetch_message(image.id)

                            
                            multiplier = self.collbomber.find_one({"attemp":attemp})["multiplier"]
                            won = round(amount*multiplier)
                            e = discord.Embed(titel = "Победа!",description = f"Вы дошли до последнего столбика! \nПоздравляем вас! \nВаш выигрыш составляет **{won}** <:hcoin:871123082029445130>", color = discord.Colour.magenta())
                            e.set_image(url = attachment.attachments[0])
                            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            await msg.edit(content = None, embed = e,components=[])
                            self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"money": won}})
                            self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$set":{"bombattemp": 0}})
                            on_click.kill()
                            ctx.command.reset_cooldown(ctx)

            @on_click.timeout
            async def on_timeout():
                attemp = self.collusers.find_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id})["bombattemp"]
                multiplier = self.collbomber.find_one({"attemp":attemp})["multiplier"]
                won = round(amount*multiplier)
                

                self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$inc":{"money": won}})
                self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$set":{"bombattemp": 0}})
                
                bomberImgUrl = msg.embeds[0].image.url

                edit = Image.open(requests.get(bomberImgUrl, stream=True).raw)

                edit.paste(gameover,(310,208),gameover)

                with io.BytesIO() as image_binary:
                    edit.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    image = await channel.send(f"{ctx.author}", file=discord.File(fp=image_binary, filename='bomber.png'))   
                    attachment = await channel.fetch_message(image.id)
                
                
                if attemp == 0:
                    e = discord.Embed(title = "Игра окончена!", description=f"Вы закончили игру(тайм-аут) так и не начав играть <:thinking:848954241581711370> \nВаши средства были возвращенны на ваш счет <a:cat_ok:871130289886363778>", color = discord.Colour.dark_green())
                    e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url) 
                    e.set_image(url = attachment.attachments[0])
                else:
                    e = discord.Embed(title = "Игра окончена!", description=f"Вы закончили игру(тайм-аут) и смогли выиграть **{won}** <:hcoin:871123082029445130>", color = discord.Colour.dark_green())
                    e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url) 
                    e.set_image(url = attachment.attachments[0])
                await msg.edit(embed = e, components=[])
                on_click.kill()
                ctx.command.reset_cooldown(ctx)

    
    @__bomber.error
    async def bomber_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            e = discord.Embed(description = f"У вас уже есть запущенная игра! \nДоиграйте сначала её!", color=discord.Colour.dark_red())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 3)
            await ctx.message.delete(delay = 3)

def setup(bot):
    bot.add_cog(bomber(bot))