from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_actionrow, create_select, create_select_option
from resources.ExtraFunctions import ExtraFunctions
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
        embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["date"], value=giftcard["response"]["date"], inline=False)
        embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["amount"], value=giftcard["response"]["amount"], inline=False)
        embed.add_field(name=embed_messages["embed_gift_card"]["embed_titles"]["guide_title"], value=embed_messages["embed_gift_card"]["instructions"], inline=False)
        embed.set_footer(text="")
        embed.set_image(url=embed_messages["embed_gift_card"]["banner_img"])
        
        return embed

    @cog_ext.cog_slash(name=commands_config["search_giftcard"]["command"], description=commands_config["search_giftcard"]["description"], guild_ids=whitelist_servers)
    async def _search_giftcard(self, ctx: SlashContext):
        
        user_id = ctx.author.id
        extra_fnc = ExtraFunctions()
        
        search_giftcard = extra_fnc.search_gift_card(user_id=user_id)
        if(search_giftcard["status"]):
            
            select_options = []
            
            for i in search_giftcard["response"]:
                if(len(select_options) < 25):
                    select_options.append(create_select_option(i[3] + " " + i[4], value=str(i[0])))
                else:
                    break
            
            select = create_select(
                options = select_options,
                placeholder="Elige tu giftcard",
                min_values=1,
                max_values=1,
                custom_id="search_giftcard_by_user"
            )
            
            comp = create_actionrow(select)
            
            message = await ctx.send("", components=[comp])
            interaction = await self.bot.wait_for("select_option", check=lambda i: i.custom_id == "search_giftcard_by_user")
            
            if(interaction):
                
                giftcard = extra_fnc.get_gift_card_by_id(id=interaction.values[0])
                
                embed = self.__embed(giftcard=giftcard)
                await message.delete()
                await ctx.author.send(embed=embed, components=[])
                
        else:
            await ctx.send("```" + search_giftcard["message"] + "```", hidden=True)


def setup(bot):
    bot.add_cog(SearchGiftcard(bot))
