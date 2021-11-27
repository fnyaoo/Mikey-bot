import discord
from datetime import datetime
from discord.ext import commands, tasks
from config import cluster_con

class VoiceLeaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = cluster_con()
        self.collusers = self.cluster.server.users
        self.collvoice = self.cluster.server.voicecounter
        self.__voicecount.start()

    async def __connect(self, member):
        if self.collvoice.count_documents({"guild_id":member.guild.id,"user_id":member.id}) == 0:
            connectTime = datetime.now()
            values = {
                "guild_id":member.guild.id,
                "user_id":member.id,
                "connectTime": connectTime,
                "disconnectTime": connectTime
            }
            self.collvoice.insert_one(values)
            
        else:
            connectTime = datetime.now()
            self.collvoice.update_one({"guild_id":member.guild.id,"user_id":member.id},{"$set":{"connectTime":connectTime}})
            print(f"{member} connect:", connectTime)

    async def __disconnect(self, member):
        disconnectTime = datetime.now()
        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        self.collvoice.update_one({"guild_id":member.guild.id,"user_id":member.id},{"$set":{"disconnectTime":disconnectTime}})
        connectTime = self.collvoice.find_one({"guild_id":member.guild.id,"user_id":member.id})["connectTime"]
        time_diff = datetime.strptime(str(disconnectTime), datetimeFormat) - datetime.strptime(str(connectTime), datetimeFormat)
        self.collusers.update_one({"guild_id":member.guild.id,"user_id":member.id},{"$inc":{"voicetime":time_diff.seconds}})
        print(f"{member} disconnect:", disconnectTime)

    async def __voiceaward(self):
        for guild in self.bot.guilds:
            for channel in guild.voice_channels:
                for member in channel.members:
                    voicetime = self.collusers.find_one({"user_id":member.id, "guild_id":member.guild.id})["voicetime"]
                    if voicetime != 0:
                        hours = int(voicetime/10*10/60/60)
                        minutes = int((voicetime - (hours*60*60))/60)
                        if minutes % 3 == 0:
                            self.collusers.update_one({"guild_id":member.guild.id,"user_id":member.id},{"$inc":{"money":1}})
                        
    @tasks.loop(minutes=1)
    async def __voicecount(self):
        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        for guild in self.bot.guilds:
            for member in guild.members:
                if self.collvoice.count_documents({"guild_id":member.guild.id,"user_id":member.id}) == 0:
                    connectTime = datetime.now()
                    values = {
                        "guild_id":member.guild.id,
                        "user_id":member.id,
                        "connectTime": connectTime,
                        "disconnectTime": connectTime
                    }
                    self.collvoice.insert_one(values)
                    self.collusers.update_one({"guild_id":member.guild.id,"user_id":member.id},{"$set":{"voicetime":0}})
                    
                if member.voice is not None:
                    if member.voice.afk == False:
                        checkTime = datetime.now()
                        connectTime = self.collvoice.find_one({"guild_id":member.guild.id,"user_id":member.id})["connectTime"]

                        time_diff = datetime.strptime(str(checkTime), datetimeFormat) - datetime.strptime(str(connectTime), datetimeFormat)
                    
                        self.collvoice.update_one({"guild_id":member.guild.id,"user_id":member.id},{"$set":{"connectTime":checkTime}})
                        self.collusers.update_one({"guild_id":member.guild.id,"user_id":member.id},{"$inc":{"voicetime":time_diff.seconds}})  

              

        await self.__voiceaward()

    @__voicecount.before_loop
    async def before_voicecount(self):
        print('voice waiting...')
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
   
        if before.channel is None or before.afk == True:
            await self.__connect(member)

        elif after.channel == None or after.afk == True:
            await self.__disconnect(member)

def setup(bot):
    bot.add_cog(VoiceLeaderboard(bot))