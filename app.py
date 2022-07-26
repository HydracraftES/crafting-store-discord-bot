import discord, json, os
from discord.ext import commands
from discord_slash import SlashCommand
from discord_components import DiscordComponents
from discord.ext.commands.errors import CommandNotFound, CommandInvokeError

# Importing config file
with open("./config.json", encoding="utf-8") as c:
    config = json.load(c)

bot = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.default())
slash = SlashCommand(bot, override_type=True, sync_commands=True)


# on_ready event
@bot.event
async def on_ready():
    print("\033[1m\033[96mLogged as: "+str(bot.user))
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Game(name="/help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        # print("\033[91m[!] Someone tried to use an inexistent command: " + str(error))
        pass
    
    if isinstance(error, CommandInvokeError):
        # print("\033[91m[!] CommandInvokeError: " + str(error))
        pass       
extensions = []
for files in os.listdir('./commands'):
    if(files.endswith('.py')):
        extensions.append("commands." + files[:-3])

if(__name__=="__main__"):
    for command in extensions:
        try:
            bot.load_extension(command)
            print("\033[92m[+] Added "+command+" command")
        except:
            print("\033[91m[-] Failed to load "+command)
            
    bot.run(config["bot_token"], bot=True, reconnect=True)