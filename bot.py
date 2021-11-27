import discord
from discord.ext import commands
from config import settings, cluster_con
from dislash import *
import os
from discord import *
from checks import is_admin

cluster = cluster_con()
collusers = cluster.server.users
collservers = cluster.server.guilds


intents = discord.Intents.all()
bot = commands.Bot(command_prefix = settings['PREFIX'], intents=intents, case_insensitive=True, strip_after_prefix=True)


bot.remove_command('help')


@bot.command() 
@is_admin()
async def load(ctx, extensions): 
    await ctx.message.delete()
    bot.load_extension(f'cogs.{extensions}')
    e = discord.Embed(description = f"Дополнение {extensions} было включено", color = discord.Colour.blurple())
    await ctx.send(embed = e, delete_after = 1)
    

@bot.command()
@is_admin()
async def unload(ctx, extensions):
    await ctx.message.delete()
    bot.unload_extension(f'cogs.{extensions}')
    e = discord.Embed(description = f"Дополнение {extensions} было отключено", color = discord.Colour.blurple())
    await ctx.send(embed = e, delete_after = 1)
    

@bot.command()
@is_admin()
async def reload(ctx, extensions):
    await ctx.message.delete()
    bot.unload_extension(f'cogs.{extensions}')
    bot.load_extension(f'cogs.{extensions}')
    e = discord.Embed(description = f"Дополнение {extensions} было перезагружено", color = discord.Colour.blurple())
    await ctx.send(embed = e, delete_after = 1)
    
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel

    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    e = discord.Embed(description = f'Pong! `{(round(bot.latency, 3))}`', color = discord.Color.random())
    e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed = e)

@bot.event
async def on_message(message):

    if message.content.lower().startswith('!'):
        cmdChannel = bot.get_channel(869603902906056765)
        msgChannel = message.channel

        if msgChannel.category_id == 875013697410576435:
            if msgChannel == cmdChannel:
                await bot.process_commands(message)
            else:
                await message.delete(delay = 1)
                e = discord.Embed(description = f'Используйте команды в специальном чате - {cmdChannel.mention}', color = discord.Colour.gold())
                e.set_author(name = message.author, icon_url = message.author.avatar_url)
                await message.channel.send(embed = e, delete_after = 5)
        else:
            await bot.process_commands(message)

@bot.event
async def on_message_edit(before,after):
    if before.content.lower().startswith('!'):
        await bot.process_commands(after)

@bot.event
async def on_member_join(member):
    values = {
        "guild_id": member.guild.id,
        "user_id": member.id,
        "money": 0,
        "steamid": 0,
        "quote": "",
        "online": 0,
        "lottery": 0,
        "bombattemp": 0,
        "wins": 0,
        "voicetime":0,
        "zxcskin":"",
        "zxcstat":{
            "win":0,
            "lose":0
        }
    }
    if collusers.count_documents({"user_id": member.id, "guild_id": member.guild.id}) == 0:
        collusers.insert_one(values)
        print('add new user')
    else:
        print('user already exists')

    role = member.guild.get_role(669686348743049243)
    await member.add_roles(role)
    channel = bot.get_channel(218043625265823744)
    e = discord.Embed(description = f"Добро пожаловать на **{member.guild.name}** <:luv_love:841087104871563294>", color = discord.Colour.random())
    e.set_image(url = "https://c.tenor.com/zXfxt7qdC5QAAAAC/gojo-satoru-jujutsu-kaisen.gif")
    await channel.send(f"**{member.mention}**", embed = e)
    
@bot.event
async def on_guild_join(guild):
    server_values ={
        "guild_id": guild.id
    }
    if collservers.count_documents({"guild_id": guild.id}) == 0:
            collservers.insert_one(server_values)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help"))

    # guild = bot.get_guild(218043625265823744)
    for guild in bot.guilds:
        for member in guild.members:
            
            values = {
                "guild_id": guild.id,
                "user_id": member.id,
                "money": 0,
                "steamid": 0,
                "quote": "",
                "online": 0,
                "lottery": 0,
                "bombattemp": 0,
                "wins": 0,
                "voicetime":0,
                "zxcskin":"",
                "zxcstat":{
                    "win":0,
                    "lose":0
                }
            }
            
            server_values ={
                "guild_id": guild.id
            }


            if collusers.count_documents({"user_id": member.id, "guild_id": guild.id}) == 0:
                collusers.insert_one(values)

            if collservers.count_documents({"guild_id": guild.id}) == 0:
                collservers.insert_one(server_values)
    print('------------------------------------')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------------------------------------')

    channel = bot.get_channel(732367665221599293)
    await channel.send("Start session...")

    for guild in bot.guilds:

            try:
                privatecategory = collservers.find_one({"guild_id":guild.id})["private_ctg"]
                privatemaker = collservers.find_one({"guild_id":guild.id})["private_ch"]
                mainCategory = discord.utils.get(guild.categories, id=privatecategory)

                for channel in mainCategory.channels:
                    if channel.id == privatemaker:
                        pass
                    else:
                        count = 0
                        for members in channel.members:
                            count+=1
                        if count == 0:
                            await channel.delete()
            except KeyError:
                pass
#cogs load
for filename in os.listdir('./cogs/'): 
    if filename.endswith('.py'): 
        bot.load_extension(f'cogs.{filename[:-3]}') 
        print(f"loaded {filename}")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
bot.run(settings['TOKEN'])