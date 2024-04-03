import discord
from discord.ext import commands
import asyncio
import random

# Define intents
intents = discord.Intents.all()
intents.presences = True
intents.members = True

# Set up the bot with intents and new prefix
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)  # Disable default help command

# Role IDs
ROLE_MANAGEMENT_ROLE_ID = 1224735755625300100
OWNER_ROLE_ID = 1224409214047355102
N_WORD_PASS_ROLE_ID = 1224732438513586226
WARN_PERMISSION_ROLE_ID = 1224783642308640800

# Warn role IDs
WARN_1_ROLE_ID = 1224782609922523189
WARN_2_ROLE_ID = 1224782694055940098
WARN_3_ROLE_ID = 1224782742735028285

# Log channel ID
LOG_CHANNEL_ID = 1224640758863102104

log_channel_id = LOG_CHANNEL_ID
warn_permission_id = WARN_PERMISSION_ROLE_ID
owners_id = OWNER_ROLE_ID
warn_1_id = WARN_1_ROLE_ID
warn_2_id = WARN_2_ROLE_ID
warn_3_id = WARN_3_ROLE_ID

# List of banned words
banned_words = [
    "fuck", "motherfucker", "asshole", "shit", "bitch",
    "bastard", "dick", "cunt", "whore", "cock",
    "pussy", "twat", "fag", "nigger", "spic",
    "slut", "wanker", "faggot", "ass", "douchebag",
    "arsehole", "prick", "cum", "bastard", "cuck",
    "damn", "crap", "bollocks", "blowjob", "jerk",
    "nigga", "cuntbag", "dickhead", "arse", "tit",
    "piss", "dildo", "bitchass", "fuckwit", "whorebag",
    "dipshit", "fucked", "cocksucker", "wank", "shite",
    "goddamn", "pissed", "asswipe", "turd", "arsewipe"
]

# Dictionary to track banned word counts for each user
banned_word_counts = {}

# Function to check if a member has a specific role
def has_role(member, role_id):
    return discord.utils.get(member.roles, id=role_id) is not None

# Function to check if a member has the N word pass role or is the owner
def has_permission(ctx):
    return has_role(ctx.author, N_WORD_PASS_ROLE_ID) or ctx.author.id == OWNER_ROLE_ID or has_role(ctx.author, ROLE_MANAGEMENT_ROLE_ID)

# Event for when the bot is ready
@bot.event
async def on_ready():
    print('Darkari is online')
    await bot.change_presence(activity=discord.Game(name="I AM BACK 🔥"))
    await asyncio.sleep(3600)  # Wait for 1 hour
    await bot.change_presence(activity=discord.Game(name="hosted by amarnath"))
    await asyncio.sleep(3600)  # Wait for 1 hour
    await bot.change_presence(activity=discord.Game(name="owners: lord devil and Google"))

# Ping command
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Calculate latency in milliseconds
    embed = discord.Embed(title="Pong!", description=f'Latency is {latency}ms', color=random.randint(0, 0xFFFFFF))
    await ctx.send(embed=embed)

# Command to add a banned word
@bot.command()
@commands.check(has_permission)  # Check if user has permission
async def add_banned_word(ctx, word: str):
    if word.lower() not in banned_words:
        banned_words.append(word.lower())
        embed = discord.Embed(title="Banned Word Added", description=f"The word `{word}` has been added to the list of banned words.", color=random.randint(0, 0xFFFFFF))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Word Already Banned", description=f"The word `{word}` is already in the list of banned words.", color=random.randint(0, 0xFFFFFF))
        await ctx.send(embed=embed)

# Command to remove a banned word
@bot.command()
@commands.check(has_permission)  # Check if user has permission
async def remove_banned_word(ctx, word: str):
    if word.lower() in banned_words:
        banned_words.remove(word.lower())
        embed = discord.Embed(title="Banned Word Removed", description=f"The word `{word}` has been removed from the list of banned words.", color=random.randint(0, 0xFFFFFF))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Word Not Found", description=f"The word `{word}` is not in the list of banned words.", color=random.randint(0, 0xFFFFFF))
        await ctx.send(embed=embed)


@bot.command()
async def role(ctx, member: discord.Member, *, role_info):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    guild = ctx.guild

    if not role_info:
        # If role info is not provided, send an error message
        embed = discord.Embed(
            title="Error",
            description="You need to mention a role.",
            color=random.randint(0, 0xFFFFFF)
        )
        embed.set_footer(text="Take some training bro")
        await ctx.send(embed=embed)
        return

    role = discord.utils.find(lambda r: r.name == role_info or str(r.id) == role_info or role_info in [f"<@&{r.id}>" for r in ctx.guild.roles], guild.roles)
    if role:
        if has_role(ctx.author, ROLE_MANAGEMENT_ROLE_ID) or ctx.author.id == OWNER_ROLE_ID:
            if role in member.roles:
                await member.remove_roles(role)
                action = "removed"
            else:
                await member.add_roles(role)
                action = "added"
            embed_log = discord.Embed(
                title="Roles Updated",
                description=f"{ctx.author.mention} {action} role {role.mention} to {member.mention}",
                color=random.randint(0, 0xFFFFFF)
            )
            embed_log.add_field(name="Person Who Got Role", value=member.mention)
            embed_log.add_field(name="Role", value=role.mention)
            embed_log.add_field(name="Channel", value=ctx.channel.mention)
            embed_log.add_field(name="Time", value=ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            await log_channel.send(embed=embed_log)
            success_embed = discord.Embed(
                title="Successfully Completed",
                description=f"Successfully {action} role {role.mention} to {member.mention}.",
                color=random.randint(0, 0xFFFFFF)
            )
            await ctx.send(embed=success_embed)
        else:
            await ctx.send("You do not have permission to use this command.")
    else:
        await ctx.send("Role not found.")
      


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        embed = discord.Embed(
            title="Beep! Boop!",
            description="Use command `!help_menu`",
            color=random.randint(0, 0xFFFFFF)
        )
        await message.channel.send(embed=embed)
    
    await bot.process_commands(message)
  





@bot.command()
async def warn(ctx, member: discord.Member, *, reason: str):
    log_channel = bot.get_channel(log_channel_id)
    
    # Check if the user has the permission or is an owner
    if has_role(ctx.author, warn_permission_id) or ctx.author.id == owners_id:
        if not member:
            # If no user is mentioned, send an error embed
            embed = discord.Embed(
                title="Error",
                description="Bro mention someone, are you trying to take fun of me or what?",
                color=random.randint(0, 0xFFFFFF)
            )
            embed.set_footer(text="Take some training bro")
            await ctx.send(embed=embed)
            return
        
        if not reason:
            # If no reason is mentioned, send an error embed
            embed = discord.Embed(
                title="Error occurred while processing",
                description="You need to mention a reason.",
                color=random.randint(0, 0xFFFFFF)
            )
            embed.set_footer(text="Take some training bro...")
            await ctx.send(embed=embed)
            return
        
        # Warn the member
        guild = ctx.guild
        warn_role_1 = guild.get_role(warn_1_id)
        warn_role_2 = guild.get_role(warn_2_id)
        warn_role_3 = guild.get_role(warn_3_id)
        
        await member.add_roles(warn_role_1)
        
        # Log the warning
        log_message = f"{ctx.author.name} has warned {member.name} reason: {reason}"
        await log_channel.send(log_message)
        
        # Update user's roles based on warn level
        if warn_role_2 in member.roles:
            await member.add_roles(warn_role_3)
            await member.remove_roles(warn_role_2)
        elif warn_role_1 in member.roles:
            await member.add_roles(warn_role_2)
            await member.remove_roles(warn_role_1)
        
        # Send success embed in the channel
        embed = discord.Embed(
            title="Successfully Warned Member",
            description=f"Warned {member.mention} Reason: {reason}",
            color=random.randint(0, 0xFFFFFF)
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("You do not have permission to use this command.")
        










# Command to display help menu
# Command to display help menu
@bot.command()
async def help_menu(ctx):
    embed = discord.Embed(title="Help Menu", color=random.randint(0, 0xFFFFFF))
    embed.add_field(name="!ping", value="Check bot's latency", inline=False)
    embed.add_field(name="!add_banned_word <word>", value="Add a word to the list of banned words", inline=False)
    embed.add_field(name="!remove_banned_word <word>", value="Remove a word from the list of banned words", inline=False)
    embed.add_field(name="!role <role name or ID>", value="Add or remove a role", inline=False)
    embed.add_field(name="!warn <member> <reason>", value="Warn a member with a reason", inline=False)
    await ctx.send(embed=embed)
  

# Run the bot
TOKEN = 'MTIyNDY1MDUxMDQ0NDAwNzUyNQ.GGbUE2.1i4GE8pEPJEumQUMPEMnHA_O1IobY3TRTUPWIs'  # Your bot token
bot.run(TOKEN)
