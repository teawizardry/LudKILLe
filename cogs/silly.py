import discord
from discord.ext import commands
from dyce import H, R

class Silly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def parry(self, ctx):
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

    @commands.command()
    async def flip(self, ctx, option = None):
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


    @commands.command()
    async def fear(self, ctx):
        """
        Silly fear command.
        Example usage: !fear
        """
        embed = discord.Embed(title = f"{ctx.message.author.display_name} is afraid.", description=f"The recent events in this server has caused {ctx.message.author.display_name} fear and anxiety.", color = discord.Colour.random())
        embed.set_thumbnail(url = "https://media.tenor.com/images/4f8714d8962c5e124799213482d32a1c/tenor.gif")
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar)
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Silly(bot))