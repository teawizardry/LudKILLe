from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import discord
import datetime
from discord.ext import commands, tasks
import json
from json.decoder import JSONDecodeError

utc = datetime.timezone.utc
time = datetime.time(hour=12, minute=00, tzinfo=utc)

def get_subs():
    url = "https://accessibleweeklyad.publix.com/PublixAccessibility/BrowseByListing/BySearch/?StoreID=2500312&SneakPeek=&searchtext=Publix+Deli"
    page = urlopen(url)

    html_bytes = page.read()
    soup = BeautifulSoup(html_bytes.decode("utf-8"), 'html.parser')

    subs = []

    for item in soup.body.find(id='BrowseLayout').css.select('.title'):
        if 'Sub' in str(item.h2.contents) and 'Combo' not in str(item.h2.contents):
            # print(str(item.h2.contents))
            m = re.search(r'\[\'(.*?)\'\]', str(item.h2.contents))
            subs.append(m.group(1))
            
    return(subs)

class PubSub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sub_sale.start()

    def cog_unload(self):
        self.sub_sale.cancel()

    @tasks.loop(time=time)
    async def sub_sale(self):
        if datetime.datetime.weekday() == 4:
            subs = get_subs()
            description = ''
            for sub in subs:
                description += f'<:pub_sub:1150800487596183623> {sub}\n\n'
            embed = discord.Embed(title="This Week's Pub Sub Sale:", description=description, color = discord.Colour.random()) 
            
            with open(f"./data/recurring.json", "r") as file:
                recurring = json.load(file)
                
            for channel in recurring['pub_sub']:
                c = self.bot.get_channel(recurring['pub_sub'][channel])
                await c.send(embed=embed)
        else:
            return
        
    @commands.command()
    async def pub_sub(self, ctx):
        subs = get_subs()
        description = ''
        for sub in subs:
            description += f'<:pub_sub:1150800487596183623> {sub}\n\n'
        embed = discord.Embed(title="This Week's Pub Sub Sale:", description=description, color = discord.Colour.random())
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.display_avatar)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def pub_sub_add(self, ctx):
        # get channel
        channel = {f'{ctx.message.author.id}': ctx.message.channel.id}
        
        # Write channel info to json file.  
        with open(f"./data/recurring.json", "r") as file:
            try:
                recurring = json.load(file)
            except JSONDecodeError:
                recurring = {}
        
        recurring['pub_sub'].update(channel)
        
        with open(f"./data/recurring.json", "w") as file:
            json.dump(recurring, file)
            
        await ctx.send("Channel added!")
        
async def setup(bot):
    await bot.add_cog(PubSub(bot))