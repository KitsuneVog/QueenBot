import discord
import json

# register
async def register(message, payload):
    member = payload.member
    reaction = payload.emoji

    with open(f'server data/{member.guild.id}-{member.guild.name}.json', 'r') as f:
        config = json.load(f)

    await message.remove_reaction(payload.emoji, member)

    if config['config']['rules']['status'] == 'on':
        emoji = '✅'
        if str(reaction) == emoji:
            role = discord.utils.get(member.guild.roles, name='Участник')
            if role in member.roles:
                pass
            else:
                await member.add_roles(role)
                print(f'{message.guild.name}:\n  {member} - зарегистрировался')

# only one reaction
async def one_reaction_photo(member, reaction, message):
    emoji = '👍'
    if str(reaction) == emoji:
        emoji = '👎'
        await message.remove_reaction(emoji, member)
    emoji = '👎'
    if str(reaction) == emoji:
        emoji = '👍'
        await message.remove_reaction(emoji, member)

async def one_reaction_survey(member, reaction, message):
        if message.content.startswith('Опрос') or message.content.startswith('опрос') or message.content.startswith('**опрос') or message.content.startswith('**Опрос'):
            emoji1 = '1️⃣'
            emoji2 = '2️⃣'
            if str(reaction) == emoji1:
                await message.remove_reaction(emoji2, member)
            elif str(reaction) == emoji2:
                await message.remove_reaction(emoji1, member)
            else:
                await message.remove_reaction(str(reaction), member)

# created role
async def give_role(name, member):
    role = discord.utils.get(member.guild.roles, name=name)
    if role in member.roles:
        await member.remove_roles(role)
    else:
        await member.add_roles(role)

# issuing skills
async def issuing_roles(function, reaction, member, roles):
    with open(f'server data/{member.guild.id}-{member.guild.name}.json', 'r') as f:
        config = json.load(f)

    if config['config'][function]['status'] == 'on':
        amount = len(roles)
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']

        for n in range (0, amount):
            emoji = emojis[n]
            if str(reaction) == emoji:
                await give_role(roles[n], member)

async def give_colour(name, member, message):
    with open(f'server data/{member.guild.id}-{member.guild.name}.json', 'r') as f:
        config = json.load(f)

    if config['config']['colors']['status'] == 'on':
        await give_role(name, member)

        list_colour = ['Чёрный', 'Белый', 'Жёлтый', 'Оранжевый', 'Голубой', 'Ярко розовый', 'Фиолетовый']
        list_colour.remove(name)

        for role in list_colour:
            role = discord.utils.get(message.guild.roles, name=role)
            if role in member.roles:
                await member.remove_roles(role)

async def colour(member, reaction, message):
    emoji = '1️⃣'
    if str(reaction) == emoji:
        await give_colour('Чёрный', member, message)

    emoji = '2️⃣'
    if str(reaction) == emoji:
        await give_colour('Белый', member, message)

    emoji = '3️⃣'
    if str(reaction) == emoji:
        await give_colour('Жёлтый', member, message)

    emoji = '4️⃣'
    if str(reaction) == emoji:
        await give_colour('Оранжевый', member, message)

    emoji = '5️⃣'
    if str(reaction) == emoji:
        await give_colour('Голубой', member, message)

    emoji = '6️⃣'
    if str(reaction) == emoji:
        await give_colour('Ярко розовый', member, message)

    emoji = '7️⃣'
    if str(reaction) == emoji:
        await give_colour('Фиолетовый', member, message)

