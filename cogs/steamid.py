import json
import discord
from discord.ext import commands,tasks
from config import cluster_con
import asyncio
from checks import is_admin
import requests
import json



class steam(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users
        self.dotaid.start()

    @tasks.loop(minutes=30)
    async def dotaid(self):
        row = self.collusers.find({"steamid":{"$nin":[0,1]}})
        for row in row:
            account_id = row["steamid"]
            member = row["user_id"]
            oldWin = row["wins"]

            r = requests.get(f"https://api.opendota.com/api/players/{account_id}/wl")
            data = r.json()
            win = data["win"]

        
            if oldWin < win:
                user = self.bot.get_user(member)
                self.collusers.update_one({"user_id":member,"steamid":account_id}, {"$set":{"wins":win}})
                result = win - oldWin
                money = result * 50
                self.collusers.update_one({"user_id":member,"steamid":account_id}, {"$inc":{"money":money}})
                e = discord.Embed(description = f"За победы в Dota 2 вам было начислено {money} <:hcoin:871123082029445130>", color = discord.Colour.magenta())
                e.set_author(name = user, icon_url = user.avatar_url)
                e.set_footer(text = "Поздравляем ☆*ヾ(-∀・* )*+☆")
                await user.send(embed = e)
                print(f"Give {money} to {user} for {result} wins")
    
    @dotaid.before_loop
    async def before_dotaid(self):
        print('dota waiting...')
        await self.bot.wait_until_ready()


    @commands.command(aliases=['stoploop'])
    @is_admin()
    async def stop_dotaid(self,ctx):
        print("stopped")
        await self.dotaid.cancel()
        
    @commands.command(aliases=['startloop'])
    @is_admin()
    async def start_dotaid(self,ctx):
        print("started")
        await self.dotaid.start()
        

    @commands.command(aliases=['steamid', 'sid','dotaid'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __setsteam(self, ctx, steamid:int = None):
        await ctx.message.delete(delay = 3)
        data = self.collusers.find_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id})["steamid"]

        if steamid is None:
            if data == 0:
                e = discord.Embed(title = "У вас не установлен Dota ID", color=discord.Colour.dark_green())
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed = e)
            else:
                e = discord.Embed(title = f"Ваш Dota ID `{data}`", color=discord.Colour.dark_green())
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed = e)
        elif data == 1:
            e = discord.Embed(title = f"Ваш Dota ID находится уже на проверке", color=discord.Colour.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
        elif data != 0:
            e = discord.Embed(title = f"У вас уже установлен Dota ID - `{data}`", color=discord.Colour.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
        # elif len(str(steamid)) != 17:
        #     e = discord.Embed(title = "Неправильная длина Dota ID!",description = "Используйте SteamID длиной в 17 символов!\nИ проверьте, чтобы была открыта история матчей", color=discord.Colour.dark_red())
        #     e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        #     await ctx.send(embed = e)
        else:
            self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$set":{"steamid":1}})
            e = discord.Embed(title = f"Ваш Dota ID `{steamid}` ушел на проверку модерации",description = "Убедитесь, что ваша история игр открыта!", color=discord.Colour.dark_green())
            e.set_author(name=ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
            channel = self.bot.get_channel(874433507206762586)
            yes = "<:yes:870307647285526528>"
            no = "<:no:870308083434422354>"
            emojis = [yes, no]
            approve = discord.Embed(description = f"Пользователь {ctx.author.mention} запросил проверку своего Dota ID \n```{steamid}```\n Используйте реакции для подтверждения", color=discord.Colour.gold())
            role = ctx.author.guild.get_role(821153000834859018)
            await channel.send(f"{role.mention}", delete_after = 1)
            msg = await channel.send(embed = approve)
            await msg.add_reaction(emoji=yes)
            await msg.add_reaction(emoji=no)
            def check(reaction, user):
                bot = self.bot.get_user(669930717467115561)
                return user != bot and str(reaction.emoji) in emojis
            
            reaction, user = await self.bot.wait_for('reaction_add', check=check)

            if str(reaction.emoji) == yes:
                self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$set":{"steamid":steamid}})
                r = requests.get(f"https://api.opendota.com/api/players/{steamid}/wl")
                data = r.json()
                win = data["win"]
                self.collusers.update_one({"user_id":ctx.author.id,"guild_id":ctx.guild.id, "steamid":steamid}, {"$set":{"wins":win}})
                for remoji in emojis:
                    await msg.clear_reaction(remoji)
                yes = discord.Embed(title = "Ваш Dota ID был подтвержден!", color = discord.Colour.dark_green())
                yes.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                approve = discord.Embed(description = f"Пользователь {ctx.author.mention} запросил проверку своего Dota ID \n```{steamid}```\n Было получено одобрение от {user.mention}", color=discord.Colour.dark_green())
                await msg.edit(embed = approve)
                await ctx.author.send(embed = yes)
            else:
                self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$set":{"steamid":0}})
                for remoji in emojis:
                    await msg.clear_reaction(remoji)
                no = discord.Embed(title = "Было отказано в установке Dota ID!", color = discord.Colour.dark_red())
                no.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                approve = discord.Embed(description = f"Пользователь {ctx.author.mention} запросил проверку своего Dota ID \n```{steamid}```\n Был получен отказ от {user.mention}", color=discord.Colour.dark_red())
    
                await msg.edit(embed = approve)
                await ctx.author.send(embed = no)
    @__setsteam.error
    async def __setsteam_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            setsteam = self.bot.get_command('__setsteam')
            sec = round(setsteam.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)
            

    @commands.command(aliases=['clearid','cid'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __clearsteam(self, ctx):
        await ctx.message.delete(delay = 3)
    
        data = self.collusers.find_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id})["steamid"]
        if data == 0:
            e = discord.Embed(description = f"У вас не установлен Dota ID", color=discord.Colour.gold())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            embed = discord.Embed(title = "Вы уверены, что хотите удалить свой Dota ID?", color=discord.Color.gold())
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            yes = "<:yes:870307647285526528>"
            no = "<:no:870308083434422354>"
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(emoji=yes)
            await msg.add_reaction(emoji=no)
            await ctx.message.delete(delay = 3)
            emojis = [yes, no]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in emojis, timeout=10.0)

            except asyncio.TimeoutError:
                for remoji in emojis:
                    await msg.clear_reaction(remoji)
                time = discord.Embed(title = "Удаление Dota ID отменено(тайм-аут)", color=0xff0000)
                time.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await msg.edit(embed = time)
                ctx.command.reset_cooldown(ctx)
                

            else:
                if str(reaction.emoji) == yes:
                    self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$set":{"steamid":0}})
                    self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id},{"$set":{"wins":0}})
                    for remoji in emojis:
                        await msg.clear_reaction(remoji)
                    yes = discord.Embed(title = "Ваш Dota ID был успешно очищен!", color=discord.Color.dark_green())
                    yes.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await msg.edit(embed = yes)
                    ctx.command.reset_cooldown(ctx)
                else:
                    for remoji in emojis:
                        await msg.clear_reaction(remoji)
                    no = discord.Embed(title = "Удаление Dota ID отменено", color=discord.Colour.dark_red())
                    no.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await msg.edit(embed = no)
                    ctx.command.reset_cooldown(ctx)
    
    @__clearsteam.error
    async def __clearsteam_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            e = discord.Embed(description = f"Вы уже пытаетесь удалить SteamID", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)

    @commands.command(aliases=['deleteid','did'])
    @is_admin()
    async def __deletesteam(self, ctx, member:discord.Member = None):
        await ctx.message.delete(delay = 3)
        data = self.collusers.find_one({"user_id":member.id, "guild_id":ctx.guild.id})["steamid"]
        if member is None:
            e = discord.Embed(description = "Укажите пользователя у которого надо удалить Dota ID", color=discord.Colour.gold())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
        elif data == 0:
            e = discord.Embed(description = f"У пользователя {member.mention} не установлен Dota ID", color=discord.Colour.gold())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            embed = discord.Embed(description = f"Вы уверены, что хотите удалить Dota ID у пользователя {member.mention}?", color=discord.Color.gold())
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            yes = "<:yes:870307647285526528>"
            no = "<:no:870308083434422354>"
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(emoji=yes)
            await msg.add_reaction(emoji=no)
            await ctx.message.delete(delay = 3)
            emojis = [yes, no]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in emojis, timeout=10.0)

            except asyncio.TimeoutError:
                for remoji in emojis:
                    await msg.clear_reaction(remoji)
                time = discord.Embed(title = "Удаление Dota ID отменено(тайм-аут)", color=0xff0000)
                time.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await msg.edit(embed = time)
                

            else:
                if str(reaction.emoji) == yes:
                    self.collusers.update_one({"user_id":member.id, "guild_id":ctx.guild.id},{"$set":{"steamid":0}})
                    for remoji in emojis:
                        await msg.clear_reaction(remoji)
                    yes = discord.Embed(description = f"Dota ID пользователя {member.mention} был успешно очищен!", color=discord.Color.dark_green())
                    yes.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await msg.edit(embed = yes)
                else:
                    for remoji in emojis:
                        await msg.clear_reaction(remoji)
                    no = discord.Embed(title = "Удаление Dota ID отменено", color=discord.Colour.dark_red())
                    no.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await msg.edit(embed = no)

def setup(bot):
    bot.add_cog(steam(bot)) 