import json
import discord
import time
import discord
from discord.ext import commands

class VoiceLeaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        '''
        Maintain vc leaderboard data
        '''
        if member.bot: # not bot
            return
        new_user = str(member.id)
        guild_id = str(member.guild.id)
        new_guild = guild_id
        
        with open('./data/vc_rank.json', 'r') as file: 
            voice_data = json.load(file)
        
        try:
            if new_user not in voice_data[guild_id]: # add a new user to the guild dict if they're not in it yet
                voice_data[guild_id][new_user] = {
                    "total_time" : 0,
                    "join_time" : None} 
            userdata = voice_data[guild_id][new_user]
        except:
            voice_data.update({guild_id: {}})
            if new_user not in voice_data[guild_id]: # add a new user to the guild dict if they're not in it yet
                voice_data[guild_id][new_user] = {
                    "total_time" : 0,
                    "join_time" : None} 
            userdata = voice_data[guild_id][new_user]

        # check if user is joining or leaving a vc
        if(before.channel == None) or (str(before.channel.guild.id) != guild_id): # join a vc or switch guilds
            userdata["join_time"] = round(time.time())
        elif(after.channel != None): # changed vc within the same guild, mute/deafen events 
            if before.channel.guild.id == after.channel.guild.id:
                return
            else:
                new_guild = after.channel.guild.id
        elif(after.channel == None) or (str(new_guild) != guild_id): # left vc or switched guilds
            if(userdata["join_time"] == None): # error catching
                print('join_time none error')
                return
            userdata["total_time"] += round(time.time()) - userdata["join_time"]
            userdata["join_time"] = None # preventive measure against errors
            
        with open('data/vc_rank.json', 'w') as update_user_data:
            json.dump(voice_data, update_user_data, indent=4)

    @commands.command()
    async def vc(self, ctx):
        ''''
        Print current guild's vc leaderboard data
        '''
        with open('./data/vc_rank.json', 'r') as file:
            voice_data = json.load(file)

        guild_id = str(ctx.message.guild.id)
        
        try:
            userdata = voice_data[guild_id]
        except:
            await ctx.send("Not enough data for VC Leaderboard! Try talking to more friends...")

        # Sort leaderboard
        leaderboard = sorted(userdata.items(), key=lambda x:x[1], reverse=True)
        
        embed = discord.Embed(title=f"{ctx.message.guild.name} VC Leaderboard", color = discord.Colour.random(), description=f"Congrats {self.bot.get_user(int(leaderboard[0][0])).name}!")
        embed.set_thumbnail(url=self.bot.get_user(int(leaderboard[0][0])).avatar)
        for user in leaderboard:
            embed.add_field(name=f"{self.bot.get_user(int(user[0])).name}", value=f"{user[1]['total_time']//60} Minutes", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(VoiceLeaderboard(bot))
    