import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from tocen import *
import json
import asyncio
#from discord_components import  DiscordComponents, Button, ButtonStyle

import functions

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='%', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

bot.remove_command('help')

# включение бота
@bot.event
async def on_ready():
    #DiscordComponents(bot)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/help'))

    print(f'{bot.user} готов к работе')

# бота подключили к серверу
@bot.event
async def on_guild_join(guild):
    await functions.guild_join(bot, guild)

# обновление названия сервера
@bot.event
async def on_guild_update(before, after):
    if before.name != after.name:
        await functions.guild_update(before, after)

# бота отключили от сервера
@bot.event
async def on_guild_remove(guild):
    await functions.guild_remove(bot, guild)

# получение сообщения
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    global guild
    guild = message.guild

    await functions.message_lvl(bot, guild, message)

# добавление реакции
@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return

    member = payload.member
    reaction = payload.emoji
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    with open(f'server data/{message.guild.id}-{message.guild.name}.json', 'r') as f:
        config = json.load(f)

# зарегистрироватся
    if channel.id in config['config']['rules']['channels']:
        await functions.register(message, payload)

# ставить только одну рякцию

    if channel.id in config['config']['photo']['channels']:
        await functions.one_reaction_photo(member, reaction, message)

    elif channel.id in config['config']['news']['channels']:
        await functions.one_reaction_survey(member, reaction, message)

# навыки
    elif channel.id in config['config']['skills']['channels'] and config['config']['skills']['status'] == 'on':
        await message.remove_reaction(payload.emoji, member)

        roles = ['🖥программист', '🎮геймер', '🎵музыкант', '🖌художник']
        await functions.issuing_roles('skills', reaction, member, roles)

# игры
    elif channel.id in config['config']['games']['channels'] and config['config']['games']['status'] == 'on':
        await message.remove_reaction(payload.emoji, member)

        roles = ['Minecraft', 'Counter-Strike', 'Genshin Impact', 'OSU!', 'Grand Theft Auto', 'Fortnite', 'PUBG', 'World of Tanks']
        await functions.issuing_roles('games', reaction, member, roles)

# цвета
    elif channel.id in config['config']['colors']['channels'] and config['config']['colors']['status'] == 'on':
        await message.remove_reaction(payload.emoji, member)

        await functions.colour(member, reaction, message)

# роли по реакции
    elif str(channel.id) in config['config']['data']['roles']:
        if str(message.id) in config['config']['data']['roles'][channel_id]:
            pass

# подключение к серверу
@bot.event
async def on_member_join(member):
    await functions.member_join(bot, member)
    await functions.member_number()

@bot.event
async def on_member_remove(member):
    await functions.member_remove(member)


@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:

        list = ['🖥программист', '🖌художник', '🎵музыкант', '🎮геймер']
        await functions.member_update(before, after, list, '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Навыки')

        list = ['Minecraft', 'Counter-Strike', 'Genshin Impact', 'Overwatch','OSU!', 'Grand Theft Auto', 'Apex Legends', 'Fortnite', 'PUBG', 'Destiny 2', 'World of Tanks', 'Call of Duty: Modern Warfare']
        await functions.member_update(before, after, list, '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Игры')

# команда help
@slash.slash(
    name='help',
    description='это поможет вам',
    options=[
        create_option(
            name='command',
            description='команда',
            required=False,
            option_type=3,
            choices=[
                create_choice(
                    name='help',
                    value='help'
                ),
                create_choice(
                    name='lvl',
                    value='lvl'
                ),
                create_choice(
                    name='info',
                    value='info'
                ),
                create_choice(
                    name='deletion',
                    value='deletion'
                ),
                create_choice(
                    name='clear',
                    value='clear'
                ),
                create_choice(
                    name='delete',
                    value='delete'
                ),
                create_choice(
                    name='settings',
                    value='add'
                ),
                create_choice(
                    name='lever',
                    value='lever'
                )
            ]

        )
    ]
)
async def help(ctx, command=None):
    if command == None:
        await functions.help(ctx)

    elif command == 'help':
        await functions.help_info(ctx)

    elif command == 'lvl':
        await functions.lvl_info(ctx)

    elif command == 'info':
        await functions.info_info(ctx)

    elif command == 'clear':
        await functions.clear_info(ctx)

    elif command == 'deletion':
        await functions.deletion_info(ctx)

    elif command == 'delete':
        await functions.delete_info(ctx)

    elif command == 'settings':
        await functions.add_info(ctx)

    elif command == 'lever':
        await functions.lever_info(ctx)


# отправка профиля
@slash.slash(
    name='lvl',
    description='ваш уровень',
)
async def lvl(ctx):
    guild = ctx.channel.guild
    author = ctx.author
    with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
        config = json.load(f)

    if config['config']['levels']['status'] == 'on':
        emb = discord.Embed(title=f'**{guild}**', colour=10181046)
        emb.set_thumbnail(url=guild.icon_url)
        exp = round(config[f'{author.id}']['exp'], 1)
        rank = config[f'{author.id}']['rank']
        lvl = config[f'{author.id}']['lvl']
        warn = config[f'{author.id}']['warn']
        emb.add_field(name=f'lvl = {lvl}', value='повышаеться когда exp = lvl', inline=False)
        emb.add_field(name=f'exp = {exp}', value='повышаеться при отправке сообщения', inline=False)
        emb.add_field(name=f'rank = {rank}', value='когда lvl = 10', inline=False)
        emb.add_field(name=f'warn = {warn}', value='ваши нарушения', inline=False)

    else:
        emb = discord.Embed(title='', colour=10181046)
        emb.add_field(name='**Данная команда не работает**',
                      value='функция **lvl** отключена на данном сервере', inline=False)

    await ctx.send(embed=emb, hidden=True)

# отправка профиля
@slash.slash(
    name='info',
    description='узнать информацию',
    options=[
        create_option(
            name='member',
            description='пользователь',
            required=True,
            option_type=6
        )
    ]
)
@commands.has_permissions(view_audit_log=True)
async def info(ctx, member: discord.Member):
    with open(f'server data/{member.guild.id}-{member.guild.name}.json', 'r') as f:
        config = json.load(f)

    member = member.id
    exp = round(config[f'{member}']['exp'], 1)
    rank = config[f'{member}']['rank']
    lvl = config[f'{member}']['lvl']
    warn = config[f'{member}']['warn']

    emb = discord.Embed(title=f'**Профиль {member}**', colour=10181046)
    emb.add_field(name=f'lvl = {lvl}', value=f'exp = {exp}', inline=False)
    emb.add_field(name=f'rank = {rank}', value=f'warn = {warn}', inline=False)

    await ctx.message.author.send(embed=emb, hidden=True)

# обнуление пользователя
@slash.slash(
    name='deletion',
    description='обнулить пользователя',
    options=[
        create_option(
            name='member',
            description='пользователь',
            required=True,
            option_type=6
        )
    ]
)
@commands.has_permissions(administrator=True)
async def deletion(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    with open(f'server data/{member.guild.id}-{member.guild.name}.json', 'r') as f:
        config = json.load(f)

    if config['config']['levels']['status'] == 'on':
        config[f'{member.id}']['lvl'] = 0
        config[f'{member.id}']['exp'] = 0
        config[f'{member.id}']['rank'] = 0

        for n in range(1, 11):
            role = discord.utils.get(member.guild.roles, name=f'Уровень {n}')

            if role in member.roles:
                await member.remove_roles(role)
    else:
        emb = discord.Embed(title='', colour=10181046)
        emb.add_field(name='**Данная команда не работает**',
                      value='функция **deletion** отключена на данном сервере', inline=False)

    with open(f'server data/{member.guild.id}-{member.guild.name}.json', 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    try:
        emb = discord.Embed(title=f'Ваш профиль был обнулён на сервере {ctx.guild}', colour=10181046)
        emb.set_thumbnail(url=guild.icon_url)

        await member.send(embed=emb)
    except discord.errors.Forbidden:
        pass

@slash.slash(
    name='clear',
    description='очистка чата',
    options=[
        create_option(
            name='number',
            description='число',
            required=True,
            option_type=10
        )
    ]
)
@commands.has_permissions(view_audit_log=True)
async def clear(ctx, number):
    await ctx.channel.purge(limit=int(number))

    emb = discord.Embed(title=f'Очистка завершина \nУдалено {int(number)} слов', colour=10181046)
    await ctx.send(embed=emb, hidden=True)

@slash.slash(
    name='add',
    description='добовление функции в канал',
    options=[
        create_option(
            name='function',
            description='функция',
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name='Навыки',
                    value='skills'
                ),
                create_choice(
                    name='Цвета',
                    value='colors'
                ),
                create_choice(
                    name='Игры',
                    value='games'
                ),
                create_choice(
                    name='Правила',
                    value='rules'
                ),
                create_choice(
                    name='Новости',
                    value='news'
                ),
                create_choice(
                    name='Фото',
                    value='photo'
                ),
                create_choice(
                    name='Спам',
                    value='levels'
                ),
                create_choice(
                    name='Привествие',
                    value='passage'
                ),
                create_choice(
                    name='Проверка',
                    value='check'
                )
            ]
        )
    ]
)
@commands.has_permissions(administrator=True)
async def add(ctx, function):
    guild = ctx.guild
    with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
        config = json.load(f)

    config['config'][function]['channels'].append(ctx.channel.id)
    config['config'][function]['channels'] = list(set(config['config'][function]['channels']))
    config['config'][function]['status'] = 'on'

    with open(f'server data/{guild.id}-{guild.name}.json', 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    emb = discord.Embed(title=f'{function.upper()}', colour=10181046)

    if function != 'skills' and function != 'colors' and function != 'games' and function != 'rules':
        emb = discord.Embed(
            title=f'Теперь в канал -__{ctx.channel.name}__- добавлена функция {function}\nФункция __{function}__ **включена**',
            colour=10181046)
        await ctx.send(embed=emb, hidden=True)

    elif function == 'skills':
        role1 = discord.utils.get(guild.roles, name='🖥программист')
        role2 = discord.utils.get(guild.roles, name='🎮геймер')
        role3 = discord.utils.get(guild.roles, name='🎵музыкант')
        role4 = discord.utils.get(guild.roles, name='🖌художник')

        emb.add_field(name='Выберите свои навыки',
                        value=f'1) {role1.mention}\n2) {role2.mention}\n3) {role3.mention}\n4) {role4.mention}\n___нажми на реакцию под соответствующим номером___',
                        inline=False)
        message = await ctx.channel.send(embed=emb)
        emb = discord.Embed(
            title=f'Теперь в канал -__{ctx.channel.name}__- добавлена функция {function}\nФункция __{function}__ **включена**',
            colour=10181046)
        await ctx.send(embed=emb, hidden=True)

        list_emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        for emoji in list_emoji:
                await message.add_reaction(emoji=emoji)

    elif function == 'colors':
        role1 = discord.utils.get(guild.roles, name='Чёрный')
        role2 = discord.utils.get(guild.roles, name='Белый')
        role3 = discord.utils.get(guild.roles, name='Жёлтый')
        role4 = discord.utils.get(guild.roles, name='Оранжевый')
        role5 = discord.utils.get(guild.roles, name='Голубой')
        role6 = discord.utils.get(guild.roles, name='Ярко розовый')
        role7 = discord.utils.get(guild.roles, name='Фиолетовый')

        emb.add_field(name='Выберите цвет своего ника',
                        value=f'1) {role1.mention}\n2) {role2.mention}\n3) {role3.mention}\n4) {role4.mention}\n5) {role5.mention}\n6) {role6.mention}\n7) {role7.mention}\n___нажми на реакцию под соответствующим номером___',
                        inline=False)
        message = await ctx.channel.send(embed=emb)
        emb = discord.Embed(
            title=f'Теперь в канал -__{ctx.channel.name}__- добавлена функция {function}\nФункция __{function}__ **включена**',
            colour=10181046)
        await ctx.send(embed=emb, hidden=True)

        list_emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
        for emoji in list_emoji:
            await message.add_reaction(emoji=emoji)

    elif function == 'games':
        role1 = discord.utils.get(guild.roles, name='Minecraft')
        role2 = discord.utils.get(guild.roles, name='Counter-Strike')
        role3 = discord.utils.get(guild.roles, name='Genshin Impact')
        role4 = discord.utils.get(guild.roles, name='OSU!')
        role5 = discord.utils.get(guild.roles, name='Grand Theft Auto')
        role6 = discord.utils.get(guild.roles, name='Fortnite')
        role7 = discord.utils.get(guild.roles, name='PUBG')
        role8 = discord.utils.get(guild.roles, name='World of Tanks')

        emb.add_field(name='Выберите игры в которые играете',
                        value=f'1) {role1.mention}\n2) {role2.mention}\n3) {role3.mention}\n4) {role4.mention}\n5) {role5.mention}\n6) {role6.mention}\n7) {role7.mention}\n8) {role8.mention}\n___нажми на реакцию под соответствующим номером___',
                        inline=False)
        message = await ctx.channel.send(embed=emb)
        emb = discord.Embed(
            title=f'Теперь в канал -__{ctx.channel.name}__- добавлена функция {function}\nФункция __{function}__ **включена**',
            colour=10181046)
        await ctx.send(embed=emb, hidden=True)

        list_emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
        for emoji in list_emoji:
            await message.add_reaction(emoji=emoji)

    elif function == 'rules':
        async for message in ctx.channel.history(limit=1, oldest_first=False):
            await message.add_reaction(emoji='✅')

            emb = discord.Embed(
                title=f'Теперь в канал -__{ctx.channel.name}__- добавлена функция {function}\nФункция __{function}__ **включена**',
                colour=10181046)
            await ctx.send(embed=emb, hidden=True)

    with open(f'server data/{guild.id}-{guild.name}.json', 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

@slash.slash(
    name='delete',
    description='удаление функции из канала',
    options=[
        create_option(
            name='function',
            description='функция',
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name='Навыки',
                    value='skills'
                ),
                create_choice(
                    name='Цвета',
                    value='colors'
                ),
                create_choice(
                    name='Игры',
                    value='games'
                ),
                create_choice(
                    name='Правила',
                    value='rules'
                ),
                create_choice(
                    name='Новости',
                    value='news'
                ),
                create_choice(
                    name='Фото',
                    value='photo'
                ),
                create_choice(
                    name='Спам',
                    value='levels'
                ),
                create_choice(
                    name='Привествие',
                    value='passage'
                ),
                create_choice(
                    name='Проверка',
                    value='check'
                )
            ]
        )
    ]
)
@commands.has_permissions(administrator=True)
async def delete(ctx, function):
    guild = ctx.guild
    with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
        config = json.load(f)

    config['config'][function]['channels'].remove(ctx.channel.id)
    config['config'][function]['channels'] = list(set(config['config'][function]['channels']))

    with open(f'server data/{guild.id}-{guild.name}.json', 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    emb = discord.Embed(title=f'Теперь канал -__{ctx.channel.name}__- удалён из {function}\nФункция __{function}__ **выключена**', colour=10181046)
    await ctx.send(embed=emb, hidden=True)

@slash.slash(
    name='lever',
    description='изменение статуса функции на сервере',
    options=[
        create_option(
            name='function',
            description='функция',
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name='Навыки',
                    value='skills'
                ),
                create_choice(
                    name='Цвета',
                    value='colors'
                ),
                create_choice(
                    name='Игры',
                    value='games'
                ),
                create_choice(
                    name='Правила',
                    value='rules'
                ),
                create_choice(
                    name='Новости',
                    value='news'
                ),
                create_choice(
                    name='Фото',
                    value='photo'
                ),
                create_choice(
                    name='Спам',
                    value='levels'
                ),
                create_choice(
                    name='Привествие',
                    value='passage'
                ),
                create_choice(
                    name='Проверка',
                    value='check'
                )
            ]
        ),
        create_option(
            name='status',
            description='статус',
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name='Включить',
                    value='on'
                ),
                create_choice(
                    name='Выключить',
                    value='off'
                )
            ]
        )
    ]
)
@commands.has_permissions(administrator=True)
async def lever(ctx, function, status):
    guild = ctx.guild
    with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
        config = json.load(f)

        config['config'][function]['status'] = status

    with open(f'server data/{guild.id}-{guild.name}.json', 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    emb = discord.Embed(
        title=f'Функция __{function}__ **выключена**',
        colour=10181046)
    await ctx.send(embed=emb, hidden=True)

@slash.slash(
    name='role',
    description='добавить роль к реакции',
    options=[
        create_option(
            name='role',
            description='роль',
            required=True,
            option_type=8
        ),
        create_option(
            name='emoji',
            description='реакция-эмодзи',
            required=True,
            option_type=3,
        ),
        create_option(
            name='one_reaction',
            description='оставлять одну реакцию?',
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name='Одна',
                    value='one'
                ),
                create_choice(
                    name='Много',
                    value='many'
                )
            ]
        ),
        create_option(
            name='lever',
            description='использовать как переключатель?',
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name='Да',
                    value='Yes'
                ),
                create_choice(
                    name='Нет',
                    value='No'
                )
            ]
        )
    ]
)
@commands.has_permissions(administrator=True)
async def role(ctx, role, emoji, one_reaction, lever):
    with open(f'server data/{ctx.guild.id}-{ctx.guild.name}.json', 'r') as f:
        config = json.load(f)

    async for message in ctx.channel.history(limit=1, oldest_first=False):
        await message.add_reaction(emoji=emoji)

        message_id = str(message.id)
        channel_id = str(ctx.channel.id)

        if channel_id not in config['config']['data']['roles']:
            config['config']['data']['roles'][channel_id] = {}

        if message_id not in config['config']['data']['roles'][channel_id]:
            config['config']['data']['roles'][channel_id][message_id] = {}

        if emoji not in config['config']['data']['roles'][channel_id][message_id]:
            config['config']['data']['roles'][channel_id][message_id][emoji] = role.id, one_reaction

            emb = discord.Embed(
                title=f'({emoji} - {role}) добавлено',
                colour=10181046)
            message = await ctx.send(embed=emb)

        else:
            emb = discord.Embed(
                title=f'({emoji} - {role}) уже добавлено',
                colour=10181046)
            await ctx.send(embed=emb, hidden=True)

        with open(f'server data/{ctx.guild.id}-{ctx.guild.name}.json', 'w') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        await asyncio.sleep(1)
        await message.delete()

if __name__ == '__main__':
    bot.run(tocen)