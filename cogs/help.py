import discord
from discord.ext import commands

class HelpMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    async def help_me(self, ctx):
        """
        Display a list of available commands.
        Example usage: !help_me
        """
        command_list = "".join([f"**!{cmd.name}:** {cmd.help} \n" for cmd in self.bot.commands])
        command_list += "Use `!help_me [command]` for more information on a specific command!"
        embed = discord.Embed(title = "Available Commands:", color = discord.Colour.random(), description = command_list)
        await ctx.send(embed=embed)
        
    @help_me.command()
    async def poll(self, ctx):
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
    async def poll_count(self, ctx):
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
    async def parry(self, ctx):
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
    async def flip(self, ctx):
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
    async def fear(self, ctx):
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
    async def sw(self, ctx):
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
              
async def setup(bot):
    await bot.add_cog(HelpMe(bot))