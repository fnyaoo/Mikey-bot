import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter, MemberNotFound
from config import cluster_con


class give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['pay', 'give', 'передать'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __give(self, ctx, rawMember, rawAmount):
        await ctx.message.delete(delay = 3)
        converter = MemberConverter()
        try:
            member = await converter.convert(ctx, rawMember)

            if rawAmount == "all":
                amount = self.collusers.find_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id})["money"]
            else:
                amount = int(rawAmount)

        except MemberNotFound:
            member = await converter.convert(ctx, rawAmount)

            if rawMember == "all":
                amount = self.collusers.find_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id})["money"]
            else:
                amount = int(rawMember)
        
        if member == ctx.author:
            e = discord.Embed(description = f"Себе нельзя переводить!", color = discord.Colour.dark_red())
            e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)

        elif amount < 1:
            e = discord.Embed(description = f"Введите сумму больше нуля!", color = discord.Colour.dark_red())
            e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)

        elif amount > self.collusers.find_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id})["money"]:
            e = discord.Embed(description = f"У вас недостаточно средств на счету!", color = discord.Colour.dark_red())
            e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            await ctx.send(embed = e)
        else:
            self.collusers.update_one({"user_id":member.id, "guild_id":ctx.guild.id},{"$inc":{"money":amount}})
            self.collusers.update_one({"user_id":ctx.author.id, "guild_id":ctx.guild.id}, {"$inc":{"money":-amount}}) 

            embed=discord.Embed(description = f"Вы перевели **{amount}** <:hcoin:871123082029445130> {member.mention}", color=discord.Colour.dark_green())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text="Ого, Вы такой щедрый 💸")
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)
            
            pm = discord.Embed(description = f"Перевел на ваш счет **{amount}** <:hcoin:871123082029445130>", color = 0x006666)
            pm.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await member.send(embed = pm)
    

    @__give.error
    async def __give_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            give = self.bot.get_command('__give')
            sec = round(give.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)
            


def setup(bot):
    bot.add_cog(give(bot))
