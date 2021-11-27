import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    
    @commands.command(aliases = ['help','помощь'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __help(self, ctx):
        await ctx.message.delete(delay = 3)


        embed1 = discord.Embed(title="Помощь по командам", description='Профиль', color = discord.Color.random())
        embed1.add_field(name = "Информация о профиле", value = "```!profile, !me, !p, !я, !профиль```", inline=False)
        embed1.add_field(name = "Установка описания профиля", value = "```!статус *текст*, если текст не отправлять, то описание будет удалено \nТакже работает !status, !bio, !цитата```", inline=False)
        embed1.add_field(name = "Привязать Dota ID", value = "```!dotaid *id*\n!clearid - чтобы удалить свой id```", inline=False)
        embed1.set_image(url = "https://media.discordapp.net/attachments/870980591741456444/875117565054173264/hel1p.png")
        embed1.set_footer(text = f"Страница 1/5")

        embed2 = discord.Embed(title="Помощь по командам", description='Игры', color = discord.Color.random())
        embed2.add_field(name = "Бомбер", value = "```!bomber *ставка*\nТакже можно !b, !techies```", inline=False)
        embed2.add_field(name = "Бетролл", value = "```!br *ставка*```", inline=False)
        embed2.add_field(name = "Проверить свою удачу", value = "```!рулетка *число*\n!roulette *число*```", inline=False)
        embed2.set_image(url = "https://media.discordapp.net/attachments/870980591741456444/875117565054173264/hel1p.png")
        embed2.set_footer(text = f"Страница 2/5")

        embed3 = discord.Embed(title="Помощь по командам", description='Валюта', color = discord.Color.random())
        embed3.add_field(name = "Проверить баланс", value = "```!$, !balance, !bal, !баланс, !money, !деньги```", inline=False)
        embed3.add_field(name = "Передать валюту", value = "```!give @линк сумма```", inline=False)
        embed3.add_field(name = "Ежедневная награда", value = "```!daily, !timely, !дань, !награда```", inline=False)
        embed3.add_field(name = "Топ богачей", value = "```!topmoney, !lb, !leaderboard, !tm```", inline=False)
        embed3.set_image(url = "https://media.discordapp.net/attachments/870980591741456444/875117565054173264/hel1p.png")
        embed3.set_footer(text = f"Страница 3/5")

        embed4 = discord.Embed(title="Помощь по командам", description='Приватные комнаты', color = discord.Color.random())
        embed4.add_field(name = "Поменять количество слотов", value = "```!slots *кол-во слотов(макс 5)*```", inline=False)
        embed4.add_field(name = "Запретить пользователю подключаться", value = "```!pban *линк*```", inline=False)
        embed4.add_field(name = "Кикнуть пользователя с канала", value = "```!pkick *линк*```", inline=False)
        embed4.add_field(name = "Изменить название вашего канала", value = "```!pname *название*```", inline=False)
        embed4.set_image(url = "https://media.discordapp.net/attachments/870980591741456444/875117565054173264/hel1p.png")
        embed4.set_footer(text = f"Страница 4/5")
        
        embed5 = discord.Embed(title="Помощь по командам", description='Остальное', color = discord.Color.random())
        embed5.add_field(name = "Посмотреть аватар пользователя", value = "```!avatar *линк*```", inline=False)
        embed5.add_field(name = "Магазин", value = "```!shop```", inline=False)
        embed5.set_image(url = "https://media.discordapp.net/attachments/870980591741456444/875117565054173264/hel1p.png")
        embed5.set_footer(text = f"Страница 5/5")

        embeds = [embed1, embed2, embed3, embed4, embed5]
        message = await ctx.send(embed = embed1)

        await message.add_reaction('◀')
        await message.add_reaction('▶')

        def check(reaction, user):
            return user == ctx.author

        i = 0
        reaction = None

        while True:

            if str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed = embeds[i])
            elif str(reaction) == '▶':
                if i < len(embeds)-1:
                    i += 1
                    await message.edit(embed = embeds[i])
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 20.0, check = check)
                await message.remove_reaction(reaction, user)
            except:
                break

        await message.clear_reactions()


    @__help.error
    async def __help_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            hhelp = self.bot.get_command('__help')
            sec = round(hhelp.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)


        
        e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = e)

        
def setup(bot):
    bot.add_cog(help(bot)) 