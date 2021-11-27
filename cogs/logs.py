from datetime import datetime as dt

import discord
from discord.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logChannel = self.bot.get_channel(875727940095197204)
        last_msgs = await message.channel.history(limit = 1).flatten()
        if message.author.bot == False:
            embed = discord.Embed(  
                title = '🚮 Удалено сообщение',
                timestamp = dt.utcnow(),
                color = discord.Colour.dark_red(),
            ).add_field(
                name = 'Автор',
                value = message.author.mention
            ).add_field(
                name = 'Канал',
                value = message.channel.mention
            ).add_field(
                name = 'Контент',
                value = message.content if message.content else '`Нет текста`',
                inline = False
            ).add_field(
                name = 'Предшесвующее сообщение',
                value = f'[Jump!]({last_msgs[0].jump_url})' if len(last_msgs) > 0 else 'Это было первое сообщение в канале',
                inline = False
            ).set_footer(
                text = f'Author: {message.author.id} Channel: {message.channel.id}'
            )
            await logChannel.send(embed = embed)
    
    @commands.Cog.listener() 
    async def on_message_edit(self, before, after):
        logChannel = self.bot.get_channel(875727940095197204)
        if after.author.bot == False:
            if after.content != before.content:
                embed = discord.Embed(
                    title = '🖋 Изменено сообщение',
                    timestamp = dt.utcnow(),
                    color = discord.Colour.dark_gold()
                ).add_field(
                    name = 'Автор',
                    value = before.author.mention
                ).add_field(
                    name = 'Канал',
                    value = before.channel.mention
                ).add_field(
                    name = 'Оригинал',
                    value = f'[Jump!]({before.jump_url})'
                ).add_field(
                    name = 'Перед изменением',
                    value = before.content if before.content else '`Нет текста`',
                    inline = False
                ).add_field(
                    name = 'После изменения',
                    value = after.content if after.content else '`Нет текста`',
                    inline = False
                ).set_footer(
                    text = f'Message: {before.id} Author: {before.author.id} Channel: {before.channel.id}'
                )
                await logChannel.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        logChannel = self.bot.get_channel(912117419894505472)
        if before.channel == after.channel:
            return
        else:
            embed = discord.Embed(
                title = '🎤 Войс статус обновлён',
                timestamp = dt.utcnow(),
                color = discord.Colour.dark_teal()
            ).add_field(
                name = 'Участник',
                value = member.mention
            ).add_field(
                name = 'Было',
                value = before.channel.mention if before.channel else '`Присоединился к войсу`'
            ).add_field(
                name = 'Стало',
                value = after.channel.mention if after.channel else '`Вышел из войса`'
            ).set_footer(
                text = f'Member: {member.id} Before: {before.channel.id if before.channel else "None"} After: {after.channel.id if after.channel else "None"}'
            )
            await logChannel.send(embed = embed)


def setup(bot):
    bot.add_cog(Logs(bot))
