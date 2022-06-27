from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from resources.CraftingStore import CraftingStore
from resources.ExtraFunctions import ExtraFunctions
from datetime import datetime
import json, discord

class SearchTransaction(commands.Cog):
    
    # Declaring global values
    global embed_messages, embed_config, err_messages, commands_config, whitelist_servers, config
    
    with open('./config.json', encoding="utf-8") as c:
        config = json.load(c)
        
    whitelist_servers = config["whitelist_servers"]
    embed_messages = config["language"]["embed_messages"]
    embed_config = config["embed_config"]
    err_messages = config["language"]["error_messages"]
    commands_config = config["language"]["commands"]
    
    def __init__(self, bot):
        self.bot = bot
        
    @cog_ext.cog_slash(name=commands_config["search_transaction"]["command"], description=commands_config["search_transaction"]["description"], guild_ids=whitelist_servers)
    async def _search_transactions(self, ctx: SlashContext, nick: str, transaction_id: str):
        self.nick = nick
        self.transaction_id = transaction_id
        
        extra_fnc = ExtraFunctions()
        validate = extra_fnc.check_permissions(permissions="search_transactions", rol_ids=ctx.author.roles, user_id=ctx.author.id)
                
        if(validate):
            
            # Saving logs
            extra_fnc.save_log(username=ctx.author, user_id=ctx.author.id, command=str(commands_config["search_transaction"]["command"]) + " " + self.nick + " " + self.transaction_id)
            
            if(self.nick == None or self.transaction_id == None):
                await ctx.send("```{} {}{} <nick> <transaction_id>```".format(err_messages["invalid_command"], config["prefix"], commands_config["search_transaction"]["command"]))
            else:
                store = CraftingStore()
                response = store.search_transaction(user=self.nick, transaction_id=self.transaction_id)
                
                if(response["status"] == "success"):
                    embed = discord.Embed(title=embed_config["title"], description=embed_messages["description"], color=int(embed_config["color"], 16))
                    embed.set_thumbnail(url=embed_config["thumbnail_url"])
                    embed.add_field(name=embed_messages["crafting_responses"]["transactionId"], value=response["response"]["transactionId"], inline=False)
                    embed.add_field(name=embed_messages["crafting_responses"]["inGameName"], value=response["response"]["inGameName"], inline=False)
                    embed.add_field(name=embed_messages["crafting_responses"]["email"], value=response["response"]["email"], inline=False)
                    embed.add_field(name=embed_messages["crafting_responses"]["packageName"], value=response["response"]["packageName"], inline=False)
                    embed.add_field(name=embed_messages["crafting_responses"]["price"], value=str(response["response"]["price"]) + str(embed_messages["crafting_responses"]["currency"]), inline=False)
                    if(response["response"]["notes"] != None):
                        embed.add_field(name=embed_messages["crafting_responses"]["notes"], value=response["response"]["notes"], inline=False)
                    embed.add_field(name=embed_messages["crafting_responses"]["gateway"], value=response["response"]["gateway"], inline=False)
                    embed.add_field(name=embed_messages["crafting_responses"]["timestamp"], value=datetime.fromtimestamp(response["response"]["timestamp"]), inline=False)
                    embed.set_footer(text=embed_messages["footer"])
                    await ctx.send(embed = embed)
                else:
                    await ctx.send("```"+response["message"]+"```")
        else:
            await ctx.reply("```"+err_messages["permissions_err"]+"```")
        
def setup(bot):
    bot.add_cog(SearchTransaction(bot))