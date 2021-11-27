import discord
from discord.ext import commands, tasks
from checks import is_admin
from config import cluster_con
from datetime import datetime, timedelta
import asyncio
from random import choice

class GenshinDailyCheck(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collserver = self.cluster.server.guilds
        self.check_msg_loop.start()

    @commands.command(aliases = ['GIC_role'])
    @is_admin()
    async def __gic_role(self, ctx):
        await ctx.message.delete(delay = 3)
        channel = self.bot.get_channel(891606628900683796)
        e = discord.Embed(description = f"Если хотите получать уведомления об ежедневной отметке на сайте для прекрасной игры **Genshin Impact**, то нажмите на реакцию под сообщением 🔔 (｡◕‿◕｡)", color = discord.Colour.random())
        msg = await channel.send(embed = e)
        await msg.add_reaction(emoji = "🔔")
        self.collserver.update_one({"guild_id":ctx.guild.id},{"$set":{"GenCheckMsg":msg.id}})

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        msg_id = self.collserver.find_one({"guild_id":payload.guild_id})["GenCheckMsg"]
        channel = self.bot.get_channel(payload.channel_id)
        bot = self.bot.get_user(669930717467115561)
        if payload.user_id != bot.id:
            if payload.message_id == msg_id:
                if payload.emoji.name == "🔔":
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(891608383340285995)
                    await payload.member.add_roles(role)
                else:
                    msg = await channel.fetch_message(payload.message_id)
                    await msg.clear_reaction(payload.emoji)

    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        msg_id = self.collserver.find_one({"guild_id":payload.guild_id})["GenCheckMsg"]
        bot = self.bot.get_user(669930717467115561)
        if payload.user_id != bot.id:
            if payload.message_id == msg_id:
                if payload.emoji.name == "🔔":
                    guild = self.bot.get_guild(payload.guild_id)
                    member = discord.utils.get(guild.members, id=payload.user_id)
                    role = guild.get_role(891608383340285995)
                    await member.remove_roles(role)

    async def check_msg(self):
        now = datetime.now()
        now_time = now.strftime("%H:%M:%S")
        msg_time = timedelta(hours = 19, minutes = 0, seconds = 0)
        print(now_time,msg_time)
        time_diff = datetime.strptime(str(msg_time), "%H:%M:%S") - datetime.strptime(str(now_time), "%H:%M:%S")
        print(time_diff)
        diff = int(time_diff.total_seconds())
        img=[
            "https://static.wikia.nocookie.net/gensin-impact/images/c/c7/Paimon_Sticker_4.png/revision/latest/scale-to-width-down/250?cb=20210904023731",
            "https://static.wikia.nocookie.net/gensin-impact/images/2/25/Paimon_Sticker_3.png/revision/latest/scale-to-width-down/250?cb=20210904023729",
            "https://static.wikia.nocookie.net/gensin-impact/images/1/1b/Character_Paimon_Portrait.png/revision/latest/scale-to-width-down/1200?cb=20201205191049",
            "https://s3.getstickerpack.com/storage/uploads/sticker-pack/paimon-1/tray_large.png?4719dfd4ead6e5b35d544e7fa0421023",
            "https://chpic.su/_data/stickers/g/Genshin_Impact_Official_Chibi/Genshin_Impact_Official_Chibi_044.webp",
            "https://pbs.twimg.com/media/EnpKypPXEAMrDpt.png",
            "https://data.whicdn.com/images/351028515/original.png",
            "https://s3.getstickerpack.com/storage/uploads/sticker-pack/genshin-impact-emotes/sticker_16.png?bc85ec9270db3dc875b83d736ebd0c11&d=200x200",
            "https://upload-os-bbs.hoyolab.com/upload/2021/08/31/83235148/edb314f25773fc6a61f48284bfca6e72_2129823988784462183.png?x-oss-process=image/resize,s_740/quality,q_80/auto-orient,0/interlace,1/format,png",
            "https://64.media.tumblr.com/5285dcc83e9c73b02727c5cfa57d851a/1b3412ae36e99e85-6f/s400x600/c3cef6ebb19080534ff86ab81faf0e3fa834793c.png",
            "https://preview.redd.it/jvgqs4gl3a461.png?width=383&format=png&auto=webp&s=e421a03aec0e749a57bb87f0901857dd2d205786",
            "https://media.discordapp.net/attachments/825781617716101181/827181157921718293/Noellips.gif",
            "https://media.discordapp.net/attachments/825781617716101181/827181183854444564/Cubeichi.gif",
            
        ]
        if diff > 0:
            await asyncio.sleep(diff)
            channel = self.bot.get_channel(891606628900683796)
            e = discord.Embed(description = "Дзинь-дзинь, пора отметиться на сайте! 🔔\n\n\n**[Кликни, чтобы перейти](https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481)**", color = discord.Colour.random())
            e.set_thumbnail(url=choice(img))
            count = 0
            async for _ in channel.history(limit=None):
                count += 1
            if count >= 2:
                await channel.purge(limit=count-1)
            await channel.send(embed = e)
            await channel.send("<@&891608383340285995>", delete_after = 0)
        else: 
            print("I'am going to sleep for 12h. See you soon!")
            await asyncio.sleep(43200)
            self.check_msg_loop.restart()
           

    @tasks.loop(hours=24)
    async def check_msg_loop(self):
        print("check time for genshin")
        await self.check_msg()
        
    @check_msg_loop.before_loop
    async def before_dotaid(self):
        print('genshin check waiting...')
        await self.bot.wait_until_ready()
    
    @commands.command(aliases = ['msgcount'])
    @is_admin()
    async def message_count(self, ctx, channel: discord.TextChannel=None):
        await ctx.message.delete(delay = 3)
        channel = channel or ctx.channel
        count = 0
        async for _ in channel.history(limit=None):
            count += 1
        await ctx.send("There were {} messages in {}".format(count, channel.mention))

def setup(bot):
    bot.add_cog(GenshinDailyCheck(bot)) 