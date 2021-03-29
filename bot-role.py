import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is online!")


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id  # message where users can left reaction
    admin_id = 331533272787976192
    server_id = 588710659882090499

    role_name = "Больной ублюдок"
    emoji_role_name = 'medved'

    if message_id == 825961963489198110:
        # condition where controls user's reaction
        # after reacting to specific message User gets DM message "to wait"
        # and Admin gets DM message "decide Y/N"

        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == emoji_role_name:
            role = discord.utils.get(guild.roles, name=role_name)
        else:
            print("Role not Found")
            role = None

        if role is not None:
            if role.name == role_name:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await payload.member.send('Привет! Ждите решение админа **(Не)Женский Подкаст**')
                    print("Done. User left reaction and got DM message")

                    await dm_mod(admin_id, guild.members, member, role, payload.emoji.name, guild_id)
                    print('Admin got message')
                else:
                    print("Member not Found")
            else:
                print("Another role")
        else:
            print("Role not Found")

    elif payload.user_id == admin_id:
        # condition where controls Admin reaction
        # Admin reacts to DM message - to give role or not
        message_id = payload.message_id
        guild_id = server_id


        with open('adminreact.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == message_id:
                    role = discord.utils.get(bot.get_guild(server_id).roles, id=x['role_id'])
                    member = bot.get_guild(server_id).get_member(x['user_name'])

                    if payload.emoji.name == '\N{WHITE HEAVY CHECK MARK}':
                        await member.add_roles(role)
                        print("Member got role!")
                    else:  # if admin press on 'x' = "Not to give role"
                        if role in member.roles:
                            await member.remove_roles(role)
                            print("we took role from you")
                        else:
                            print("Sorry, admin decided to not give role to you")
                else:
                    print('Message not found in json file')
    else:
        pass


@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    role_name = "Больной ублюдок"
    emoji_role_name = 'medved'

    admin_id = 331533272787976192
    server_id = 588710659882090499

    if message_id == 825961963489198110:
        # if user decide to not have role

        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == emoji_role_name:
            role = discord.utils.get(guild.roles, name=role_name)
        else:
            print("Role not Found")
            role = None

        if role is not None:
            if role.name == role_name:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print("User removed reaction")
                else:
                    print("Member not Found")
            else:
                print("Another role")
        else:
            print("Role not Found")

    elif payload.user_id == admin_id:
        # condition where controls Admin reaction
        # Admin reacts to DM message - to give role or not
        message_id = payload.message_id
        guild_id = server_id

        with open('adminreact.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == message_id:
                    role = discord.utils.get(bot.get_guild(server_id).roles, id=x['role_id'])
                    member = bot.get_guild(server_id).get_member(x['user_name'])

                    if payload.emoji.name == "\N{NEGATIVE SQUARED CROSS MARK}":
                        print("NOT X")
                    else:  # if admin press on 'x' = "Not to give role"
                        if role in member.roles:
                            await member.remove_roles(role)
                            print("we took role from you")
                else:
                    print('Message not found in json file')

@bot.event
async def dm_mod(mod, members_guild, member, role, emoji, server):
    for user in members_guild:
        if mod == user.id:
            print(user)
            msg = await user.send(
                f"{member.mention} хочет роль **@{role.name}**.\nПрисвоить роль - нажмите :white_check_mark:,"
                f"\nОтказать в запросе - нажмите :negative_squared_cross_mark:.")
            message_channel = msg.channel.id

            await msg.add_reaction(u"\u2705")
            await msg.add_reaction(u"\u274E")
            print("Message was sent to admins")

            with open('adminreact.json') as json_file:
                data = json.load(json_file)

                react_roles = {
                    'user_name': member.id,
                    'role_name': role.name,
                    'role_id': role.id,
                    'message_id': msg.id,
                    'server': server,
                    'dm': message_channel
                }

                data.append(react_roles)

            with open('adminreact.json', 'w') as j:
                json.dump(data, j, indent=4)

bot.run('ODIyMTIzMzkyMzYyMzQ4NTc1.YFNsEw.aTBY8CE13WEvhw7TBsk_o2OrEvQ')
