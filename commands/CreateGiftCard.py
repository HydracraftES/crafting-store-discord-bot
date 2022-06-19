from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from resources.CraftingStore import CraftingStore
from resources.ExtraFunctions import ExtraFunctions
import json, discord

class CreateGiftCard(commands.Cog):
    
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

    @cog_ext.cog_slash(name=commands_config["create_giftcard"]["command"], description=commands_config["create_giftcard"]["description"], guild_ids=whitelist_servers)
    async def _create_gift_card(self, ctx: SlashContext, nick: str = None, amount: str = None):
        
        self.nick = nick
        self.amount = amount
        
        extra_fnc = ExtraFunctions()
        validate = extra_fnc.check_permissions(permissions="create_gift_cards", rol_ids=ctx.author.roles, user_id=ctx.author.id)
        
        if(validate):
            
            # Saving logs
            extra_fnc.save_log(user=ctx.author, user_id=ctx.author.id, command=str(commands_config["create_giftcard"]["command"]) + " " + self.nick + " " + self.amount)
            
            if(self.nick == None or self.amount == None):
                await ctx.send("```{} {}{} <nick>```".format(err_messages["invalid_command"], config["prefix"], commands_config["create_giftcard"]["command"]))
            else:
                store = CraftingStore()
                response = store.create_gift_card(self.nick, self.amount)
                
                if(response["status"] == "success"):
                    embed = discord.Embed(title=embed_config["title"], description=embed_messages["embed_gift_card"]["gratitude"], color=int(embed_config["color"], 16))
                    embed.set_thumbnail(url=embed_config["thumbnail_url"])
                    embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["code"], value=response["response"]["gift_code"], inline=False)
                    embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["amount"], value=str(response["response"]["amount"]) + str(embed_messages["crafting_responses"]["currency"]), inline=False)
                    embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["token"], value=response["response"]["token"], inline=False)
                    embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["guide_title"], value=embed_messages["embed_gift_card"]["instructions"], inline=False)
                    embed.set_footer(text="")
                    embed.set_image(url="http://hydracraft.es/botimg/gift_card_banner.png")
                    await ctx.send(embed=embed)
                
                else:
                    await ctx.send("```"+response["message"]+"```")
            # pass

        else:
            await ctx.send("```"+err_messages["permissions_err"]+"```")
            
def setup(bot):
    bot.add_cog(CreateGiftCard(bot))