import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter, MemberNotFound
from checks import is_admin
from config import cluster_con

class award(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users

    @commands.command(aliases = ['award'])
    @is_admin()
    async def __awardtest(self, ctx, rawMember, rawAmount):
        await ctx.message.delete(delay = 1)

        converter = MemberConverter()
        try:
            member = await converter.convert(ctx, rawMember)
            amount = int(rawAmount)
        except MemberNotFound:
            amount = int(rawMember)
            member = await converter.convert(ctx, rawAmount)

        self.collusers.update_one({"user_id": member.id, "guild_id": ctx.guild.id},{"$inc":{"money":amount}})
        await ctx.send(embed = discord.Embed(description = f"Вы успешно начислили **{amount}** <:hcoin:871123082029445130> на счет {member.mention}", color = discord.Colour.dark_green()))

        pm = discord.Embed(description = f"Администрация начислила на ваш счет **{amount}** <:hcoin:871123082029445130>", color = 0x006666)
        pm.set_footer(text = "С чего такая щедрость (｡◕‿◕｡)")
        # pm.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        # pm.set_thumbnail(url = member.avatar_url)
        await member.send(embed = pm)

        

        

def setup(bot):
    bot.add_cog(award(bot)) 