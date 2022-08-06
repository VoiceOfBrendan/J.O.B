import discord
from discord.ext import commands
from discord.utils import get
from googlesearch import search
# Discord import
bot = commands.Bot(command_prefix='!')
# Create the class MyClient to act as our own discord bots class. We will inherit it from discord.Client




@bot.event
async def on_ready(ctx):
    embed = discord.Embed(
        title = 'J.O.B. - Everybody, Everywhere, Everyday needs a job!',
        description = 'Welcome to J.O.B. see the guide below for information on our bot!'
    )
    embed.set_footer(text='Please contact an Admin if you still have questions.')
    embed.set_image(url='https://ecress.weebly.com/uploads/1/3/8/7/138724180/published/image-2022-07-06-192102163.png?1657160470')
    embed.add_field(name='Job Link:', value='Change your job searching roles by using !changeJob @your server name role. EX !changeJob @J.O.B Computer Science', inline=False)
    embed.add_field(name='Job Link:', value='Have job links delivered in a matter of seconds with !displaySearch. Make sure you have set your role first!', inline=False)
    embed.add_field(name='Job Link:', value='Found a job you think would better suit a friend? !sendJob @username. EX !sendJob @J.O.B', inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used. Use !help to see valid commands.')

@bot.command()
async def info(ctx):
        #ctx - context (information about how the command was executed)
        #!info
    await ctx.send(ctx.guild)
    await ctx.send(ctx.author)
    await ctx.send(ctx.message.id)

@bot.command(pass_context=True)
async def giveRole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been giving a role called: {role.name}")

#Now lets make a function that takes in any number of arguments
@bot.command()
async def list(ctx, *args):
    # !list Justin Julia Tanner
    #line 76 is how you turn a list into a string separated with a comma
    everyone = ', '.join(args)
    await ctx.send(f'Here is your list: {everyone}')

@bot.command()
async def message(ctx, user: discord.Member = None, *, message=None):
    if user is None:
        await ctx.send("I do not know who to send this to.")
    if user is not None:
        if message is None:
            await ctx.send("I do not know what to send them.")
        if message is not None:
            myembed = discord.Embed()
            myembed.add_field(name=f"{ctx.author} sent you: ", value=f"{message}")
            myembed.set_footer(text="If you do not want to see messages like this contact the server admin.")
            await user.send(embed=myembed)

bot.links = []

@bot.command()
async def jobSearch(ctx):
    bot.numberOfResults = 10

    bot.results = search(bot.curJob, num_results=bot.numberOfResults)
    ignoreWebsites = ['indeed', 'simplyhired']
    maxNumberOfLinks = 2
    bot.links = []
    for _ in range(bot.numberOfResults):
        nextResult = next(bot.results)
        if not any(website in nextResult for website in ignoreWebsites):
            bot.links.append(nextResult)
        if len(bot.links) == maxNumberOfLinks:
            break
    embed = discord.Embed(
        title = 'Here is a job for you!',
        description = 'Here are some jobs based on your role: ' + bot.curJob
    )
    embed.set_footer(text='Please contact an Admin if you do not want to see these messages')
    embed.set_image(url='https://ecress.weebly.com/uploads/1/3/8/7/138724180/published/image-2022-07-06-192102163.png?1657160470')
    embed.set_author(name=f"{ctx.author} is the author to this message")
    embed.add_field(name='Job Link:', value=bot.links[0], inline=False)
    embed.add_field(name='Job Link:', value=bot.links[1], inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def changeJob(ctx, user : discord.Member, * ,arg):
    CS = discord.utils.get(ctx.guild.roles, name="Computer Science")
    GD = discord.utils.get(ctx.guild.roles, name="Game Design")
    WD = discord.utils.get(ctx.guild.roles, name="Web Design")

    
    for i in user.roles:
        try:
            await user.remove_roles(i)
        except:
            print(f"Can't remove the role {i}")

    if arg == 'Game Design':
        await user.add_roles(GD)
        await ctx.send("User role has been updated.")
        bot.curJob = "Game Design Jobs"
    if arg == 'Web Design':
        await user.add_roles(WD)
        await ctx.send("User role has been updated.")
        bot.curJob = "Web Design Jobs"
    if arg == 'Computer Science':
        await user.add_roles(CS)
        await ctx.send("User role has been updated.")
        bot.curJob = "Computer Science Jobs"

@bot.command()
async def sendJob(ctx, user: discord.Member = None):
    embed = discord.Embed(
        title = 'Here is a job for you!',
        description = 'Someone sent you a job opportunity from the J.O.B discord bot!'
    )
    embed.set_footer(text='Please contact an Admin if you do not want to see these messages')
    embed.set_image(url='https://ecress.weebly.com/uploads/1/3/8/7/138724180/published/image-2022-07-06-192102163.png?1657160470')
    embed.set_author(name=f"{ctx.author} is the author to this message")
    embed.add_field(name='Job Link:', value=bot.links[0], inline=False)
    embed.add_field(name='Job Link:', value=bot.links[1], inline=False)

    await user.send(embed=embed)

    


intents = discord.Intents.default()
intents.members = True
# Make sure you put your own Token inside
bot.run('')