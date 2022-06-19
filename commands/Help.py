from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import json, discord

class Help(commands.Cog):
    
    global config, whitelist_servers, commands_config, embed_messages, embed_config
    
    with open('./config.json', encoding="utf-8") as c:
        config = json.load(c)

    whitelist_servers = config["whitelist_servers"]
    commands_config = config["language"]["commands"]
    embed_messages = config["language"]["embed_messages"]
    embed_config = config["embed_config"]
    
    def __init__(self, bot):
        self.bot = bot
        
    @cog_ext.cog_slash(name=commands_config["help"]["command"], description=commands_config["help"]["description"], guild_ids=whitelist_servers)
    async def _help(self, ctx: SlashContext):
        embed = discord.Embed(title=embed_config["title"], description=embed_messages["description"], color=int(embed_config["color"], 16))
        embed.set_thumbnail(url=embed_config["thumbnail_url"])
        embed.add_field(name=str(config["prefix"]) + str(commands_config["help"]["command"]), value="```"+commands_config["help"]["description"]+"```", inline=False)
        embed.add_field(name=str(config["prefix"]) + str(commands_config["search_transaction"]["command"]), value="```"+commands_config["search_transaction"]["description"]+"```", inline=False)
        embed.add_field(name=str(config["prefix"]) + str(commands_config["get_player_list"]["command"]), value="```"+commands_config["get_player_list"]["description"]+"```", inline=False)
        embed.add_field(name=str(config["prefix"]) + str(commands_config["search_giftcard"]["command"]), value="```"+commands_config["search_giftcard"]["description"]+"```", inline=False)
        embed.set_footer(text=embed_messages["footer"])
        await ctx.send(embed = embed)
        
def setup(bot):
    bot.add_cog(Help(bot))