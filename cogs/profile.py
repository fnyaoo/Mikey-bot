import discord
from discord.ext import commands
from config import cluster_con

class profile(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases=['profile','p','я','me','профиль'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __profile(self, ctx, member: discord.Member = None):
        await ctx.message.delete(delay = 3)
        if member is None or member == ctx.author:
            member = ctx.author
            
        e = discord.Embed(title = f"Профиль {member}", colour = 0x2F3136)
        e.set_thumbnail(url = member.avatar_url)
        if member != ctx.author:
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        money = self.collusers.find_one({"user_id":member.id, "guild_id":ctx.guild.id})["money"]
        quote = self.collusers.find_one({"user_id":member.id, "guild_id":ctx.guild.id})["quote"]
        voicetime = self.collusers.find_one({"user_id":member.id, "guild_id":member.guild.id})["voicetime"]
        hours = int(voicetime/10*10/60/60)
        minutes = int((voicetime - (hours*60*60))/60)
        # color = self.collusers.find_one({"user_id":member.id, "guild_id":member.guild.id})["color"]
        if quote  != "":
            e.add_field(name = "О себе:", value = f"```\n{quote}```", inline=False)
        else:
            e.add_field(name = "О себе:", value = f"```\nПусто...```", inline=False)

        e.add_field(name = "Онлайн:", value = f"```\n{hours}ч.{minutes}м.```")
        e.add_field(name = "МОнетки:", value = f"```\n{money}```")
        e.set_image(url = "https://media.discordapp.net/attachments/870980591741456444/872055257914572830/1.gif")
        steamid = self.collusers.find_one({"user_id":member.id, "guild_id":ctx.guild.id})["steamid"]
        if steamid != 0:
            e.add_field(name = "Steam ID:", value = f"```\n{steamid}```", inline=False)
        await ctx.send(embed = e)

        
    @__profile.error
    async def __profile_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            profile = self.bot.get_command('__profile')
            sec = round(profile.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)

def setup(bot):
    bot.add_cog(profile(bot)) 