import discord
from discord.ext import commands

class cmdcheck(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # await ctx.message.delete(delay=3)
        print(error)

        # if isinstance(error, commands.UserInputError):
        #     await ctx.send(f"Correct use of the command: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief}): {ctx.prefix}{ctx.command.usage}")
        # elif isinstance(error, commands.CommandNotFound):
        #     await ctx.send(embed = discord.Embed(description = f"Такой команды я не нашел... Попробуй использовать !help и найти её там"))
        # elif isinstance(error, commands.MissingPermissions):
        #     await ctx.send("You are not enough a rights")
        # elif isinstance(error, commands.MissingRequiredArgument):
        #     await ctx.send("You didn't specify the argument")

        # if isinstance(error, commands.CommandNotFound):
        #     await ctx.message.delete(delay = 3)
        #     await ctx.send(embed = discord.Embed(description = f"Такой команды я не нашел... \nПопробуй использовать `!help` и найти её там", color = discord.Colour.random(), delete_after = 5))
        # if isinstance(error, commands.MissingRequiredArgument):
        #     await ctx.send("You didn't specify the argument")

def setup(bot):
    bot.add_cog(cmdcheck(bot)) 

