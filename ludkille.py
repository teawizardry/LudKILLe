# ludkille.py
import os
import dotenv
import discord
from discord.ext import commands
import json
from json.decoder import JSONDecodeError
from dyce import H, R
import icepool
from sw_dice import *

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

TOKEN = os.getenv('DISCORD_TOKEN')

description = '''My bot with different functions. Ludcille is a friend. Use !help_me for help and command list.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


# When bot comes online
@bot.event
async def on_ready():
    """
    Prints how many servers the bot is connected to.
    """
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print(f"LudKILLe is in " + str(guild_count) + " guilds.")


@bot.command()
async def poll(ctx, question, *emojis_and_options):
    """
    Create a poll with custom emojis and options.
    Example usage: !poll "Question" 👍 "Option 1" 👎 "Option 2"
    """
    if len(emojis_and_options) % 2 != 0:
        await ctx.send("You need to provide an equal number of emojis and options.")
        return

    emojis = emojis_and_options[::2]
    options = emojis_and_options[1::2]

    if len(options) < 2:
        await ctx.send("You need to provide at least two options for the poll.")
        return

    # Create a poll message with custom emojis and options
    poll_message = ""
    for emoji, option in zip(emojis, options):
        poll_message += f"{emoji} {option}\n\n"
        
    embed = discord.Embed(title = question, color = discord.Colour.random(), description = ''.join(poll_message))
    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar)
    embed_message = await ctx.send(embed=embed)
    embed.set_footer(text='Poll ID: {}'.format(embed_message.id))
    await embed_message.edit(embed=embed)
    
    # Add reactions to the poll message using custom emojis
    for emoji in emojis:
        await embed_message.add_reaction(emoji)

    # Write poll info to json file.  
    with open(f"poll_data.json", "r") as file:
        try:
            poll_data = json.load(file)
        except JSONDecodeError:
            poll_data = {}
        
    poll_data[embed_message.id] = {
        "options": options,
        "emojis": emojis
    }
    with open(f"poll_data.json", "w") as file:
        json.dump(poll_data, file)
        

@bot.command()
async def poll_count(ctx, poll_id):
    """
    Gets the current results of a poll from its poll id.
    Example usage: !poll_count 123456890
    """
    # Get the poll message with updated reactions
    poll_message = await ctx.channel.fetch_message(poll_id)

    with open(f"poll_data.json", "r") as file:
        poll_data = json.load(file)
        
    emojis = poll_data[poll_id]["emojis"]
    options = poll_data[poll_id]["options"]
        
    # Count the reactions for each option and find the option with the most reactions
    reaction_counts = {}
    for reaction in poll_message.reactions:
        if reaction.emoji in emojis:
            index = emojis.index(reaction.emoji)
            option = options[index]
            reaction_counts[option] = reaction.count

    # Find the option with the most reactions
    first_max_key = max(reaction_counts, key=reaction_counts.get)
    max_keys = [k for k in reaction_counts if reaction_counts[k] == reaction_counts[first_max_key]]
    
    winners = ""
    for key in max_keys:
        index = options.index(key)
        max_emoji = emojis[index]
        winners += f"{max_emoji} {key}\n\n"
    
    if len(max_keys) == 1:
        embed = discord.Embed(title = "The winner is:", color = discord.Colour.random(), description = winners)
        embed.set_footer(text='Poll ID: {}'.format(poll_id))
        _ = await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title = "There is a tie between:", color = discord.Colour.random(), description = winners)
        embed.set_footer(text='Poll ID: {}'.format(poll_id))
        _ = await ctx.send(embed=embed)
  
  
@bot.command()
async def parry(ctx):
    """
    Silly parry message.
    Example usage: !parry
    """
    val = R.from_value(H(4)).roll().total()
    
    if val == 1:
        description = "360 no scope"
    elif val == 2:
        description = "one shot, one kill"
    elif val == 3:
        description = "Deus Vult"
    else:
        description = "gg"
        
    embed = discord.Embed(title = "Parry This You Filthy Casual!", color = discord.Colour.random(), description = description, thumbnail = "https://i.imgflip.com/2/1bupu2.jpg")
    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar)
    await ctx.send(embed=embed)

@bot.command()
async def flip(ctx, option = None):
    """
    Coin flipper (1d2) with extra silly options.
    Example usage: !flip, !flip [stem, pol, simp]
    """

    roll = R.from_value(H(2)).roll().total()
    
    if option == "stem":
        if roll == 1:
            embed = discord.Embed(title = f"{ctx.message.author.display_name} decides to...", description = f"Follow **~~STEM GODS~~** 🤖", color = discord.Colour.random())
        else:
            embed = discord.Embed(title = f"{ctx.message.author.display_name} decides to...", description = f"Follow **their heart** 💖 ", color = discord.Colour.random())

    elif option == "pol":
        if roll == 1:
            embed = discord.Embed(title = f"Ben Shapiro says...", description = f"Follow :fax: **FACTS** and **LOGIC** :triumph:", color = discord.Colour.random())
            embed.set_thumbnail(url = "https://bloximages.newyork1.vip.townnews.com/omaha.com/content/tncms/assets/v3/editorial/f/43/f43a13b7-7bbd-579a-b0a3-a5097f1e5220/5a97959fd0923.image.jpg")
        else:
            embed = discord.Embed(title = f"Bernie Sanders says...", description = f"Follow your :hugging: **HEART** 💖", color = discord.Colour.random())
            embed.set_thumbnail(url = "http://dartreview.com/wp-content/uploads/2016/11/bernie.jpg")
    
    elif option == "simp":
        if roll == 1:
            embed = discord.Embed(title = f"{ctx.message.author.display_name} decides to simp!", description = f"Though {ctx.message.author.display_name} should maybe fight, they have decided to simp.", color = discord.Colour.random())
        else:
            embed = discord.Embed(title = f"{ctx.message.author.display_name} decides to fight!", description = f"Forsaking all notions of love, {ctx.message.author.display_name} has decided to fight.", color = discord.Colour.random())
    
    else:
        if roll == 1:
            embed = discord.Embed(title = f"{ctx.message.author.display_name} flips a coin!", description = f"Heads!", color = discord.Colour.random())
            embed.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/US_One_Cent_Obv.png/330px-US_One_Cent_Obv.png")
        else:
            embed = discord.Embed(title = f"{ctx.message.author.display_name} flips a coin!", description = f"Tails!", color = discord.Colour.random())
            embed.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/2005_Penny_Rev_Unc_D.png/330px-2005_Penny_Rev_Unc_D.png")
    
    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar)
    await ctx.send(embed=embed)


@bot.command()
async def fear(ctx):
    """
    Silly fear command.
    Example usage: !fear
    """
    embed = discord.Embed(title = f"{ctx.message.author.display_name} is afraid.", description=f"The recent events in this server has caused {ctx.message.author.display_name} fear and anxiety.", color = discord.Colour.random())
    embed.set_thumbnail(url = "https://media.tenor.com/images/4f8714d8962c5e124799213482d32a1c/tenor.gif")
    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar)
    await ctx.send(embed=embed)
    
# @bot.command()
# async def dice(ctx, dice_str):
#     """
#     Returns the probabilities of the given dice string.
#     Example usage: !dice 4d6kh3
#     """

@bot.command()
async def sw(ctx, dice=None):
    """
    Rolls one star wars dice.
    Example usage: !sw [ability, proficiency, boost, difficulty, challenge, setback]
    """
    allowed_dice = {"ability": ability, "proficiency": proficiency, "boost": boost, "difficulty": difficulty, "challenge": challenge, "setback": setback, "force": force}
    
    if dice in allowed_dice:
        result = sw_roll(allowed_dice[dice])
    else:
        await ctx.send("Error please pick valid dice. `!help_me sw` for more info.")
        return
       
    result_img = ''
    description = '**Result:** '
    for r in result: 
        result_img += f"{r}_"
        description += f"{r} "
    result_img += '.png'
    result_img_path = f"./imgs/{result_img}"
    roll_file = discord.File(result_img_path, filename=result_img)
    
    dice_img = f'{dice}.png'
    dice_img_path = f"./imgs/{dice_img}"
    dice_file = discord.File(dice_img_path, filename=dice_img)
    
    embed = discord.Embed(title=f"{ctx.message.author.display_name} rolled a {dice} die", description=description, color = discord.Colour.random())
    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar)
    embed.set_thumbnail(url=f"attachment://{dice_img}")
    embed.set_image(url=f"attachment://{result_img}")
    
    await ctx.send(files=[roll_file, dice_file], embed=embed)

  
#################################      
####### help commands ###########
#################################

@bot.group()
async def help_me(ctx):
    """
    Display a list of available commands.
    Example usage: !help_me
    """
    command_list = "".join([f"**!{cmd.name}:** {cmd.help} \n" for cmd in bot.commands])
    command_list += "Use `!help_me [command]` for more information on a specific command!"
    embed = discord.Embed(title = "Available Commands:", color = discord.Colour.random(), description = command_list)
    await ctx.send(embed=embed)
    
@help_me.command()
async def poll(ctx):
    """
    Get help for the !poll command.
    Example usage: !help_me poll
    """
    help_text = """\
    Create a poll with custom emojis and options.
    **Example usage: !poll "Question" 👍 "Option 1" 👎 "Option 2"**
    You need at least two options and an equal number of options and emojis.
    """
    embed = discord.Embed(title = "!poll \"Question\" 👍 \"Option 1\" 👎 \"Option 2\"", color = discord.Colour.random(), description = help_text)
    await ctx.send(embed=embed)
    
@help_me.command()
async def poll_count(ctx):
    """
    Get help for the !poll_count command.
    Example usage: !help_me poll_count
    """
    help_text = """\
    Gets the current results of a poll from its poll id.
    **Example usage: !poll_count 123456890**
    You need to provide the poll id from the footer of the poll.
    """
    embed = discord.Embed(title = "!poll_count 123456890", color = discord.Colour.random(), description = help_text)
    await ctx.send(embed=embed)

@help_me.command()
async def parry(ctx):
    """
    Get help for the !parry command.
    Example usage: !help_me parry
    """
    help_text = """\
    Silly parry message.
    **Example usage: !parry**
    """
    embed = discord.Embed(title = "!parry", color = discord.Colour.random(), description = help_text)
    await ctx.send(embed=embed)
    
@help_me.command()
async def flip(ctx):
    """
    Get help for the !flip command.
    Example usage: !help_me flip
    """
    help_text = """\
    Coin flipper (1d2) with extra silly options.
    **Example usage: !flip, !flip [stem, pol, simp]**
    """
    embed = discord.Embed(title = "!flip", color = discord.Colour.random(), description = help_text)
    await ctx.send(embed=embed)

@help_me.command()
async def fear(ctx):
    """
    Get help for the !fear command.
    Example usage: !help_me fear
    """
    help_text = """\
    Silly fear command.
    **Example usage: !fear**
    """
    embed = discord.Embed(title = "!flip", color = discord.Colour.random(), description = help_text)
    await ctx.send(embed=embed)
    
@help_me.command()
async def sw(ctx):
    """
    Get help for the !sw command.
    Example usage: !help_me sw 
    """
    help_text = """\
    Rolls one star wars dice.
    **Example usage: !sw [ability, proficiency, boost, difficulty, challenge, setback, force]**
    """
    embed = discord.Embed(title = "!sw [ability, proficiency, boost, difficulty, challenge, setback, force]", color = discord.Colour.random(), description = help_text)
    await ctx.send(embed=embed)
    
# Run Bot
bot.run(TOKEN)