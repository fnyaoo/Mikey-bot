import discord
from discord.ext import commands
from config import cluster_con

class Voicetop(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['voicetop','topvoice', 'vlb','топонлайн'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __voicetop(self, ctx):
        embed = discord.Embed(title = "Топ онлайн сервера", color=0x1ec88f)
        counter = 0
        users = ""
        online = ""
        row = self.collusers.find({"guild_id":ctx.guild.id,"voicetime":{"$ne":0}}).limit(15).sort("voicetime", -1)
        for row in row:

            bot_check = self.bot.get_user(row["user_id"])

            if bot_check.bot == False:
                counter+=1
                users += f"№{counter} `{bot_check}`\n"
                voicetime = row["voicetime"]
                hours = int(voicetime/10*10/60/60)
                minutes = int((voicetime - (hours*60*60))/60)
                online += f"`{hours}ч.{minutes}м.`\n"
                if counter == 10:
                    break

        embed.add_field(
            name = f"Пользователи:",
            value = f"{users}",
            inline=True
        )   
        embed.add_field(
            name = f"Онлайн:",
            value = f"{online}",
            inline = True
        )

        await ctx.send(embed = embed)

        await ctx.message.delete(delay = 3)

    @__voicetop.error
    async def __voicetop_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            voicetop = self.bot.get_command('__voicetop')
            sec = round(voicetop.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)   
def setup(bot):
    bot.add_cog(Voicetop(bot))