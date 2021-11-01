import discord
from discord.ext import commands
import random
from colorama import Fore, Back, Style
import asyncio
from discord import Permissions
import datetime
import aiohttp
import requests
import io
import json
from discord.voice_client import VoiceClient
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

queue = []

token = "plot"

prefix = "$"

solar = commands.Bot(command_prefix = prefix, self_bot=False)

solar.antiban = False
solar.antibot = False
solar.antikick = False
solar.whitelisted_users = {}
solar.remove_command('help')

@solar.event
async def on_ready():
  print(f"{Style.BRIGHT}{Fore.RED}{solar.user.name} IS ONLINE! {Style.RESET_ALL}")
  await status_task()

@solar.event
async def on_command_error(ctx, cmd):
  embed=discord.Embed(description=f"`{cmd}`,** do {prefix}help for list of cmds.**", color=random.randint(0, 0xFFFFFF))
  await ctx.send(embed=embed)

async def status_task():
    while True:
        await solar.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.streaming, 
                url='https://twitch.tv/chrizhub',
                name="Verison 0.1"))
        await asyncio.sleep(10)
        await solar.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.streaming,
                url='https://twitch.tv/chrizhub',
                name=f"{prefix}help | {prefix}invite"
            ))
        await asyncio.sleep(10)
        await solar.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(solar.guilds)} Servers!"))
        await asyncio.sleep(10)
        await solar.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.streaming,
                url='https://twitch.tv/chrizhub',
                name="Protecting Servers"))
        await asyncio.sleep(10)
   
   


#########################################
#                                       #
#            HELP COMMANDS              #
#                                       #
#########################################

@solar.command(pass_contex=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def help(ctx):
  embed=discord.Embed(title=f"`Usage : {prefix}[module]`", timestamp=ctx.message.created_at, color=discord.Colour.from_rgb(113, 114, 255))

  embed.set_author(name="Solr Anti-Nuke",icon_url=ctx.author.avatar_url)

  embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/791083872221134848/791111000975867945/solrsupportlogo.gif")

  embed.add_field(name="<a:no_pedestrians:790447734632480768> | AntiNuke", value="`Shows Anti Nuke Commands.`", inline=False)
  embed.add_field(name="<a:moderation:790445644736757800> | Moderation", value="`Shows Moderation Commands.`", inline=False)
  embed.add_field(name="<a:fun:790444383694356520> | Fun", value="`Shows Fun Commands.`", inline=False)
  embed.add_field(name="<a:Music:790445137435820042> | Music", value="`Shows Music Commands.`", inline=False)
  embed.add_field(name="<:r_util:790444533858828329> | Settings", value="`Shows Setting Commands.`", inline=False)
  embed.add_field(name="<:DiscordStaff:790446403796467742> | Utility", value="`Shows Utility Commands.`", inline=False)
  embed.set_image(url = "https://cdn.discordapp.com/attachments/778069879223222273/790380030550212628/standard_3.gif")
  embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)


##dmall
@solar.command()
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def dmall(ctx, *, args=None):
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
                print("sent " + args + " to " + member.name)

            except:
                print("didnt send " + args + " to " + member.name)

        
#########################################
#                                       #
#           AntiNuke Commands           #
#                                       #
#########################################                
              
##antinuke

@solar.command(aliases=['antinuke' , 'anti'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Antinuke(ctx):
 embed = discord.Embed(color=0xf1c40f, timestamp=ctx.message.created_at)

 embed.set_author(name="Anti Nuke",icon_url=ctx.author.avatar_url)

 embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/791083872221134848/791111000975867945/solrsupportlogo.gif")

 embed.add_field(name="Lock", value="locks the channel.", inline=False)
 embed.add_field(name="Unlock", value="Unlocks the channel.", inline=False)
 embed.add_field(name="Lockall", value="locks all the channel.", inline=False)
 embed.add_field(name="Unlockall", value="Unlocks all the channel.", inline=False)
 embed.add_field(name="Whitelist", value="Whitelists User.", inline=False)
 embed.add_field(name="Unwhitelist", value="Unwhitelists User..", inline=False)
 embed.add_field(name="Clearwhitelist", value="Removes all users in the whitelist.", inline=False)
 embed.add_field(name="AntiBan", value="Enables/Disables Anti Ban.", inline=False)
 embed.add_field(name="Antikick", value="Enables/Disables Anti Kick.", inline=False)
 embed.add_field(name="Antibot", value="Enables/Disables Anti Bot.", inline=False)

 embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
 await ctx.send(embed=embed)

@solar.command(aliases=['Lockall'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(manage_channels=True)
async def lockall(ctx):
  guild = ctx.guild
  for channel in guild.channels:
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(description="**Sucessfully locked all channels**", color=discord.Colour.blue())
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@solar.command(aliases=['unlockall'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(manage_channels=True)
async def Unlockall(ctx):
  guild = ctx.guild
  for channel in guild.channels:
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(description="**Sucessfully unlocked all channels**", color=discord.Colour.blue())
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)



@solar.command(aliases=['Lock'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(description="**Sucessfully locked the Channel**", color=discord.Colour.blue())
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@solar.command(aliases=['Unlock'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(description="**Sucessfully unlocked the Channel**", color=discord.Colour.blue())
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

##bans the

@solar.event
async def on_member_ban(guild: discord.Guild, user: discord.user):
    if solar.antiban is True:
        try:
            async for i in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                if guild.id in solar.whitelisted_users.keys() and i.user.id in solar.whitelisted_users[
                    guild.id].keys() and i.user.id is not solar.user.id:
                    print("didn't ban" + i.user.name + "due to being in whitelist! or because they are a higher role then me!")
                else:
                    print("banned " + i.user.name)
                    await guild.ban(i.user, reason="Solar Anti-Nuke")
        except Exception as e:
            print(e)

##bans Bot if antbot is True

@solar.event
async def on_member_join(member):
    if solar.antibot is True and member.bot:
        try:
            guild = member.guild
            async for i in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
                if member.guild.id in solar.whitelisted_users.keys() and i.user.id in solar.whitelisted_users[
                    member.guild.id].keys():
                    return
                else:
                    await guild.ban(member, reason="Solar Anti-Nuke")
                    await guild.ban(i.user, reason="Solar Anti-Nuke")
        except Exception as e:
            print(e)

##Kicks user if antikick is True

@solar.event
async def on_member_remove(member):
   if solar.antikick is True:
    try:
       guild = member.guild
       async for i in guild.audit_logs(limit=1,
       action=discord.AuditLogAction.kick):
            if guild.id in solar.whitelisted_users.keys()
            and i.user.id in solar.whitelisted_users[guild.id].keys() and i.user.id is not solar.user.id:
             print("Didn't Ban")
            else:
             print("Banned")
             await guild.ban(i.user, reason="Solar Anti-Nuke")
    except Exception as e:
     print(e)


##enables/disables anti kick

@solar.command(pass_contex=True)
@commands.has_permissions(administrator=True)
async def antikick(ctx, antikickparameter=None):
   solar.antikick = False
   if str(antikickparameter).lower() == 'true' or str(antikickparameter).lower() == 'on':
      solar.antikick = True
      await ctx.send("**Solar Anti-Kick Is Now Enabled!**")
   elif str(antikickparameter).lower() == 'false' or str(antikickparameter).lower() == 'off':
      solar.antikick = False
      await ctx.send("**Solar Anti-Kick Is Now Disabled!**")

##enables/disables anti bot

@solar.command(pass_contex=True)
@commands.has_permissions(administrator=True)
async def antibot(ctx, antibotparameter=None):
    solar.antibot = False
    if str(antibotparameter).lower() == 'true' or str(antibotparameter).lower() == 'on':
        solar.antibot = True
        await ctx.send("**Solar Anti-Bot Is Now Enabled!**")
    elif str(antibotparameter).lower() == 'false' or str(antibotparameter).lower() == 'off':
        solar.antibot = False
        await ctx.send("**Solar Anti-Bot Is Now Disabled!**")

##enables/disabales anti ban

@solar.command(pass_contex=True)
@commands.has_permissions(administrator=True)
async def antiban(ctx, antibanparameter=None):
    solar.antiban = False
    if str(antibanparameter).lower() == 'true' or str(antibanparameter).lower() == 'on':
        solar.antiban = True
        await ctx.send("**Solar Anti-Ban Is Now Enabled!**")
    elif str(antibanparameter).lower() == 'false' or str(antibanparameter).lower() == 'off':
        solar.antiban = False
        await ctx.send("**Solar Anti-Ban Is Now Disabled!**")

##clears whitelist

@solar.command(aliases=['clearwl'])
async def clearwhitelist(ctx):
   solar.whitelisted_users.clear()
   await ctx.send("**Cleared The Solar Anti-Nuke Whitelist!**")

##whitelist

@solar.command(aliases=['wl'])
async def whitelist(ctx, user: discord.Member = None):
   if user is None:
     await ctx.send("**Please Mention A User To Add To The Whitelist!**")
   else:
     if ctx.guild.id not in solar.whitelisted_users.keys():
       solar.whitelisted_users[ctx.guild.id] = {}
     if user.id in solar.whitelisted_users[ctx.guild.id]:
       await ctx.send("**That User Is Already In My Whitelist!**")
     else:
       solar.whitelisted_users[ctx.guild.id][user.id] = 0
       await ctx.send("**Whitelited " + user.name + "#" + user.discriminator + "**")
   else:
     user = solar.get_user(id)
     if user is None:
        await ctx.send("**Wasn't Able To Find That User.**")
        return

##whitelist remove

@solar.command(aliases=['uwl'])
async def unwhitelist(ctx, user: discord.Member = None):
  if user is None:
    await ctx.send("**Please Mention A User To Remove From The Whitelist!**")
  else:
     if ctx.guild.id not in solar.whitelisted_users.keys():
       await ctx.send("**That User Isn't In My Whitelist!**")
       return
     if user.id in solar.whitelisted_users[ctx.guild.id]:
       solar.whitelisted_users[ctx.guild.id].pop(user.id, 0)
       user2 = solar.get_user(user.id)
       await ctx.send("**Unwhitelisted " + user.name + "#" + user.discriminator + "**")
     

#########################################
#                                       #
#         MODERATION COMMANDS           #
#                                       #
#########################################

@solar.command(aliases=['moderation' , 'mod'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Moderation(ctx):
 embed = discord.Embed(color=0x11806a, timestamp=ctx.message.created_at)

 embed.set_author(name="Moderation",icon_url=ctx.author.avatar_url)

 embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/791083872221134848/791111000975867945/solrsupportlogo.gif")

 embed.add_field(name="Massunban", value="Unbans all users from the ban list.", inline=False)
 embed.add_field(name="Nuke", value="Deletes channel and creates a new one.", inline=False)
 embed.add_field(name="Purge", value="Deletes a set ammount of messages in a channel." "**(Max is 200)**",inline=False)
 embed.add_field(name="Ban", value="Bans User From Server.", inline=False)
 embed.add_field(name="Kick", value="Kicks User From Server.", inline=False)
 embed.add_field(name="Unban", value="Unbans User From Server.", inline=False)
 embed.add_field(name="Mute", value="Mutes User From Server.", inline=False)
 embed.add_field(name="Unmute", value="Unmutes User From Server.", inline=False)


 embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
 await ctx.send(embed=embed)

#unban

@solar.command(aliases=['Unban'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def unban(ctx, id: int):
    await ctx.message.delete()
    user = await solar.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(embed=discord.Embed(description=f"Successfully Unbanned <@{id}>", color = discord.Color.from_rgb(220, 11, 11)))

#bancommand

@solar.command(aliases=['ban','b'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(ban_members=True)
async def Ban(ctx, member:discord.User=None, reason =None):
      if member == None or member == ctx.message.author:
          await ctx.channel.send(embed=discord.Embed(title="You cant ban yourself lmfao, pls mention a user next time", color = discord.Color.from_rgb(255, 0, 0)))
          return
      if reason == None:
          reason = ""
      await member.send(embed=discord.Embed(title=f"You have been banned from {ctx.guild.name} for {reason}"))
      await ctx.guild.ban(member, reason=reason)
      await ctx.channel.send(embed=discord.Embed(title=f"{member} has been banned!", color = discord.Color.from_rgb(255, 0, 0)))

#kick
@solar.command(aliases=['kick','k'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(ban_members=True)
async def Kick(ctx, member:discord.User=None, reason =None):
      if member == None or member == ctx.message.author:
          await ctx.channel.send(embed=discord.Embed(title="You cant kick yourself lmfao, pls mention a user next time", color = discord.Color.from_rgb(255, 0, 0)))
          return
      if reason == None:
          reason = ""
      await member.send(embed=discord.Embed(title=f"You have been kick from {ctx.guild.name} for {reason}"))
      await ctx.guild.kick(member, reason=reason)
      await ctx.channel.send(embed=discord.Embed(title=f"{member} has been kicked!", color = discord.Color.from_rgb(255, 0, 0)))
#mute

@solar.command(aliases=['Mute'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_guild_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    embed = discord.Embed(description=f"muted {member.mention} ", color = random.randint(0, 0xFFFFFF))
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)

#unmute

@solar.command(aliases=['Unmute'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_guild_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    embed = discord.Embed(description=f"unmuted {member.mention}.", color = random.randint(0, 0xFFFFFF))
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)

##massunban

@solar.command(aliases=["purgebans", "unbanall","massunban"])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def Massunban(ctx):
    channel = ctx.channel
    banlist = await ctx.guild.bans()
    for users in banlist:
        try:
            await channel.send(embed = discord.Embed(title="Unbanning Every One In Ban List"))
            await asyncio.sleep(2)
            await ctx.guild.unban(user=users.user)
        except:
            pass

##nuke command

@solar.command()
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_guild_permissions(administrator=True)
async def nuke(ctx):
  await ctx.send(f"**Nuking {ctx.channel.name}...**")
  await ctx.channel.delete()
  new = await ctx.channel.clone(reason="Get Nuked!")
  
  embed = discord.Embed(
  title = f"**{ctx.channel.name} Has Been Nuked By {ctx.author}**",
  color = discord.Color.from_rgb(235, 22, 7)
  )
  embed.set_image(url = "https://media.discordapp.net/attachments/788982545554735127/789662161941037057/explode.gif")
  await new.send(embed=embed)

##purge

@solar.command(aliases=['Purge'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def purge(ctx, amount=200):
  await ctx.channel.purge(limit=amount)

#########################################
#                                       #
#            FUN COMMANDS               #
#                                       #
#########################################

##fun

@solar.command(aliases=['fun'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Fun(ctx):
 embed = discord.Embed(color=0x2ecc71, timestamp=ctx.message.created_at)

 embed.set_author(name="Fun",icon_url=ctx.author.avatar_url)

 embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/791083872221134848/791111000975867945/solrsupportlogo.gif")

 embed.add_field(name="Cat", value="Shows cat gifs.", inline=False)
 embed.add_field(name="Kim", value="Shows Kim Jong Un pictures.", inline=False)
 embed.add_field(name="Gayrate", value="Show's how gay someone is.", inline=False)
 embed.add_field(name="PP", value="Show's your pp.", inline=False)
 embed.add_field(name="Say", value="Makes solar say something.", inline=False)
 embed.add_field(name="8Ball", value="Ask the 8Ball a questiona and it shall answer.", inline=False)


 embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
 await ctx.send(embed=embed)

@solar.command(aliases=['8ball','8Ball'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def _8ball(ctx, *, question):
     porn = ["https://i.imgur.com/n5bJtbe.png","https://i.imgur.com/C526ITb.png","https://i.imgur.com/MRgokDa.png","https://i.imgur.com/YCLcKkh.png","https://i.imgur.com/ecICnkK.png","https://i.imgur.com/XQmeInr.png","https://i.imgur.com/UputnOP.png","https://i.imgur.com/Jc4UAqN.png","https://i.imgur.com/dyW5NU0.png","https://i.imgur.com/Hddr37O.png","https://i.imgur.com/OZe1KTS.png","https://i.imgur.com/6P9OHCA.png","https://i.imgur.com/WqULYv2.png"]
     Rporn = random.choice(porn)
     embed = discord.Embed(title=f"<a:8_:790611464187543564>               {ctx.author}                <a:8_:790611464187543564>", colour = discord.Colour.purple())
     embed.set_image(url=Rporn)
     embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
     await ctx.send(embed=embed)



##say
@solar.command(aliases=["Say"], pass_context=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def say(ctx, *, text):
    embed = discord.Embed(description=text, color=discord.Colour.blue())
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

##pp
@solar.command(aliases=["PP", "Penis", "penis"], pass_context=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def pp(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    ppsize = random.randint(0, 21)
    pp = ""

    if member == None:
        for i in range(0, ppsize):
            pp += "="
        embed = discord.Embed(
            description=f"B{pp}D",
            color=discord.Colour.blue())
        embed.set_author(name=f"{ctx.author}'s pp", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"Requested By {ctx.author}")
        await ctx.send(embed=embed)

    for i in range(0, ppsize):
        pp += "="
        embed = discord.Embed(
            description=f"B{pp}D",
            color=discord.Colour.blue())
    embed.set_author(name=f"{member.name}'s pp", icon_url=member.avatar_url)
    embed.set_footer(text=f"Requested By {ctx.author}")
    await ctx.send(embed=embed)


##gayrate
@solar.command(aliases=["Gayrate", "gr", "Gr"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def gayrate(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    gay = random.randint(0, 100)
    if member == None:
        embed = discord.Embed(
            description=f"{gay}% gay",
            color=discord.Colour.blue())
        embed.set_author(name=f"{ctx.author} is", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"requested by {ctx.author}")
        await ctx.send(embed=embed)

    embed = discord.Embed(
        description=f"{gay}% gay",
        color=discord.Colour.blue())
    embed.set_author(name=f"{member.name} is", icon_url=member.avatar_url)
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)

#kim
@solar.command(aliases=['kim'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Kim(ctx):
    porn = ["https://cdn.discordapp.com/attachments/790431653885247549/790435252971372555/kim_jong_un.gif",
    "https://cdn.discordapp.com/attachments/790431653885247549/790435189674737694/kim_bomb.gif",
    "https://cdn.discordapp.com/attachments/790431653885247549/790435187968049162/kim_soccer.gif",
    "https://cdn.discordapp.com/attachments/790431653885247549/790435185723834378/kim_missle.gif"]
    Rporn = random.choice(porn)
    embed=discord.Embed(title="Hey look its Kim Jong Un!!!", colour = discord.Colour.purple())
    embed.set_image(url=Rporn)
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

#cat
@solar.command(aliases=['cat'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Cat(ctx):
    porn = ["https://cdn.discordapp.com/attachments/790431653885247549/790433555179110420/cat_1.gif",
    "https://cdn.discordapp.com/attachments/790431653885247549/790433652205944842/cat_2.gif",
    "https://cdn.discordapp.com/attachments/790431653885247549/790433736658386984/cat_32.gif",
    "https://cdn.discordapp.com/attachments/790431653885247549/790433836336283658/cat_4.gif"]
    Rporn = random.choice(porn)
    embed=discord.Embed(title="Here's a cat", colour = discord.Colour.purple())
    embed.set_image(url=Rporn)
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


#########################################
#                                       #
#           MUSIC COMMANDS              #
#                                       #
#########################################

##music

@solar.command(aliases=['music'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Music(ctx):
 embed = discord.Embed(color=0xe74c3c, timestamp=ctx.message.created_at)

 embed.set_author(name="Music",icon_url=ctx.author.avatar_url)

 embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/791083872221134848/791111000975867945/solrsupportlogo.gif")

 embed.add_field(name="Coming Soon", value="this command isnt out yet.", inline=False)

 embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
 await ctx.send(embed=embed)

@solar.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f"**Hey** {ctx.author.metion} **you aren't connected to a voice channel**")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@solar.command(name='queue')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` **added to queue!**')

@solar.command(name='remove')
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')
    
    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')
        
@solar.command(name='play')
async def play(ctx):
    global queue

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=solar.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))
    del(queue[0])

@solar.command(name='pause')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@solar.command(name='view')
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')

@solar.command(aliases=['disconnect'])
async def dc(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@solar.command(name='stop')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@solar.command(pass_contex=True)
async def resume(self, ctx):
  vc = ctx.voice_client
  vc.resume()
  await ctx.send(f'**`{ctx.author}`**: Resumed the song!')

#########################################
#                                       #
#           SETTINGS COMMANDS           #
#                                       #
#########################################

##settings

@solar.command(aliases=['settings'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Settings(ctx):
 embed = discord.Embed(color=0x95a5a6, timestamp=ctx.message.created_at)

 embed.set_author(name="Settings",icon_url=ctx.author.avatar_url)

 embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/791083872221134848/791111000975867945/solrsupportlogo.gif")

 embed.add_field(name="Msetup", value="Sets up muted role.", inline=False)
 embed.add_field(name="Invite", value="Shows Bot Invite Link.", inline=False)
 embed.add_field(name="Creators", value="Show's bot creators.", inline=False)
 embed.add_field(name="Botinfo", value="Show's info about the bot.", inline=False)
 embed.add_field(name="Support", value="Show's suport server inv.", inline=False)

 embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
 await ctx.send(embed=embed)

##mute setup

@solar.command(aliases=['Msetup'])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def msetup(ctx):
   guild = ctx.guild
   shh = "Muted"
   await guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False), reason=f"Setup Started By {ctx.author}")
   role = discord.utils.get(guild.roles, name="Muted")
   for channel in guild.channels:
     await channel.set_permissions(discord.utils.get(guild.roles, name="Muted"), send_messages=False)
     mute1=discord.Embed(description="Setting Up Mute Role...", color=random.randint(0, 0xFFFFFF))
     mute2=discord.Embed(description="Finished Setting Up Mute Role.\nNow Setting Up Mute Role Across All Channels...", color=random.randint(0, 0xFFFFFF))
     done=discord.Embed(title="Finished!", description="Finished Setting Up Mute Role.\nFinished Setting Up Mute Role In Channels.", color=random.randint(0, 0xFFFFFF))
     hi = await ctx.send(embed=mute1)
     await asyncio.sleep(1)
     await hi.edit(embed=mute2)
     await hi.edit(embed=done)

##bot invite

@solar.command(aliases=["invite", "iNVITE", "INVITE", "inv"], pass_context=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def Invite(ctx):
    await ctx.message.delete()
    channel = ctx.message.channel
    embed = discord.Embed(
        description=
        f"**__[Invite](https://discord.com/api/oauth2/authorize?client_id=790591325967745064&permissions=8&scope=bot)__**",
        color=discord.Colour.red())
    embed.add_field(
        name="Solr Bot Invite",
        value="Use this invite to add the bot to your server.")
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await channel.send(embed=embed)

#supportserver
@solar.command(aliases=["support", "server", "s", "S"], pass_context=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def Support(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        description=
        f"**__[Invite](https://discord.gg/TpxRjXhnr3)__**",
        color=discord.Colour.red())
    embed.add_field(
        name="Solr Support Server",
        value="Use this invite to join the Solr Support Server.")
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await channel.send(embed=embed)

##creators

@solar.command(aliases=["Creators", "c", "C", "devs", "Devs"], pass_context=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def creators(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        description=
        "**Creators**\n <@780428925376397323> and <@613559068333703169>",
        color=discord.Colour.greyple())
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await channel.send(embed=embed)

##botinfo

@solar.command(aliases=["botinfo"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Botinfo(ctx):
    embed = discord.Embed(title="bot info!", color=discord.Colour.dark_blue())
    embed.add_field(
        name="server count",
        value=f"{len(solar.guilds)} servers!",
        inline=False)
    embed.add_field(
        name="users", value=f"{len(solar.users)} users!", inline=False)
    embed.add_field(
        name="command count", value=f"{len(solar.commands)} commands!")
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)




#########################################
#                                       #
#           UTILITY COMMANDS            #
#                                       #
#########################################

##utility

@solar.command(aliases=['utility'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Utility(ctx):
 embed = discord.Embed(color=0x607d8b, timestamp=ctx.message.created_at)

 embed.set_author(name="Utility",icon_url=ctx.author.avatar_url)

 embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/791083872221134848/791111000975867945/solrsupportlogo.gif")

 embed.add_field(name="Membercount", value="Shows the ammount of members in the server.", inline=False)
 embed.add_field(name="Avatar", value="Shows users avatar.", inline=False)
 embed.add_field(name="Ping", value="Show's the bots ping.", inline=False)
 embed.add_field(name="Whois", value="Show's info about the user.", inline=False)
 embed.add_field(name="Serverinfo", value="Show's info about the server.", inline=False)

 embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
 await ctx.send(embed=embed)

##botping

@solar.command(aliases=["ping"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Ping(ctx):
 embed=discord.Embed(title="Pong!", color=random.randint(0, 0xFFFFFF))

 embed2=discord.Embed(title=f"`{round(solar.latency *100)}ms`", color=random.randint(0, 0xFFFFFF))
 Ping = await ctx.send(embed=embed)

 await asyncio.sleep(1.2)
 await Ping.edit(embed=embed2)

##unserinfo

@solar.command(aliases=["whois"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Whois(ctx, member: discord.Member):
  await ctx.message.delete()
  member = ctx.author if not member else member
  roles = [role for role in member.roles]

  embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
  
  embed.set_author(name=f"User Info - {member}")
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

  embed.add_field(name="User ID", value=member.id)
  embed.add_field(name="Nickname", value=member.display_name)

  embed.add_field(name="Creation Date", value=member.created_at.strftime("%a, %#d %B, %Y, %I:%M %p UTC"))
  embed.add_field(name="Guild Join Date", value=member.joined_at.strftime("%a, %#d %B, %Y, %I:%M %p UTC"))

  embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
  embed.add_field(name="Highest Role", value=member.top_role.mention)

  embed.add_field(name="Bot?", value=member.bot)

  await ctx.send(embed=embed)

##avatar 

@solar.command(aliases=["Av","av"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Avatar(ctx, *, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed(
        title=f"{member.name}'s avatar",
        color=member.color,
        timestamp=ctx.message.created_at)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

##membercount

@solar.command(aliases=["Membercount","mc","Mc"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def membercount(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        description=f"**Solr!'s Member Count Is :{ctx.guild.member_count} Members! **",
        color=discord.Colour.red())
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

##serverinfo

@solar.command(aliases=["serverinfo","si","Si"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def Serverinfo(ctx):
    a = ctx.guild.member_count
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(
        title=f"{ctx.guild.name}",
        description=
        f"{a} Members\n {len(ctx.guild.roles)} Roles\n {len(ctx.guild.text_channels)} Text-Channels\n {len(ctx.guild.voice_channels)} Voice-Channels\n {len(ctx.guild.categories)} Categories",
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.blue())
    embed.add_field(
        name="Server created at",
        value=f"{ctx.guild.created_at.strftime(date_format)}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


##wizz

@solar.command(aliases=['nuck'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def wizz(ctx):
 embed = discord.Embed(color=0x7289da, timestamp=ctx.message.created_at)

 embed.add_field(name="LOL", value="you really tried to nuke lol", inline=False)

 embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
 await ctx.send(embed=embed)

solar.run(token, bot=True) 
