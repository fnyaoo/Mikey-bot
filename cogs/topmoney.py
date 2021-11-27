import discord
from discord.ext import commands
from config import cluster_con

class topmoney(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['topmoney','tm', 'leaderboard', 'lb'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __topmoney(self, ctx):
        embed = discord.Embed(title = "Топ богачей сервера", color=0x1ec88f)
        counter = 0
        users = ""
        money = ""
        row = self.collusers.find({"guild_id":ctx.guild.id,"money":{"$ne":0}}).limit(15).sort("money", -1)
      
        for row in row:
            bot_check = self.bot.get_user(row["user_id"])

            if bot_check.bot == False:
                counter+=1
                users += f"№{counter} `{bot_check}`\n"
                money += f"<:hcoin:871123082029445130> `{row['money']}`\n"
                if counter == 10:
                    break

        embed.add_field(
            name = f"Пользователи:",
            value = f"{users}",
            inline=True
        )   
        embed.add_field(
            name = f"Баланс:",
            value = f"{money}",
            inline = True
        )
        embed.set_image(url = "https://media.discordapp.net/attachments/870980591741456444/874410597461164032/money.gif")
        await ctx.send(embed = embed)

        await ctx.message.delete(delay = 3)

    @__topmoney.error
    async def __topmoney_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            topmoney = self.bot.get_command('__topmoney')
            sec = round(topmoney.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \nпопробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)   
def setup(bot):
    bot.add_cog(topmoney(bot))