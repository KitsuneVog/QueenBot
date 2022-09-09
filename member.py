import discord
import json

async def member_join(bot, member):
    guild = member.guild

    print(f'{member} - присоединился к серверу {guild.name}')

    with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
        config = json.load(f)

    if config['config']['levels']['status'] == 'on':
        role = discord.utils.get(member.guild.roles, name='Новичок')
        await member.add_roles(role)

    if config['config']['passage']['status'] == 'on':
        for id in config['config']['passage']['channels']:
            channel = bot.get_channel(id)
            emb = discord.Embed(
                title=f'Уважаемые участники сервера {member.guild.name}',
                colour=10181046)
            emb.add_field(name=f'Поприветствуем нового участника',
                          value=f'{member.mention}',
                          inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=emb)

    try:
        if config['config']['rules'] != None:
            channel = bot.get_channel(config['config']['rules'])
            emb = discord.Embed(
                title=f'Привет! Вижу ты решил зайти к нам на сервер. \nНу что же, добро пожаловать на {guild.name}!',
                colour=10181046)
            emb.add_field(name='Мы рады видеть тебя здесь, обязательно прочитай правила и нажми на галочку в конце правил!',
                          value=f'>>> {channel.mention}', inline=False)
        else:
            emb = discord.Embed(
                title=f'Привет! Вижу ты решил зайти к нам на сервер. \nНу что же, добро пожаловать на {member.guild.name}! \nМы рады видеть тебя здесь, обязательно прочитай правила',
                colour=10181046)
        await member.send(embed=emb)

    except discord.errors.Forbidden:
        pass

async def member_remove(member):
    if member.bot:
        return

    guild = member.guild

    print(f'{member} - покинул сервер {member.guild.name}')

    with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
        config = json.load(f)

    if str(member.id) in config:
        del config[str(member.id)]

    with open(f'server data/{guild.id}-{guild.name}.json', 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

async def member_update(before, after, list, section):
    role = discord.utils.get(before.guild.roles, name=section)
    if role in after.roles:
        list.append(section)
        for name in list:
            role = discord.utils.get(before.guild.roles, name=name)
            if name == section:
                await after.remove_roles(role)
                break
            if role in after.roles:
                break
            else:
                continue
    if role not in after.roles:
        for name in list:
            role = discord.utils.get(before.guild.roles, name=name)
            if role in after.roles:
                role = discord.utils.get(before.guild.roles, name=section)
                await before.add_roles(role)
                break

async def member_number():
    pass

