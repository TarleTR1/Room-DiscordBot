########################################
# - - - - - - MEB PRESENTS - - - - - - #
# Name of produce: Room-DiscordBot     #
# Author of the bot: Machnev Egor      #
# Contacts in the network:             #
# --Web-Site > smtechnology.info       #
# --Telegram > @machnev_egor           #
# --VK > https://vk.com/machnev_egor   #
# --Email > meb.official.com@gmail.com #
########################################

# import main modules
import discord as discord
from discord import Activity, ActivityType
from discord.ext import commands as commands
from configurationFile import BotConfig as BotConfig
import datetime as datetime
import pickle as pickle
from random import randint as randint

# creating a client for the bot
client = discord.Client()
# prefix for all ctx-commands of the bot
client = commands.Bot(command_prefix=["room/"])
# to use the internal help command
client.remove_command("help")


# working with a text database
def working_with_the_database(registered_channels=None):
    # check for the integrity of the database
    try:
        # attempt to open the database
        pickle.load(open("configurationFile/database.sm", "rb+"))
    except Exception as E:
        # download of reset the database
        pickle.dump(dict({60547261464449: dict({60547261464449: [60547261464449, "🚪Room", []]})}),
                    open("configurationFile/database.sm", "rb+"))
    # update the database if required
    if registered_channels != None:
        pickle.dump(registered_channels, open("configurationFile/database.sm", "rb+"))
    # returning the current stored database
    return pickle.load(open("configurationFile/database.sm", "rb+"))


# connection notification
@client.event
async def on_ready():
    # sending data to the terminal
    print("-----------------------------")
    print("Bot launched into the network")
    print(f"Name in network: {client.user}")
    print(f"ID: {client.user.id}")
    print("-----------------------------")
    # list of all servers that the bot is connected to
    members = "\n".join([f"|♡|➳ {guild.name}" for guild in client.guilds])
    print(f"|♡|All friends of the bot:\n{members}")
    print("-----------------------------")
    # setting the bot's status
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game("room/help"))


# sending all necessary information about the bot to help embed
@client.command(pass_context=True)
async def help(ctx):
    # creating and sending embed
    help_embed = discord.Embed(colour=discord.Color(0x3b1a11), url=BotConfig.BotInvite,
                               title="**Room** - Сlick here to __invite__ to your server😏")
    help_embed.add_field(name="Basic command for adding a marker:", inline=True,
                         value="┣ **room/addmarker** - then enter the channel ID and category ID (you must activate _developer mode_)\n┣ **room/deletemarker** - then enter the channel ID\n┗ **room/info** - next, you will immediately see all the information about all the markers on your server")
    help_embed.add_field(name="Technical support site:", value=f"{BotConfig.BotSite}", inline=True)
    help_embed.set_footer(text="P.S. To add a marker you must have administrator rights")
    await ctx.send(embed=help_embed)


# adding a marker to a channel with a category
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def addmarker(ctx, channel_id=None, category_id=None, layout_text=None):
    # sending data to the terminal
    print(datetime.datetime.today())
    print(f"{ctx.guild.name}-->{ctx.author}")
    print(f"Command name: room/addmarker {list(ctx.args)[1:]}")
    # logic for adding a marker
    try:
        # checking for correct spelling
        if (channel_id != None and len(list(channel_id)) == 18) and (
                category_id != None and len(list(category_id)) == 18):
            # correction of the entered data
            channel_id, category_id = int(channel_id), int(category_id)
            if layout_text == None:
                layout_text = "🚪Room"
            # adding a marker if this is the first channel on the server
            if ctx.guild.id not in list(working_with_the_database().keys()):
                # uploading new data to the database
                updated_database = working_with_the_database()
                updated_database.update(dict({ctx.guild.id: dict({channel_id: [category_id, layout_text, []]})}))
                working_with_the_database(registered_channels=updated_database)
                # creating and forming an embed structure
                add_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                          title="**Room** - Your first marker on this server was created __successfully__🥳")
            # changing the marker if the channel already exists
            elif channel_id in list(working_with_the_database()[ctx.guild.id].keys()):
                # uploading new data to the database
                updated_database = working_with_the_database()
                updated_database[ctx.guild.id][channel_id] = [category_id, layout_text, []]
                working_with_the_database(registered_channels=updated_database)
                # creating and forming an embed structure
                add_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                          title="**Room** - The marker was __successfully modified__✍")
            # adding a marker if there are already added channels on the server
            elif list(working_with_the_database().keys()) != []:
                # uploading new data to the database
                updated_database = working_with_the_database()
                updated_database[ctx.guild.id].update(dict({channel_id: [category_id, layout_text, []]}))
                working_with_the_database(registered_channels=updated_database)
                # creating and forming an embed structure
                add_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                          title="**Room** - Your additional marker was created __successfully__👌")
            # adding informative data and sending embed
            add_embed.add_field(name="Channel ID:", value=f"{channel_id}", inline=True)
            add_embed.add_field(name="Category ID:", value=f"{category_id}", inline=True)
            add_embed.add_field(name="Standard name:", value=f"{layout_text}", inline=True)
            await ctx.send(embed=add_embed)
            # sending data to the terminal
            print(f"Added/changed marker: {channel_id}-->{category_id}-->{layout_text}")
        # warnings about incorrect data
        else:
            # creating and sending embed
            error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                        title="**Room** - Oops, I think you're __typing__ something __wrong__😜")
            error_embed.add_field(name="For example (standard input without additional content):",
                                  value=f"```room/addmarker {randint(10 ** (18 - 1), 10 ** 18 - 1)} {randint(10 ** (18 - 1), 10 ** 18 - 1)}```")
            error_embed.add_field(name="For example (with the introduction of the standard name of a channel):",
                                  value=f"```room/addmarker {randint(10 ** (18 - 1), 10 ** 18 - 1)} {randint(10 ** (18 - 1), 10 ** 18 - 1)} 🎄Party```")
            error_embed.set_footer(text="P.S. Enter the standard channel name without spaces")
            await ctx.send(embed=error_embed)
            # sending data to the terminal
            print(f"ERROR: Incorrect data entry")
    # catching errors when adding a marker
    except Exception as E:
        # generating an embed that informs you of an error and sending it
        error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                    title="**Room** - Oops, something __went wrong__ when you set the marker😳")
        error_embed.add_field(name="Technical support site:", value=f"{BotConfig.BotSite}", inline=True)
        error_embed.add_field(name="Error date:", value=f"{datetime.datetime.today()}", inline=True)
        error_embed.add_field(name="Сause of error:", value=f"{E}", inline=True)
        await ctx.send(embed=error_embed)
        # sending data to the terminal
        print(f"ERROR: {E}")
    # sending data to the terminal
    print("-----------------------------")


# catching errors about a lack of rights
@addmarker.error
async def addmarker_error(ctx, error):
    # generating an embed that informs you of an error and sending it
    error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                title="**Room** - You __don't have__ enough __rights__ to add markers🤨")
    await ctx.send(embed=error_embed)


# deleting an installed marker
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def deletemarker(ctx, channel_id=None):
    # sending data to the terminal
    print(datetime.datetime.today())
    print(f"{ctx.guild.name}-->{ctx.author}")
    print(f"Command name: room/deletemarker {list(ctx.args)[1:]}")
    # logic for delete a marker
    try:
        # checking for correct spelling
        if channel_id != None and len(list(channel_id)) == 18:
            # correction of the entered data
            channel_id = int(channel_id)
            # the presence of markers
            if ctx.guild.id not in list(working_with_the_database().keys()):
                # creating and forming an embed structure
                delete_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                             title="**Room** - There is __nothing to delete__ on this server yet😄")
            elif channel_id not in list(working_with_the_database()[ctx.guild.id].keys()):
                # creating and forming an embed structure
                delete_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                             title="**Room** - In any case, this channel __wasn't in__ the database🧐")
            else:
                # uploading new data to the database
                updated_database = working_with_the_database()
                updated_database[ctx.guild.id].pop(channel_id)
                working_with_the_database(registered_channels=updated_database)
                # creating and forming an embed structure
                delete_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                             title="**Room** - The specified channel was __successfully deleted__😊")
            # adding informative data and sending embed
            delete_embed.add_field(name="Channel ID:", value=f"{channel_id}", inline=True)
            delete_embed.add_field(name="Delete status:", value="The channel is not in the database", inline=True)
            delete_embed.add_field(name="Сurrent commands now:", inline=True,
                                   value="┣ **room/help**\n┣ **room/addmarker**\n┗ **room/info**")
            await ctx.send(embed=delete_embed)
        # warnings about incorrect data
        else:
            # creating and sending embed
            error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                        title="**Room** - Oops, I think you're __typing__ something __wrong__😜")
            error_embed.add_field(name="Example of the correct spelling of this command:",
                                  value=f"```room/deletemarker {randint(10 ** (18 - 1), 10 ** 18 - 1)}```", inline=True)
            error_embed.add_field(name="Сurrent commands now:", inline=True,
                                  value="┣ **room/help**\n┣ **room/addmarker**\n┗ **room/info**")
            await ctx.send(embed=error_embed)
            # sending data to the terminal
            print(f"ERROR: Incorrect data entry")
    # catching errors when deleting a marker
    except Exception as E:
        # generating an embed that informs you of an error and sending it
        error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                    title="**Room** - Oops, something __went wrong__ when you removed the marker😳")
        error_embed.add_field(name="Technical support site:", value=f"{BotConfig.BotSite}", inline=True)
        error_embed.add_field(name="Error date:", value=f"{datetime.datetime.today()}", inline=True)
        error_embed.add_field(name="Сause of error:", value=f"{E}", inline=True)
        await ctx.send(embed=error_embed)
        # sending data to the terminal
        print(f"ERROR: {E}")
    # sending data to the terminal
    print("-----------------------------")


# catching errors about a lack of rights
@deletemarker.error
async def deletemarker_error(ctx, error):
    # generating an embed that informs you of an error and sending it
    error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                title="**Room** - You __don't have__ enough __rights__ to delete markers🤨")
    await ctx.send(embed=error_embed)


# view information about all existing markers
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def info(ctx):
    # sending data to the terminal
    print(datetime.datetime.today())
    print(f"{ctx.guild.name}-->{ctx.author}")
    print(f"Command name: room/info {list(ctx.args)[1:]}")
    # the logic for generating the output information
    try:
        # comparison for the presence of markers on the server
        if ctx.guild.id not in list(working_with_the_database().keys()):
            # creating and forming an embed structure
            info_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                       title="**Room** - Wow, it looks like you __haven't put__ any markers yet😀")
        elif list(working_with_the_database()[ctx.guild.id].keys()) == []:
            # creating and forming an embed structure
            info_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                       title="**Room** - Wow, looks like __you deleted__ all your markers😮")
        else:
            # creating and forming an embed structure
            info_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                       title="**Room** - Yes, of course, here are __all the channels__ with __markers__😎")
            # listing of all information about the token on the server
            for channel in list(working_with_the_database()[ctx.guild.id].keys()):
                info_embed.add_field(name="Marker data:", inline=True,
                                     value=f"```Channel ID: {channel}\nCategory ID: {working_with_the_database()[ctx.guild.id][channel][0]}\nStandart name: {working_with_the_database()[ctx.guild.id][channel][1]}\nSome data: {working_with_the_database()[ctx.guild.id][channel][2]}```")
        # concluding information and sending embed
        info_embed.set_footer(
            text="P.S. The last item in the output data for the channel is the active channel IDs created by the bot")
        await ctx.send(embed=info_embed)
    # catching errors when checking the information on the markers
    except Exception as E:
        # generating an embed that informs you of an error and sending it
        error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                    title="**Room** - Oops, something __went wrong__ when you removed the marker😳")
        error_embed.add_field(name="Technical support site:", value=f"{BotConfig.BotSite}", inline=True)
        error_embed.add_field(name="Error date:", value=f"{datetime.datetime.today()}", inline=True)
        error_embed.add_field(name="Сause of error:", value=f"{E}", inline=True)
        await ctx.send(embed=error_embed)
        # sending data to the terminal
        print(f"ERROR: {E}")
    # sending data to the terminal
    print("-----------------------------")


# catching errors about a lack of rights
@info.error
async def info_error(ctx, error):
    # generating an embed that informs you of an error and sending it
    error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                title="**Room** - You __don't have__ enough __rights__ to view existing markers🤨")
    await ctx.send(embed=error_embed)


# creating a separate voice channel when joining a specific channel
@client.event
async def on_voice_state_update(member: discord.Member, before, after):
    # logic for creating/deleting voice channels
    try:
        # checking for connection to a specific channel
        if after.channel is not None:
            for guild in client.guilds:
                # checking for the presence of a server in the database
                if guild.id not in list(working_with_the_database().keys()):
                    return
                # checking for a marker in the database
                if after.channel.id in list(working_with_the_database()[guild.id].keys()):
                    # the establishment of a separate voice channel
                    new_voice_channel = await guild.create_voice_channel(
                        name=f"┗{working_with_the_database()[guild.id][after.channel.id][1]} [{len(working_with_the_database()[guild.id][after.channel.id][2]) + 1}]",
                        category=discord.utils.get(guild.categories,
                                                   id=working_with_the_database()[guild.id][after.channel.id][0]))
                    # reserving channels ID for further work with the user
                    channel_id_reservation = after.channel.id
                    new_channel_id_reservation = new_voice_channel.id
                    # moving a user to a new channel
                    await member.move_to(new_voice_channel)
                    # uploading new data to the database
                    updated_database = working_with_the_database()
                    updated_database[guild.id][channel_id_reservation][2].append(new_channel_id_reservation)
                    # clearing the array and sorting data
                    for channel_id in updated_database[guild.id][channel_id_reservation][2]:
                        for number_of_duplicate_channels in range(
                                updated_database[guild.id][channel_id_reservation][2].count(channel_id) - 1):
                            updated_database[guild.id][channel_id_reservation][2].remove(channel_id)
                    # analysis for the presence of a voice channel and renaming of existing channels
                    channel_number = 0
                    while channel_number != len(updated_database[guild.id][channel_id_reservation][2]):
                        # getting a channel from the server
                        channel = guild.get_channel(
                            updated_database[guild.id][channel_id_reservation][2][channel_number])
                        # working with a channel, if it still exists
                        try:
                            # renaming a channel if it is active
                            if len(channel.members) != 0:
                                # renaming a channel and creating a "channels branch"
                                if channel_number != len(updated_database[guild.id][channel_id_reservation][2]) - 1:
                                    await channel.edit(
                                        name=f"┣{working_with_the_database()[guild.id][channel_id_reservation][1]} [{channel_number + 1}]")
                                else:
                                    await channel.edit(
                                        name=f"┗{working_with_the_database()[guild.id][channel_id_reservation][1]} [{channel_number + 1}]")
                                # shift the register to process the next channel, since this is a positive case
                                channel_number += 1
                            # deleting a channel from the created ones, if there is no one in the channel, and the wait_for method did not have time to detect it
                            else:
                                await channel.delete()
                                updated_database[guild.id][channel_id_reservation][2].remove(
                                    updated_database[guild.id][channel_id_reservation][2][channel_number])
                        # deleting a channel from the database if it has already been deleted
                        except Exception as E:
                            updated_database[guild.id][channel_id_reservation][2].remove(
                                updated_database[guild.id][channel_id_reservation][2][channel_number])
                    # saving the updated array with channels to the main database
                    working_with_the_database(registered_channels=updated_database)
                    # waiting for the channel to clear
                    while len(new_voice_channel.members) != 0:
                        await client.wait_for("voice_state_update")
                    # complete deletion of the new channel
                    await new_voice_channel.delete()
                    # uploading new data to the database
                    updated_database = working_with_the_database()
                    updated_database[guild.id][channel_id_reservation][2].remove(new_channel_id_reservation)
                    # clearing the array and sorting data
                    for channel_id in updated_database[guild.id][channel_id_reservation][2]:
                        for number_of_duplicate_channels in range(
                                updated_database[guild.id][channel_id_reservation][2].count(channel_id) - 1):
                            updated_database[guild.id][channel_id_reservation][2].remove(channel_id)
                    # analysis for the presence of a voice channel and renaming of existing channels
                    channel_number = 0
                    while channel_number != len(updated_database[guild.id][channel_id_reservation][2]):
                        # getting a channel from the server
                        channel = guild.get_channel(
                            updated_database[guild.id][channel_id_reservation][2][channel_number])
                        # working with a channel, if it still exists
                        try:
                            # renaming a channel if it is active
                            if len(channel.members) != 0:
                                # renaming a channel and creating a "channels branch"
                                if channel_number != len(updated_database[guild.id][channel_id_reservation][2]) - 1:
                                    await channel.edit(
                                        name=f"┣{working_with_the_database()[guild.id][channel_id_reservation][1]} [{channel_number + 1}]")
                                else:
                                    await channel.edit(
                                        name=f"┗{working_with_the_database()[guild.id][channel_id_reservation][1]} [{channel_number + 1}]")
                                # shift the register to process the next channel, since this is a positive case
                                channel_number += 1
                            # deleting a channel from the created ones, if there is no one in the channel, and the wait_for method did not have time to detect it
                            else:
                                await channel.delete()
                                updated_database[guild.id][channel_id_reservation][2].remove(
                                    updated_database[guild.id][channel_id_reservation][2][channel_number])
                        # deleting a channel from the database if it has already been deleted
                        except Exception as E:
                            updated_database[guild.id][channel_id_reservation][2].remove(
                                updated_database[guild.id][channel_id_reservation][2][channel_number])
                    # saving the updated array with channels to the main database
                    working_with_the_database(registered_channels=updated_database)
    # catching errors and sending them to the terminal
    except Exception as E:
        # sending data to the terminal
        print(datetime.datetime.today())
        print(f"Server: {''.join([f'{guild.name} (ID={guild.id})' for guild in client.guilds])}")
        print(f"VOICE ERROR: {E}")
        print("-----------------------------")


# connect the bot to the servers discord
client.run(BotConfig.BotToken)

########################################
# - - - - - - MEB PRESENTS - - - - - - #
# Name of produce: Room-DiscordBot     #
# Author of the bot: Machnev Egor      #
# Contacts in the network:             #
# --Web-Site > smtechnology.info       #
# --Telegram > @machnev_egor           #
# --VK > https://vk.com/machnev_egor   #
# --Email > meb.official.com@gmail.com #
########################################
