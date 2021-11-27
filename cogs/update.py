import discord
from discord.ext import commands
from dislash.slash_commands.slash_core import command
from config import cluster_con
from checks import is_admin

class update(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users


    @commands.command(aliases = ['update_role'])
    @is_admin()
    async def __update_role(self, ctx):
        await ctx.message.delete(delay = 3)
        emoji = "\U0001F361"
        channel = self.bot.get_channel(869621058964160583)
        e = discord.Embed(description = f"Если хотите получать уведомления об обновлении бота\n То нажмите на реакцию под сообщением 🐷 (｡◕‿◕｡)", color = discord.Colour.random())
        msg = await channel.send(embed = e)
        await msg.add_reaction(emoji = "🐷")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        channel = self.bot.get_channel(payload.channel_id)
        bot = self.bot.get_user(669930717467115561)
        if payload.user_id != bot.id:
            if payload.message_id == 875092641598029825:
                if payload.emoji.name == "🐷":
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(875069218402500658)
                    await payload.member.add_roles(role)
                else:
                    msg = await channel.fetch_message(payload.message_id)
                    await msg.clear_reaction(payload.emoji)

    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        channel = self.bot.get_channel(payload.channel_id)
        bot = self.bot.get_user(669930717467115561)
        if payload.user_id != bot.id:
            if payload.message_id == 875092641598029825:
                if payload.emoji.name == "🐷":
                    guild = self.bot.get_guild(payload.guild_id)
                    member = discord.utils.get(guild.members, id=payload.user_id)
                    role = guild.get_role(875069218402500658)
                    await member.remove_roles(role)

    @commands.command(aliases=['update','upd'])
    @is_admin()
    async def __update_msg(self,ctx, *, message):
        await ctx.message.delete()
        channel = self.bot.get_channel(869621058964160583)
        # bot = self.bot.get_user(669930717467115561)

        # e = discord.Embed(description = f"{message}")
        # e.set_author(name=bot.name,icon_url=bot.avatar_url)
        # e.set_footer(text ="Следите за обновлениями!")
        # msg = await channel.send(embed = e)

        msg = await channel.send(f"```\n{message}```")
        mention = await channel.send(f"<@&875069218402500658>")
        await mention.delete()
        await msg.add_reaction(emoji = "🐷")


    @commands.command(aliases=['editupd','updedit'])
    @is_admin()
    async def __edit_update_msg(self,ctx, msgid, *, message):
        await ctx.message.delete()
        channel = self.bot.get_channel(869621058964160583)
        msg = await channel.fetch_message(msgid)
        await msg.edit(content = f"```\n{message}```")

def setup(bot):
    bot.add_cog(update(bot)) 