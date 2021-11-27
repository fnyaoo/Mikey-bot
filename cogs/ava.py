import discord
from discord.ext import commands

class ava(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['ava', 'avatar', 'ава', 'аватар'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __avatar(self, ctx, member: discord.Member = None):
        if member is None or member == ctx.author:
            e = discord.Embed(
                description = f"Ваш аватар:"
            )
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            e.set_image(url = ctx.author.avatar_url)

            await ctx.send(embed = e)
        else:
            e = discord.Embed(
                description = f"Аватар пользователя **{member}**:"
            )
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            e.set_image(url = member.avatar_url)

            await ctx.send(embed = e)
        await ctx.message.delete(delay = 3)

    @__avatar.error
    async def __avatar_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            avatar = self.bot.get_command('__avatar')
            sec = round(avatar.get_cooldown_retry_after(ctx),2)
            e = discord.Embed(description = f"Вы пытаетесь слишком часто! \n попробуйте через **{sec}мс.**", color=discord.Colour.gold())
            e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e, delete_after = 1)
            await ctx.message.delete(delay = 3)   
def setup(bot):
    bot.add_cog(ava(bot)) 