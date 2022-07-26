from discord.ext import commands
from datetime import datetime
from discord_slash.utils.manage_components import create_actionrow, create_select, create_select_option
from discord_slash import cog_ext, SlashContext
from resources.CraftingStore import CraftingStore
from resources.ExtraFunctions import ExtraFunctions
import json, discord

class SearchPlayer(commands.Cog):

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

    @cog_ext.cog_slash(name=commands_config["get_player_list"]["command"], description=commands_config["get_player_list"]["description"], guild_ids=whitelist_servers)
    async def _search_player(self, ctx: SlashContext, nick: str):

        self.nick = nick
        
        extra_fnc = ExtraFunctions()
        validate = extra_fnc.check_permissions(permissions="get_bought_items_list", rol_ids=ctx.author.roles, user_id=ctx.author.id)

        if(validate):
            
            # Saving logs
            extra_fnc.save_log(username=ctx.author, user_id=ctx.author.id, command=str(commands_config["get_player_list"]["command"]) + " " + self.nick )
            
            if(self.nick == None):
                await ctx.send("```{} {}{} <nick>```".format(err_messages["invalid_command"], config["prefix"], commands_config["get_player_list"]["command"]))
            else:
                
                store = CraftingStore()
                response = store.get_bought_items(nick)
                if(response["status"] == "success"):
                    select_options = []
                    for i in response["response"]:
                        if(len(select_options) < 25):
                            if(len(i["packageName"]) < 27):
                                select_options.append(create_select_option(i["packageName"] + " - " + str(datetime.fromtimestamp(i["timestamp"])), value=i["transactionId"]))
                            else:
                                select_options.append(create_select_option(i["packageName"][:27] + "... - " + str(datetime.fromtimestamp(i["timestamp"])), value=i["transactionId"]))
                        else:
                            break
                        
                    select = create_select(
                        options = select_options,
                        placeholder="Elige",
                        min_values=1,
                        max_values=1,
                        custom_id="bought_items"
                    )
                    
                    comp = create_actionrow(select)
                    message = await ctx.send("", components=[comp])
                    interaction = await self.bot.wait_for("select_option", check=lambda i: i.custom_id == "bought_items")

                    if(interaction):
                        response = store.search_transaction(user=nick, transaction_id=interaction.values[0])
                        embed = discord.Embed(title=embed_config["title"], description=embed_messages["description"], color=int(embed_config["color"], 16))
                        embed.set_thumbnail(url=embed_config["thumbnail_url"])
                        if(response["response"]["transactionId"] != None):
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
                        await message.edit(embed = embed, components=[])
                else:
                    await ctx.send("```"+response["message"]+"```")
        else:
            await ctx.send("```"+err_messages["permissions_err"]+"```")

def setup(bot):
    bot.add_cog(SearchPlayer(bot))
