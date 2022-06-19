from tabnanny import check
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_actionrow, create_select, create_select_option
from resources.ExtraFunctions import ExtraFunctions
from datetime import datetime
import json, discord 

class SearchGiftcard(commands.Cog):

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

    def __embed(self, giftcard):
        embed = discord.Embed(title=embed_config["title"], description=embed_messages["embed_gift_card"]["gratitude"], color=int(embed_config["color"], 16))
        embed.set_thumbnail(url=embed_config["thumbnail_url"])
        embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["code"], value=giftcard["response"]["gift_code"], inline=False)
        embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["token"], value=giftcard["response"]["private_token"], inline=False)
        embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["amount"], value=giftcard["response"]["amount"], inline=False)
        embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["guide_title"], value=embed_messages["embed_gift_card"]["instructions"], inline=False)
        embed.set_footer(text="")
        embed.set_image(url=embed_messages["embed_gift_card"]["banner_img"])
        
        return embed

    @cog_ext.cog_slash(name=commands_config["search_giftcard"]["command"], description=commands_config["search_giftcard"]["description"], guild_ids=whitelist_servers)
    async def _search_giftcard(self, ctx: SlashContext, user: str = None, private_token: str = None):
        self.user = user
        self.private_token = private_token

        extra_fnc = ExtraFunctions()
        validate = extra_fnc.check_permissions(permissions="search_giftcard", rol_ids=ctx.author.roles, user_id=ctx.author.id)

        if(validate):
            if (user == None and private_token == None):
                await ctx.reply("```"+err_messages["bad_usage"]+"```")
            
            else:
                if (self.user != None and self.private_token == None):
                    
                    # Saving logs
                    extra_fnc.save_log(user=ctx.author, user_id=ctx.author.id, command=str(commands_config["search_giftcard"]["command"]) + " " + self.user)
                    
                    giftcard = extra_fnc.search_gift_card(user = self.user)
                    
                    if(giftcard["status"]):
                        select_options = []
                        
                        for i in giftcard["response"]:
                            if(len(select_options) < 25):
                                select_options.append(create_select_option(i[4] + " - " + str(i[5]) + str(embed_messages["crafting_responses"]["currency"]),  value=i[4]))
                            else:
                                break
                        
                        select = create_select(
                            options = select_options,
                            placeholder="Elige",
                            min_values=1,
                            max_values=1,
                            custom_id="search_giftcard"
                        )
                        
                        comp = create_actionrow(select)
                        message = await ctx.send("", components=[comp])
                        interaction = await self.bot.wait_for("select_option", check=lambda i: i.custom_id == "search_giftcard")
                        
                        if(interaction):
                            
                            giftcard = extra_fnc.search_gift_card(private_token = interaction.values[0])
                            
                            embed = self.__embed(giftcard=giftcard)
                            await message.edit(embed=embed, components=[])
                            
                    else:
                        await ctx.send("```"+giftcard["message"]+"```")                        
                    
                elif(self.user == None and self.private_token != None):
                    
                    # Saving logs
                    extra_fnc.save_log(user=ctx.author, user_id=ctx.author.id, command=str(commands_config["search_giftcard"]["command"]) + " " + self.private_token)
                    
                    giftcard = extra_fnc.search_gift_card(private_token = self.private_token)
                    
                    if(giftcard["status"]):

                        embed = self.__embed(giftcard=giftcard)
                        await ctx.send(embed=embed)
                    
                    else:
                        await ctx.send("```"+giftcard["message"]+"```")
                        
                        
                else:
                    await ctx.send("```"+err_messages["one_of_them"]+"```")

        else:
            await ctx.send("```"+err_messages["permissions_err"]+"```")

def setup(bot):
    bot.add_cog(SearchGiftcard(bot))
