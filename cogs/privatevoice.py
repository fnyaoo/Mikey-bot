from checks import is_admin
import discord
from discord.ext import commands
from config import cluster_con
from checks import is_admin

channelid = {}

class privatevoice(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collguild = self.cluster.server.guilds

    global channelid

    async def useradd(self, member, channel):
        channelid.update({f"{channel.id}":f"{member.id}"})

    async def userdelete(self,channel):
        channelid.pop(f"{channel.id}")

    async def channelcheck(self, member):
        try:
            if list(channelid.keys())[list(channelid.values()).index(str(member))] is not None:
                dictTup = list(channelid.items())
                reverseTup = dictTup[::-1]
                reverseDict = dict(reverseTup)
                if reverseDict != {}:
                    for k, v in reverseDict.items():
                        if v == str(member):
                            return k
        except ValueError: return False


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel or after.afk == False:
        
            privatemaker = self.collguild.find_one({"guild_id":member.guild.id})["private_ch"]
            privatecategory = self.collguild.find_one({"guild_id":member.guild.id})["private_ctg"]

            if after.channel and after.channel.id == privatemaker: #privatemaker 

                mainCategory = discord.utils.get(member.guild.categories, id=privatecategory) #privatecategory
                newchannel = await member.guild.create_voice_channel(name=f"{member.display_name}",category=mainCategory, user_limit = 2)
                await member.move_to(newchannel)
                await newchannel.set_permissions(member, connect = True) #, manage_channels=True
                await self.useradd(member, newchannel)
                def check(a,b,c):
                    return len(newchannel.members) == 0
                await self.bot.wait_for('voice_state_update', check=check)
                await newchannel.delete()
                await self.userdelete(newchannel)

            # if after.channel.category_id == privatecategory and after.channel.id != privatemaker:
            #     print(before.channel.user_limit)
        

    @commands.command(aliases = ['setprivate'])
    @is_admin()
    async def __setprivate(self, ctx, private:int = None):
        await ctx.message.delete(delay = 1)
        if private == None:
            e = discord.Embed(description = f"Укажите ID канала для создания приватов", color = discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            
            channel = discord.utils.get(ctx.guild.voice_channels, id = int(private))

            if channel is not None:
                self.collguild.update_one({"guild_id":ctx.guild.id}, {"$set":{"private_ctg":channel.category_id}})
                self.collguild.update_one({"guild_id":ctx.guild.id}, {"$set":{"private_ch":channel.id}})
                e = discord.Embed(description = f"Вы установили:\nПриватную категорию - `{channel.category}`\nПриватный канал - `{channel}`", color = discord.Colour.dark_green())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)
            else:
                e = discord.Embed(description = f"Такого канала не существует!", color = discord.Colour.gold())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)

    @commands.command(aliases = ['s','slots','с','слоты'])
    async def __slots(self, ctx, num:int = 1):
        await ctx.message.delete(delay = 3)
        channel = await self.channelcheck(ctx.author.id)
        if channel != False:
            channel = discord.utils.get(ctx.guild.voice_channels, id = int(channel))
            if num < 1:
                e = discord.Embed(description = f"Введите число слотов больше **0**!", color = discord.Color.dark_red())
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)
            else:
                if num > 5:
                    num = 5
                    e = discord.Embed(description = f"Было установлено максимальное число слотов - `{num}`", color = discord.Color.gold())
                else:
                    e = discord.Embed(description = f"Вы изменили кол-во слотов на `{num}`", color = discord.Color.dark_green())

                await channel.edit(user_limit = num)

                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                e.set_footer(text = "Также можно использовать - !s, !slots, !с, !слоты")
                await ctx.send(embed = e)

        else:
            e = discord.Embed(description = f"У вас нет приватного канала!", color = discord.Color.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)

    @commands.command(aliases = ['pname','название','к','канал'])
    async def __pname(self, ctx,*, pname):
        await ctx.message.delete(delay = 3)
        channel = await self.channelcheck(ctx.author.id)
        if channel != False:
            channel = discord.utils.get(ctx.guild.voice_channels, id = int(channel))
     
            await channel.edit(name = pname)
            e = discord.Embed(description = f"Вы поменяли название своего канала на `{pname}`", color = discord.Colour.dark_green())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            e.set_footer(text = "Также можно использовать - !название, !канал, !к")
            await ctx.send(embed = e)

        else:
            e = discord.Embed(description = f"У вас нет приватного канала!", color = discord.Color.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)

    @commands.command(aliases = ['pkick','кик'])
    async def __pkick(self, ctx, member:discord.Member = None):
        await ctx.message.delete(delay = 3)
        channel = await self.channelcheck(ctx.author.id)

        if channel != False:

            if member is None or member == ctx.author:
                e = discord.Embed(description = f"Укажите имя пользователя!", color = discord.Colour.gold())
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed = e)
            else:
                channel = discord.utils.get(ctx.guild.voice_channels, id = int(channel))
                if member in channel.members:
                    await member.move_to(channel = None)
                    
                    e = discord.Embed(description = f"Вы кикнули {member.mention}", color = discord.Colour.dark_green())
                    e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    e.set_footer(text = "Также можно использовать - !кик")
                    await ctx.send(embed = e)
                else:
                    e = discord.Embed(description = f"Пользователя нет в вашем канале!", color = discord.Colour.gold())
                    e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed = e)
        else:
            e = discord.Embed(description = f"У вас нет приватного канала!", color = discord.Color.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)

    @commands.command(aliases = ['pban','блок'])
    async def __pban(self, ctx, member:discord.Member = None):
        await ctx.message.delete(delay = 3)
        channel = await self.channelcheck(ctx.author.id)
        if channel != False:
            if member is None or member == ctx.author:
                e = discord.Embed(description = f"Укажите имя пользователя!", color = discord.Colour.gold())
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed = e)
            else:
                private = discord.utils.get(ctx.guild.voice_channels, id = int(channel))
                if member in private.members:
                    await member.move_to(channel = None)
                await private.set_permissions(member, overwrite=discord.PermissionOverwrite(connect = False))
                e = discord.Embed(description = f"Вы запретили {member.mention} присоединятся к вашему каналу!", color = discord.Colour.dark_green())
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                e.set_footer(text = "Также можно использовать - !блок")
                await ctx.send(embed = e)
            
        else:
            e = discord.Embed(description = f"У вас нет приватного канала!", color = discord.Color.dark_red())
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)

    # @commands.Cog.listener()
    # async def on_ready(self):
        

def setup(bot):
    bot.add_cog(privatevoice(bot)) 