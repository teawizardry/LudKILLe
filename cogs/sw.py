import discord
from discord.ext import commands
import numpy as np

# Values
SUCCESS = "Success"
FAILURE = "Failure"
ADVANTAGE = "Advantage"
THREAT = "Threat"
TRIUMP = "Triump"
DESPAIR = "Despair"
BLANK = "Blank"
DARK = "Dark"
LIGHT = "Light"

# Ability
ability =  [[SUCCESS, ADVANTAGE], [ADVANTAGE, SUCCESS], [SUCCESS, SUCCESS], [ADVANTAGE], [SUCCESS], [ADVANTAGE, ADVANTAGE], [BLANK]]

# Proficiency
proficiency = [[ADVANTAGE, ADVANTAGE], [ADVANTAGE], [ADVANTAGE, ADVANTAGE], [TRIUMP], [SUCCESS], [SUCCESS, ADVANTAGE], [SUCCESS], [SUCCESS, ADVANTAGE], [SUCCESS, SUCCESS], [SUCCESS, ADVANTAGE], [SUCCESS, SUCCESS], [BLANK]]

# Boost
boost = [[ADVANTAGE], [SUCCESS, ADVANTAGE], [ADVANTAGE, ADVANTAGE], [SUCCESS], [BLANK], [BLANK]]

# Difficulty
difficulty = [[THREAT], [FAILURE], [THREAT, FAILURE], [THREAT], [BLANK], [THREAT, THREAT], [FAILURE, FAILURE], [THREAT]]

# Challenge
challenge = [[THREAT, THREAT], [THREAT], [THREAT, THREAT], [THREAT], [THREAT, FAILURE], [FAILURE], [THREAT, FAILURE], [FAILURE], [FAILURE, FAILURE], [DESPAIR], [FAILURE, FAILURE], [BLANK]]

# Setback
setback = [[FAILURE], [FAILURE], [THREAT], [THREAT], [BLANK], [BLANK]]

# Force
force = [[DARK], [DARK], [DARK], [DARK], [DARK], [DARK], [DARK, DARK], [LIGHT], [LIGHT], [LIGHT, LIGHT], [LIGHT, LIGHT], [LIGHT, LIGHT]]

rng = np.random.default_rng()

def sw_roll(dice):
    roll = rng.integers(len(dice))
    return dice[roll]

class StarWars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def sw(self, ctx, dice=None):
        """
        Rolls one star wars dice.
        Example usage: !sw [ability, proficiency, boost, difficulty, challenge, setback]
        """
        allowed_dice = {"ability": ability, "proficiency": proficiency, "boost": boost, "difficulty": difficulty, "challenge": challenge, "setback": setback, "force": force}
        dice_emojis = {"Advantage": "<:advantage:1150616126850596864>", "Blank": "<:blank:1150616129925034027>", "Dark": "<:dark:1150616134173859851>", "Despair": "<:despair:1150616453838544978>", "Failure": "<:failure:1150616458196426883>", "Light": "<:light:1150616461056950314>", "Success": "<:success:1150616144613494787>", "Threat": "<:threat:1150616464148144128>", "Triumph": "<:triumph:1150616465653891173>"}
        
        if dice in allowed_dice:
            result = sw_roll(allowed_dice[dice])
        else:
            await ctx.send("Error please pick valid dice. `!help_me sw` for more info.")
            return
        
        description = '**Result: **'
        embed = discord.Embed(title=f"{ctx.message.author.display_name} rolled a {dice} die", description=description, color = discord.Colour.random())
        
        for r in result: 
            embed.add_field(name=f"{r}", value=f"{dice_emojis[r]}", inline=True)
        
        dice_img = f'{dice}.png'
        dice_img_path = f"./imgs/{dice_img}"
        dice_file = discord.File(dice_img_path, filename=dice_img)
        
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.display_avatar)
        embed.set_thumbnail(url=f"attachment://{dice_img}")
        
        await ctx.send(file=dice_file, embed=embed)
    
async def setup(bot):
    await bot.add_cog(StarWars(bot))