import jotalea, settings
import discord, time, asyncio, subprocess, random, sqlite3
from datetime import timedelta
from discord.ext import commands
from discord.ext.commands import has_permissions

# Keep alive
from keep_alive import server

bot = commands.Bot(command_prefix='j!', intents=discord.Intents.all())
bot.remove_command('help')

database = sqlite3.connect('counter.db')
cursor = database.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS server_count (
    id INT PRIMARY KEY,
    count INT,
    ping TEXT,
    cpu TEXT,
    ram TEXT,
    version TEXT,
    uptime TEXT
    )
''')
database.commit()

chat_history = {}

# Store the bot's start time
bot.start_time = time.time()

# Función para desbanear a un usuario
async def unban_user(ctx, args):
    jotalea.prettyprint("cyan", "[COMMAND] j!ban unban command requested")

    # Extrae el ID del usuario a desbanear
    user_id_str = args.split("user=")[1].split(",")[0]
    user_id = int(user_id_str)

    # Obtiene la lista de usuarios baneados
    ban_list = await ctx.guild.bans()

    # Busca al usuario en la lista de usuarios baneados
    for entry in ban_list:
        if entry.user.id == user_id:
            # Desbanea al usuario
            await ctx.guild.unban(entry.user)
            embed = discord.Embed(title="User Unbanned", description=f"User with ID {user_id} has been unbanned.", color=settings.embed_color)
            await ctx.send(embed=embed)
            jotalea.prettyprint("green", f"[COMMAND] Unbanned user with ID {user_id}")
            return

    # Envía un mensaje si el usuario no está en la lista de baneados
    embed = discord.Embed(title="Error", description=f"User with ID {user_id} not found in the ban list.", color=settings.embed_color)
    await ctx.send(embed=embed)
    jotalea.prettyprint("red", f"[COMMAND] User with ID {user_id} not found in the ban list")

async def show_ban_list(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!ban list command requested")

    # Obtiene la lista de usuarios baneados
    ban_list = await ctx.guild.bans()

    if ban_list:
        # Formatea la lista de usuarios baneados
        banned_users = [f"@{entry.user.name} (Ping: <@{entry.user.id}>, ID: {entry.user.id})" for entry in ban_list]
        banned_list_str = "\n".join(banned_users)

        # Envía la lista de usuarios baneados
        embed = discord.Embed(title="Banned Users", description=banned_list_str, color=settings.embed_color)
        await ctx.send(embed=embed)

        jotalea.prettyprint("green", "[COMMAND] Banned user list sent")
    else:
        # Envía un mensaje si no hay usuarios baneados
        embed = discord.Embed(title="Banned Users", description="No users are currently banned.", color=settings.embed_color)
        await ctx.send(embed=embed)
# hehe funy number lol
        jotalea.prettyprint("green", "[COMMAND] No users are currently banned")

# Commands

@bot.command()
@has_permissions(administrator=True)
async def ban(ctx, *, args):
    jotalea.prettyprint("cyan", "[COMMAND] j!ban command requested")

    if args.lower() == "list":
        await show_ban_list(ctx)
        return

    if args.lower().startswith("user=") and ", unban" in args.lower():
        await unban_user(ctx, args)
        return

    user_id = None
    reason = "No reason given"

    args_list = args.split(", ")
    for arg in args_list:
        key, value = arg.split("=")
        if key == "user":
            user_id = int(value)
        elif key == "reason":
            reason = value.strip('"')

    if user_id:
        user = ctx.guild.get_member(user_id)
        if user:
            await ctx.guild.ban(user, reason=reason)
            embed = discord.Embed(title="User Banned", description=f"{user.mention} has been banned for: {reason}", color=settings.embed_color)
            await ctx.reply(embed=embed, mention_author=True)
            jotalea.prettyprint("green", f"[COMMAND] Banned {user.mention}")
        else:
            embed = discord.Embed(title="Error", description="User not found.", color=settings.embed_color)
            await ctx.reply(embed=embed, mention_author=True)
            jotalea.prettyprint("red", "[COMMAND] User not found")
    else:
        embed = discord.Embed(title="Invalid Syntax", description="Use `j!ban user=1234567890, reason='Your reason here'` or `j!ban list` or `j!ban user=1234567890, unban.", color=settings.embed_color)
        await ctx.reply(embed=embed, mention_author=True)
        jotalea.prettyprint("red", "[COMMAND] Invalid syntax")

@bot.command()
async def crear(ctx):
    try:
        embed = discord.Embed(title="Formatting server", description="Formatting this server with a basic format", color=settings.embed_color)
        await ctx.reply(embed=embed)
        # Permissions
        owner_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=True, administrator=True, manage_channels=True, manage_guild=True, add_reactions=True,view_audit_log=True, priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=True, connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=True, manage_emojis=True )
        admin_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=True, administrator=True, manage_channels=True, manage_guild=False,add_reactions=True,view_audit_log=True, priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=True, connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=False,manage_emojis=True )
        staff_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=True, add_reactions=True,view_audit_log=True, priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=False,manage_emojis=True )
        booster_permissions = discord.Permissions(kick_members=False,create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=True )
        member_permissions  = discord.Permissions(kick_members=False,create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=False,embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=False,deafen_members=False,move_members=False,use_voice_activation=False,change_nickname=False,manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=False)
        bot_permissions     = discord.Permissions(kick_members=True, create_instant_invite=False,ban_members=True, administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=False,manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=False,change_nickname=True, manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=False)

        await ctx.guild.create_category(name="═══Server═══")
        await ctx.guild.create_category(name="═══Chat═════")
        await ctx.guild.create_category(name="═══Audio════")
        await ctx.guild.create_category(name="═══Misc.════")

        category = discord.utils.get(ctx.guild.categories, name="═══Server═══")
        await category.create_text_channel("╔═[📢]anuncios")
        await category.create_text_channel("╠═[📜]reglas")
        await category.create_text_channel("╠═[🎉]sorteos")
        await category.create_text_channel("╠═[📊]encuestas")
        await category.create_text_channel("╠═[🆙]niveles")
        await category.create_text_channel("╠═[🎈]eventos")
        await category.create_text_channel("╠═[👋]bienvenidas")
        await category.create_text_channel("╠═[👋]despedidas")
        await category.create_text_channel("╠═[🚫]baneos")
        await category.create_text_channel("╚═[⚠️]warns")

        category = discord.utils.get(ctx.guild.categories, name="═══Chat═════")
        await category.create_text_channel("╔═[💬]general")
        await category.create_text_channel("╠═[🖼️]media")
        await category.create_text_channel("╠═[😂]memes")
        await category.create_text_channel("╠═[🤖]commands")
        await category.create_text_channel("╚═[🤖]jotabot-commands")

        category = discord.utils.get(ctx.guild.categories, name="═══Audio════")
        await category.create_voice_channel("╔═[🔊]general-1")
        await category.create_voice_channel("╠═[🔊]general-2")
        await category.create_voice_channel("╠═[🎮]gaming-1")
        await category.create_voice_channel("╠═[🎮]gaming-2")
        await category.create_voice_channel("╠═[🎤]streaming")
        await category.create_voice_channel("╚═[🔇]no-mic")

        # category = discord.utils.get(ctx.guild.categories, name="═══Misc.════")
        # await category.create_text_channel("general-1")
        # await category.create_voice_channel("no-mic")

        await ctx.guild.create_role(name = "Owner",   permissions =   owner_permissions)
        await ctx.guild.create_role(name = "Admin",   permissions =   admin_permissions)
        await ctx.guild.create_role(name = "Staff",   permissions =   staff_permissions)
        await ctx.guild.create_role(name = "Booster", permissions = booster_permissions)
        await ctx.guild.create_role(name = "Miembro", permissions =  member_permissions)
        await ctx.guild.create_role(name = "Bot",     permissions =     bot_permissions)
    except Exception as e:
        embed = discord.Embed(title="Error formatting server", description=f"Error: {e}", color=settings.embed_color)
        await ctx.reply(embed=embed)

@bot.command()
async def createinvites(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!createinvites command requested")
    if ctx.author.id != settings.admin_id:
        await ctx.send("Command not found.")
        return

    invites = []
    for guild in bot.guilds:
        try:
            text_channel = next((x for x in guild.channels if isinstance(x, discord.TextChannel)), None)
            if text_channel:
                invite = await text_channel.create_invite(max_age=900)  # Invitación que expira en 15 minutos
                invites.append(f"{guild.name}: {invite.url}")
            else:
                invites.append(f"{guild.name}: No se pudo crear la invitación (sin canal disponible).")
        except Exception as e:
            invites.append(f"{guild.name}: Error al crear la invitación - {e}")

    response = "\n".join(invites)
    if len(response) > 2000:
        await ctx.author.send(response)
    else:
        await ctx.send(response)

@bot.command()
async def credits(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!credits command requested")
    embed = discord.Embed(title="Jota-Bot Credits", description="Programmed by <@795013781607546931>\nProfile Picture made by <@1015852332266815559>\nInspired by <@836623013641191464>\nTesting by:\n- <@1093363729955049503>\n- <@795013781607546931>", color=settings.embed_color)
    await ctx.reply(embed=embed, mention_author=True)
    jotalea.prettyprint("green", "[COMMAND] j!credits command responded")

@bot.command()
async def emoji(ctx, *, emoji_name):
    emoji = discord.utils.get(bot.emojis, name=emoji_name)

    if emoji:
        embed = discord.Embed(title=f'Information about this emoji :{emoji_name}:', color=settings.embed_color)
        embed.add_field(name='Name', value=f':{emoji_name}:', inline=False)
        embed.add_field(name='ID', value=emoji.id, inline=False)
        embed.add_field(name='URL', value=emoji.url, inline=False)

        await ctx.reply(embed=embed, mention_author=True)
    else:
        await ctx.reply(f'That emoji isn\'t from this server (or I can\'t find it).', mention_author=True)

@bot.command()
async def help(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!help command requested")
    embed = discord.Embed(title="Help - Available Commands", description=f"- `j!ban`: Bans a user (admin only). Syntax: `j!ban user=1234567890, reason='Your reason here'` (123... is the user ID placeholder).\n- `j!credits`: Show the bot's credits.\n- `j!emoji`: Get information about an emoji.\n- `j!getinvite`: Get a temporary invite to this server.\n- `j!help`: Show this list.\n- `j!invite`: Get the invite link for Jota-Bot.\n- `j!kick`: Kicks a user (admin only). Syntax: `j!kick user=1234567890` (123... is the user ID placeholder).\n- `j!ping`: Check if the bot is online.\n- `j!rr`: Play the russian roulette.\n- `j!say`: Make the bot say something.\n- `j!setup`: Create an organized server from a template. ||(Para servidores en español `j!crear`)||\n- `j!shutdown`: Turn off the bot (Only for Jotalea).\n- `j!ssh`: Connect to Jotalea's computer.\n- `j!tts`: Generates a Text-To-Speech using AI.\n- `j!uptime`: Shows how much time has the bot been running.\n- `j!version`: Shows the current bot version.\n- `j!web`: Get the link of Jotalea's website.\n\n\"{bot.user.mention} Message\" Ask anything to the AI behind Jota-Bot (May not always work)", color=settings.embed_color)
    await ctx.reply(embed=embed, mention_author=True)
    jotalea.prettyprint("green", "[COMMAND] j!help command responded")

@bot.command(name='info')
async def info(ctx):
    # Obtener información
    bot_ram_usage = psutil.virtual_memory().percent
    bot_cpu_usage = psutil.cpu_percent()
    bot_ping = round(bot.latency * 1000)
    api_ping = round((discord.utils.utcnow() - ctx.message.created_at).total_seconds() * 1000)

    # Crear un embed con la información
    embed = discord.Embed(title='Bot Information', color=discord.Color.blue())
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name='Bot Username', value=bot.user.name, inline=False)
    embed.add_field(name='Servers', value=len(bot.guilds), inline=True)
    embed.add_field(name='Members in Current Server', value=len(ctx.guild.members), inline=True)
    embed.add_field(name='Bot Version', value=bot_version, inline=False)
    embed.add_field(name='RAM Usage', value=f'{bot_ram_usage}%', inline=True)
    embed.add_field(name='CPU Usage', value=f'{bot_cpu_usage}%', inline=True)
    embed.add_field(name='Bot Ping', value=f'{bot_ping} ms', inline=True)
    embed.add_field(name='API Ping', value=f'{api_ping} ms', inline=True)
    embed.add_field(name='Bot Prefix', value=bot.command_prefix, inline=False)

    '''
    CREATE TABLE IF NOT EXISTS server_count (
        id INT PRIMARY KEY,
        count INT,
        ping TEXT,
        cpu TEXT,
        ram TEXT,
        version TEXT,
        uptime TEXT
        )
    '''
    
    conn = sqlite3.connect('counter.db')
    cursor = conn.cursor()
    values = [1, len(bot.guilds), bot_ping, bot_cpu_usage, bot_ram_usage, settings.bot_version, uptime]  # Replace with actual values
    cursor.executemany('INSERT INTO server_count VALUES (?, ?, ?, ?, ?, ?, ?)', values)
    conn.commit()
    conn.close()

    # Enviar el embed al canal
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!invite command requested")
    embed = discord.Embed(title="Invite JotaBOT", description="Invite JotaBOT to your Discord server :) You can do that using [this link](https://discord.com/api/oauth2/authorize?client_id=1142577469422051478&permissions=10291617721719&scope=bot+applications.commands)\n||https://discord.com/api/oauth2/authorize?client_id=1142577469422051478&permissions=10291617721719&scope=bot+applications.commands||", color=settings.embed_color)
    await ctx.reply(embed=embed, mention_author=True)
    jotalea.prettyprint("green", "[COMMAND] j!invite command responded")

@bot.command()
@has_permissions(administrator=True)
async def kick(ctx, *, args):
    jotalea.prettyprint("cyan", "[COMMAND] j!kick command requested")

    user_id = None

    args_list = args.split(", ")
    for arg in args_list:
        key, value = arg.split("=")
        if key == "user":
            user_id = int(value)

    if user_id:
        user = ctx.guild.get_member(user_id)
        if user:
            await ctx.guild.kick(user)
            embed = discord.Embed(title="User Kicked", description=f"{user.mention} has been kicked.", color=settings.embed_color)
            await ctx.reply(embed=embed, mention_author=True)
            jotalea.prettyprint("green", f"[COMMAND] Kicked {user.mention}")
        else:
            embed = discord.Embed(title="Error", description="User not found.", color=settings.embed_color)
            await ctx.reply(embed=embed, mention_author=True)
            jotalea.prettyprint("red", "[COMMAND] User not found")
    else:
        embed = discord.Embed(title="Invalid Syntax", description="Use `j!kick user=1234567890`.", color=settings.embed_color)
        await ctx.reply(embed=embed, mention_author=True)
        jotalea.prettyprint("red", "[COMMAND] Invalid syntax")

@bot.command()
async def ping(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!ping command requested")
    import psutil

    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent

    bot_latency = round(bot.latency * 1000)
    api_latency = round((discord.utils.utcnow() - ctx.message.created_at).total_seconds() * 1000)

    embed = discord.Embed(title="Pong!", color=settings.embed_color)
    embed.add_field(name="Bot ping", value=f"{bot_latency}ms")
    embed.add_field(name="API ping", value=f"{api_latency}ms")
    embed.add_field(name="CPU Usage", value=f"{cpu_percent}%")
    embed.add_field(name="RAM Usage", value=f"{memory_percent}%")
    await ctx.reply(embed=embed, mention_author=True)
    jotalea.prettyprint("green", "[COMMAND] j!ping command responded")

@bot.command()
async def rr(ctx):
    jotalea.prettyprint("red", "[COMMAND] j!rr command requested")

    def check(message):
        return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

    embed = discord.Embed(title="Russian Roulette", description="Rules:\n- Once you react with :white_check_mark:, there's no way back\n- If you win, nothing happens\n- But if you lose, you'll get **banned**\n\nAre you sure you want to play? (react with ✅/❌)", color=settings.embed_color)
    message = await ctx.reply(embed=embed, mention_author=True)
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    await bot.wait_for("reaction", check=check, timeout=60)

@bot.command()
async def say(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!say command requested")
    message_to_say = ctx.message.content.replace("j!say ", "")
    embed = discord.Embed(title=f"{ctx.author.display_name} says:", description=message_to_say, color=settings.embed_color)
    await ctx.send(embed=embed)
    jotalea.prettyprint("green", "[COMMAND] j!say command responded")

@bot.command()
@has_permissions(administrator=True)
async def removech(ctx):
  for channel in ctx.guild.channels:
    await channel.delete()
  await ctx.send("All channels have been deleted.")
  await category.create_text_channel("general")

@bot.command()
async def setup(ctx):
    try:
        embed = discord.Embed(title="Formatting server", description="Formatting this server with a basic format", color=settings.embed_color)
        await ctx.reply(embed=embed)
        # Permissions
        owner_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=True, administrator=True, manage_channels=True, manage_guild=True, add_reactions=True,view_audit_log=True, priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=True, connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=True, manage_emojis=True )
        admin_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=True, administrator=True, manage_channels=True, manage_guild=False,add_reactions=True,view_audit_log=True, priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=True, connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=False,manage_emojis=True )
        staff_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=True, add_reactions=True,view_audit_log=True, priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=False,manage_emojis=True )
        booster_permissions = discord.Permissions(kick_members=False,create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=True )
        member_permissions  = discord.Permissions(kick_members=False,create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=False,embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=False,deafen_members=False,move_members=False,use_voice_activation=False,change_nickname=False,manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=False)
        bot_permissions     = discord.Permissions(kick_members=True, create_instant_invite=False,ban_members=True, administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=False,manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=False,change_nickname=True, manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=False)

        await ctx.guild.create_category(name="═══Server═══")
        await ctx.guild.create_category(name="═══Chat═════")
        await ctx.guild.create_category(name="═══Audio════")
        await ctx.guild.create_category(name="═══Misc.════")

        category = discord.utils.get(ctx.guild.categories, name="═══Server═══")
        await category.create_text_channel("╔═[📢]announcements")
        await category.create_text_channel("╠═[📜]rules")
        await category.create_text_channel("╠═[🎉]giveaways")
        await category.create_text_channel("╠═[📊]polls")
        await category.create_text_channel("╠═[🆙]levels")
        await category.create_text_channel("╠═[🎈]events")
        await category.create_text_channel("╠═[👋]welcome")
        await category.create_text_channel("╠═[👋]goodbye")
        await category.create_text_channel("╠═[🚫]bans")
        await category.create_text_channel("╚═[⚠️]warns")

        category = discord.utils.get(ctx.guild.categories, name="═══Chat═════")
        await category.create_text_channel("╔═[💬]general")
        await category.create_text_channel("╠═[🖼️]media")
        await category.create_text_channel("╠═[😂]memes")
        await category.create_text_channel("╠═[🤖]commands")
        await category.create_text_channel("╚═[🤖]jotabot-commands")

        category = discord.utils.get(ctx.guild.categories, name="═══Audio════")
        await category.create_voice_channel("╔═[🔊]general-1")
        await category.create_voice_channel("╠═[🔊]general-2")
        await category.create_voice_channel("╠═[🎮]gaming-1")
        await category.create_voice_channel("╠═[🎮]gaming-2")
        await category.create_voice_channel("╠═[🎤]streaming")
        await category.create_voice_channel("╚═[🔇]no-mic")

        # category = discord.utils.get(ctx.guild.categories, name="═══Misc.════")
        # await category.create_text_channel("general-1")
        # await category.create_voice_channel("no-mic")

        await ctx.guild.create_role(name = "Owner",   permissions =   owner_permissions)
        await ctx.guild.create_role(name = "Admin",   permissions =   admin_permissions)
        await ctx.guild.create_role(name = "Staff",   permissions =   staff_permissions)
        await ctx.guild.create_role(name = "Booster", permissions = booster_permissions)
        await ctx.guild.create_role(name = "Miembro", permissions =  member_permissions)
        await ctx.guild.create_role(name = "Bot",     permissions =     bot_permissions)
    except Exception as e:
        embed = discord.Embed(title="Error formatting server", description=f"Error: {e}", color=settings.embed_color)
        await ctx.reply(embed=embed)

@bot.command()
async def shutdown(ctx):
    print("[COMMAND] j!shutdown command requested")
    embed = discord.Embed(title="Shutdown JotaBOT?", description="Are you sure you want to **shutdown** JotaBOT? There is no way back...", color=settings.embed_color)
    message = await ctx.reply(embed=embed, mention_author=True)
    await message.add_reaction('✔️')
    print("[COMMAND] j!shutdown command responded")

@bot.command()
async def serverinvite(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!serverinvite command requested")

    try:
        text_channel = next((x for x in bot.guild.channels if isinstance(x, discord.TextChannel)), None)
        if text_channel:
            # Crea una invitación en ese canal
            invite = await text_channel.create_invite(max_age=900)  # Invitación que expira en 15 minutos
            embed = discord.Embed(title="Server Invite", description=f"Here is a temporary invite to {bot.guild.name}:\n{invite}", color=settings.embed_color)

        else:
            embed = discord.Embed(title="Server Invite - Error", description=f"{bot.guild.name}: Invite couldn't be created (no channels available).", color=settings.embed_color)
    except Exception as e:
        embed = discord.Embed(title="Server Invite - Error", description=f"{bot.guild.name}: Error when creating the invite: {e}", color=settings.embed_color)

    jotalea.prettyprint("green", "[COMMAND] j!serverinvite command responded")
    await ctx.reply(embed, mention_author=True)

@bot.command()
async def ssh(ctx):
    jotalea.prettyprint("cyan", f"[COMMAND] SSH requested by {ctx.author.name}")

    def checkDM(message):
        return message.author.id == ctx.author.id and message.channel.type == discord.ChannelType.private

    def check(message):
        return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

    async def run(command_array):
        try:
            result = subprocess.run(process, capture_output=True, text=True)
        except Exception as e:
            await ctx.send(f"Error: {e}.")
            await ctx.send(f"Output: {result.stdout}")
            await ctx.send(f"{result.stderr}")
        return result

    outputs = ["Password inserted, type a command", "Type a command"]
    inputs = []

    # Ask for the password via DM
    await ctx.author.send("Type the password for SSH connection")

    try:
        password_msg = await bot.wait_for('message', check=checkDM, timeout=60)
        password = password_msg.content
    except asyncio.TimeoutError:
        await ctx.send("Timed out. No password received.")
        return

    if password == settings.ssh_password:
        pass
    else:
        await ctx.send("Wrong password.")
        return

    for output in outputs:
        await ctx.send(output)

        try:
            response = await bot.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("Timed out.")
            return

        inputs.append(response.content)
        outputs.append("Type a command")

        process = response.content.split(" ")

        if str(ctx.author.id) in settings.allowed_users:
            result = run(process)
        else:
            await ctx.send(f"{ctx.author.mention} You may have guessed or found the password, but you don't have permissions. Ask <@{settings.admin_id}> to get them.")

        sl = 1994
        t = (len(result.stdout) + sl - 1) // sl
        for i in range(t):
            start = i * sl
            end = (i + 1) * sl
            s = result.stdout[start:end]
            await ctx.send(f"```{s}```")

    await ctx.send("Thanks for using JotaSSH!")
    jotalea.prettyprint("green", f"[COMMAND] {ctx.author.name}'s SSH responded and closed")

@bot.command(name='tts')
async def tts(ctx, *, text_to_speech):
    audio_file_path = jotalea.tts(text_to_speech, keys.api_key)

    if not audio_file_path:
        await ctx.reply("Error when generating audio.")
        return

    try:
        embed = discord.Embed(title="Generated TTS", description="Your Text-To-Speech has been generated", color=settings.embed_color)
        await ctx.reply(embed=embed, file=discord.File(audio_file_path))

    finally:
        os.remove(audio_file_path)

@bot.command(name='uptime')
async def uptime(ctx):
    current_time = time.time()
    uptime_seconds = current_time - bot.start_time
    global uptime
    uptime = timedelta(seconds=int(uptime_seconds))
    embed = discord.Embed(title="Uptime", description=f"My uptime is: {str(uptime)}", color=settings.embed_color)
    await ctx.reply(embed=embed, mention_author=True)

@bot.command()
async def version(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!version command requested")
    embed = discord.Embed(title="Jota-Bot Version", description=f'Version {str(settings.bot_version)}', color=settings.embed_color)
    await ctx.reply(embed=embed, mention_author=True)
    jotalea.prettyprint("green", "[COMMAND] j!version command responded")

@bot.command()
async def web(ctx):
    jotalea.prettyprint("cyan", "[COMMAND] j!web command requested")
    embed = discord.Embed(title="Jotalea's Website", description="[Visit here](http://jotalea.com.ar)", color=settings.embed_color)
    await ctx.reply(embed=embed, mention_author=True)
    # https://jotabot.jotaleaex.repl.co/
    embed = discord.Embed(title="Jotabot's Website (beta)", description="Jota-bot's live website, with real-time information about it!\n[Visit here](https://jotabot.jotaleaex.repl.co/)\nNote: the website is still in development, so it may not be fully functional.", color=settings.embed_color)
    await ctx.send(embed=embed, mention_author=True)
    jotalea.prettyprint("green", "[COMMAND] j!web command responded")

@bot.event
async def on_ready():
    jotalea.prettyprint("green", f'[BOT] Logged in as {bot.user.name} ({bot.user.id})')
    global guild_count
    while True:
        guild_count = len(bot.guilds)
        cursor.execute('''UPDATE server_count SET count = ? WHERE id = 1''', (guild_count,))
        database.commit()
        await asyncio.sleep(3600) # Update the count every hour

@bot.event
async def on_guild_join(guild):
    global guild_count
    guild_count += 1
    cursor.execute('''UPDATE server_count SET count = ? WHERE id = 1''', (guild_count,))
    database.commit()

@bot.event
async def on_guild_remove(guild):
    global guild_count
    guild_count -= 1
    cursor.execute('''UPDATE server_count SET count = ? WHERE id = 1''', (guild_count,))
    database.commit()

@bot.event
async def on_reaction_add(reaction, user):
    print(user.id)
    print(reaction.message.author.id)
    if str(reaction.emoji) == '✅' and user.id == reaction.message.author.id:
        print("[COMMAND] RUSSIAN ROULETTE MOMENT...")

        result = random.choice([True, False])

        if result:
            embed = discord.Embed(title="Russian Roulette - Sucess", description=f"Congratulations {user.mention}! You won!", color=settings.embed_color)
            await reaction.message.channel.send(embed)
            jotalea.prettyprint("green", f"[RR] {user.name} has beaten the russian roulette")
        else:
            embed = discord.Embed(title="Russian Roulette - Fail", description=f"{user.mention}, you lost, get banned", color=settings.embed_color)
            await reaction.message.channel.send(embed)
            embed = discord.Embed(title="Russian Roulette - Fail", description=f"{user.mention}, you lost the russian roulette on {reaction.message.guild.name}, get banned", color=settings.embed_color)
            await user.send(embed)
            try:
                await user.ban(reason="Russian Roulette loss")
            except Exception as e:
                if result:
                    embed = discord.Embed(title="Russian Roulette - Error", description=f"There was an error processing the russian roulette's ban, you weren't going to get banned anyway", color=settings.embed_color)
                else:
                    embed = discord.Embed(title="Russian Roulette - Error", description=f"There was an error processing the russian roulette's ban, you were going to get banned", color=settings.embed_color)
                await reaction.message.channel.send(embed)
            jotalea.prettyprint("red", f"[RR] {user.name} has lost the russian roulette on {reaction.message.guild.name}")
    jotalea.prettyprint("green", "[COMMAND] j!rr command responded")

@bot.event
async def on_reaction_add(reaction, user):
    if str(user.id) == str(settings.admin_id) and str(reaction.emoji) == '✔️':
        jotalea.prettyprint("red", "[BOT] Shutting down...")
        await bot.close()

@bot.listen('on_message')
async def on_message(message):
    global chat_history

    if message.author.bot:
        return

    # Conversation log
    if settings.printlog:
        server_name = message.guild.name if message.guild else "the DMs"
        username = message.author.name
        jotalea.prettyprint("blue", f"[MESSAGE] In {server_name}, @{username} said: {message.content}")

    # Logs help to locate and prevent server raids
    if settings.logging:
        if settings.use_async:
            try:
                asyncio.create_task(jotalea.async_webhook(settings.log_webhook, f"<@{message.author.id}> at <#{message.channel.id}> ({server_name}) said: {message.content}"))
            except Exception as e:
                jotalea.prettyprint("red", "[ERROR] Error while logging (async)")
        else:
            try:
                import os
                wh = os.environ['WEBHOOK']
                jotalea.webhook(wh, f"<@{message.author.id}> at <#{message.channel.id}> ({server_name}) said: {message.content}")
            except Exception as e:
                jotalea.prettyprint("red", "[ERROR] Error while logging")
    else:
        pass

    # If the message is for the bot
    if message.content.startswith("<@1142577469422051478>"):
        user_id = str(message.author.id)

        # Get or create the chat history for the user
        user_history = chat_history.get(user_id, [])

        # Take away the bot name from the message and add to history
        user_message = message.content.replace("<@1142577469422051478> ", '').strip()
        jotalea.prettyprint("cyan", user_message)
        user_history.append({'role': 'user', 'content': user_message})

        # Limit the chat history to a maximum amount of messages
        max_history_length = 20
        user_history = user_history[-max_history_length:]

        # Update the chat history for the user
        chat_history[user_id] = user_history

        async def throwException(er, re):
            error_message = f"> An error occurred while connecting to the API: ```{str(er)}```"
            await message.channel.send(error_message)
            jotalea.prettyprint("red", "[API] An error ocurred: " + str(er))
            jotalea.prettyprint("red", re)
        
        async with message.channel.typing():
            response = jotalea.gemini(user_message)
            print(response)
            if len(response) <= 2000:
                embed = discord.Embed(title="Jotabot AI (beta)", description=response, color=settings.embed_color)
                await message.reply(embed=embed, content="")
            else:
                embed = discord.Embed(title="Jotabot AI (beta)", description=response, color=settings.embed_color)
                await message.reply(content=response[:2000])
                response = response[2000:]
                while response:
                    embed = discord.Embed(description=response, color=settings.embed_color)
                    await message.channel.send(response[:2000])
                    response = response[2000:]
        
    # If the user is replying to the bot
    if message.reference and message.reference.cached_message:
        original_message = message.reference.cached_message
        if original_message.author == bot.user:
            user_message = message.content.replace("<@1142577469422051478> ", '').strip()
            response = jotalea.gemini(user_message)
            print(response)
            if len(response) <= 2000:
                embed = discord.Embed(title="Jotabot AI (beta)", description=response, color=settings.embed_color)
                await message.reply(embed=embed, content="")
            else:
                embed = discord.Embed(title="Jotabot AI (beta)", description=response, color=settings.embed_color)
                await message.reply(content=response[:2000])
                response = response[2000:]
                while response:
                    embed = discord.Embed(description=response, color=settings.embed_color)
                    await message.channel.send(response[:2000])
                    response = response[2000:]

try:
    import keys
    botToken = keys.bot_token
    jotalea.GPT_KEY = keys.api_key
    jotalea.GPT_ENDPOINT = keys.api_endpoint
    jotalea.prettyprint("green", "[CODE] Keys loaded sucessfully.")
except ImportError:
    jotalea.prettyprint("red", "[CODE] Could not load the keys.")
    botToken = input("Paste the bot token: ")
    jotalea.GPT_KEY = input("Paste the API Key: ")
    jotalea.GPT_ENDPOINT = input("Paste the API Endpoint (none for default): ")

server()
bot.run(botToken)