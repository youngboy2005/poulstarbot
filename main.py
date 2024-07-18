import discord
from dispie import EmbedCreator
from discord.ext import commands
import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$",intents=intents)
token = ""

@bot.event
async def on_ready():
    activity = discord.Game(name=f"poulstar.org", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("bot ready")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command")
    except Exception as e:
        print(e)

@bot.tree.command(name="help", description="help command")
async def help_1(interaction : discord.Interaction):
    mbed = discord.Embed(title="list of bot commands", description="bot command", color=discord.Color.yellow())
    mbed.add_field(name="/ping", value="show bot ping", inline=False)
    mbed.add_field(name="/avatar", value="show members avatar", inline=False)
    mbed.add_field(name="/userinfo", value="show a member information", inline=False)
    mbed.add_field(name="/serverinfo", value="show server information", inline=False)
    mbed.add_field(name="/kick", value="kick a member", inline=False)
    mbed.add_field(name="/ban", value="ban a member", inline=False)
    mbed.add_field(name="/timeout", value="timeout a member", inline=False)
    mbed.add_field(name="/embed-gen", value="generate and send an embed message", inline=False)
    await interaction.response.send_message(embed=mbed)

@bot.tree.command(name="ping", description="bot ping")
async def ping(interaction : discord.Interaction):
    await interaction.response.send_message(f"bot ping is {round(bot.latency* 1000)}ms")

@bot.tree.command(name="avatar", description="a member avatar")
async def avatar(interaction : discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f'{member.global_name}\'s Avatar', color=0x00ff00)
    embed.set_image(url=member.avatar)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo",description="show information about a member")
async def userinfo(interaction: discord.Interaction, member: discord.Member):
    roles = [role.name for role in member.roles]
    toprole = member.top_role.name
    embed = discord.Embed(title="userinfo", description=f"{member.mention} user info", color= discord.Color.random())
    embed.add_field(name="NICKNAME", value=member.display_name)
    embed.add_field(name="NAME", value=member.name)
    embed.add_field(name="ID", value=f"user id {member.id}")
    embed.add_field(name="STATUS", value=str(interaction.user.status))
    embed.add_field(name="ROLE" , value=", ".join(roles))
    embed.add_field(name="TOP ROLE", value=toprole)
    embed.add_field(name="JOIN", value=member.joined_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    embed.add_field(name="Created At", value=member.created_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    embed.add_field(name="bot?", value=member.bot)
    embed.set_footer(text=f"requested by {interaction.user}")
    embed.timestamp = interaction.created_at
    embed.set_thumbnail(url=member.avatar)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="server",description='about this server')
async def serverinfo(interaction: discord.Interaction):
    server = interaction.guild
    embed = discord.Embed(title="serverinfo", description=f"{server.name} info", color= discord.Color.random())
    embed.add_field(name="NAME", value=server.name)
    embed.add_field(name="ID", value=f"{server.id}")
    embed.add_field(name="OWNER", value=f"{server.owner}")
    embed.add_field(name="Created At", value=server.created_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    embed.set_footer(text=f"requested by {interaction.user}")
    embed.set_thumbnail(url=server.icon)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='kick',description="kick a member")
@commands.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.kick(reason=reason)
    await interaction.response.send_message(f'Kicked {member.mention}.')

@bot.tree.command(name='ban',description="ban a member")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.ban(reason=reason)
    await interaction.response.send_message(f'Banned {member.mention}.')

@bot.tree.command(name='timeout',description="timeout a member")
@commands.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = None):
    await member.timeout(duration=duration, reason=reason)
    await interaction.response.send_message(f'Timed out {member.mention} for {duration} seconds.')

@bot.tree.command(name='say',description="say a message as bot")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

@bot.tree.command(name="embed-gen",description="create an embed")
@commands.has_permissions(administrator=True)
async def embed_creator(interaction : discord.Interaction):
    view = EmbedCreator(bot=bot)
    await interaction.response.send_message(embed=view.get_default_embed, view=view)

@bot.event
async def on_message_delete(message):
    embed = discord.Embed(title="{} deleted a message".format(message.author.name),description="", color=0xFF0000)
    embed.add_field(name=message.content, value="This is the message that he has deleted",inline=True)
    channel = bot.get_channel(1263416651647422507)
    await channel.send(channel, embed=embed)

@bot.event
async def on_message_edit(message_before, message_after):
    embed = discord.Embed(title="{} edited a message".format(message_before.author.name),description="", color=0xFF0000)
    embed.add_field(name=message_before.content, value="This is the message before any edit",inline=True)
    embed.add_field(name=message_after.content, value="This is the message after the edit",inline=True)
    channel = bot.get_channel(1263416651647422507)
    await channel.send(channel, embed=embed)

@bot.event
async def on_member_join(member:discord.Member):
    channel = discord.utils.get(member.guild.channels, id=1263416651647422507)
    if channel is not None:
        await channel.send(f'Welcome {member.mention} to the server!')

bot.run(token)