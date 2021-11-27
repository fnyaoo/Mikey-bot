import discord
from discord.ext import commands
from config import cluster_con

class bio(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users
    @commands.command(aliases=['quote','цитата','статус','status','bio','био'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __bio(self, ctx, *quote):
        await ctx.message.delete(delay = 3)

        if len(quote) == 0:
            self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$set":{"quote":""}})
            e = discord.Embed(description = "Ваше описание было очищено!", colour = discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            s = ''
            if len(quote) > 0:
                for item in quote:
                    s = s + item + ' '
                s = s[:len(s)-1]
                if len(s) > 128:
                    e = discord.Embed(description = f"Ваша длина описания превышает **128** символов ||{len(s)}||", colour = discord.Colour.dark_red())
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)
                else:
                    self.collusers.update_one({"user_id": ctx.author.id, "guild_id": ctx.guild.id},{"$set":{"quote":s}})
                    e = discord.Embed(description = "Ваше описание было обновлено!", colour = discord.Colour.dark_green())
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)

    @__bio.error
    async def __bio_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            bio = self.bot.get_command('__bio')
            sec = round(bio.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)   
def setup(bot):
    bot.add_cog(bio(bot)) 