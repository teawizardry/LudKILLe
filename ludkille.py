# ludkille.py
import os
import dotenv
import discord
from discord.ext import commands
import json
from json.decoder import JSONDecodeError

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

TOKEN = os.getenv('DISCORD_TOKEN')

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in bot.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name})")

        # INCREMENTS THE GUILD COUNTER.
        guild_count = guild_count + 1

    # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
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
    
# Run Bot
bot.run(TOKEN)