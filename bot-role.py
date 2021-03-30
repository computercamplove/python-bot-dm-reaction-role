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
        """
         condition where controls user's reaction
         after reacting to specific message User gets DM message "to wait"
         and Admin gets DM message "decide Y/N"
        """

        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name != emoji_role_name:
            print("Emoji not Found")
            return
        role = discord.utils.get(guild.roles, name=role_name)

        if role is None or role.name != role_name:
            print("Role not Found")
            return

        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        if member is None:
            print("Member not Found")
            return

        await payload.member.send('Здравствуй! Жди решение админа **(Не)Женский Подкаст**')
        print("Done. User left reaction and got DM message")
        await dm_mod(admin_id, guild.members, member, role, guild_id)
        print('Admin got message')


    elif payload.user_id == admin_id:
        """ 
            condition where controls Admin reaction
            Admin reacts to DM message - to give role or not
        """

        message_id = payload.message_id
        guild_id = server_id

        with open('adminreact.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == message_id:
                    print(message_id)
                    print(x['message_id'])


                    role = discord.utils.get(bot.get_guild(server_id).roles, id=x['role_id'])
                    member = bot.get_guild(server_id).get_member(x['user_name'])

                    if payload.emoji.name != '\N{WHITE HEAVY CHECK MARK}':  # if admin press on 'x' = "Not to give role"
                        print("Sorry, admin decided to not give role to you")
                        return

                    await add_r(member, role)
                else:
                    pass
    else:
        return


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

        if payload.emoji.name != emoji_role_name:
            print("Emoji not Found")
            return
        role = discord.utils.get(guild.roles, name=role_name)

        if role is None or role.name != role_name:
            print("Role not Found")
            return

        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        if member is None:
            print("Member not Found")
            return

        await member.remove_roles(role)
        print("User removed reaction")


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
                        print("Negative reaction is not active")
                        return

                    # if admin press on 'y' = "Not to give role"
                    if role not in member.roles:
                        print('User do not have role')
                        return

                    await remove_r(member, role)
                    print("Positive reaction is not active")
                else:
                    pass

@bot.event
async def dm_mod(mod, members_guild, member, role, server):
    for user in members_guild:
        if mod == user.id:
            print(user)
            msg = await user.send(
                f"{member.mention} хочет роль **@{role.name}**.\nПрисвоить роль - нажмите :white_check_mark:,"
                f"\nОтказать в запросе - нажмите :negative_squared_cross_mark:.")
            message_channel = str(msg.channel)

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


@bot.event
async def add_r(member, role):
    await member.add_roles(role)
    print("Member got role!")


@bot.event
async def remove_r(member, role):
    await member.remove_roles(role)
    print("Took role from you!")


bot.run('ODIyMTIzMzkyMzYyMzQ4NTc1.YFNsEw.aTBY8CE13WEvhw7TBsk_o2OrEvQ')
