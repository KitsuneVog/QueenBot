import discord
import json

async def message_lvl(bot, guild, message):
    user = message.author

    try:
        print(f'{guild.name}: [{message.created_at}]\n  {user}\n       --{message.content}')
    except UnicodeEncodeError:
        pass

    with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
        config = json.load(f)

    if config['config']['check']['status'] == 'on':
        if not message.content.startswith('.play') and not message.content.startswith('=play'):
            if '://' in message.content:
                emb = discord.Embed(title='ссылка на сообщение', url=message.jump_url, colour=10181046)
                emb.set_author(name=user.name, icon_url=user.avatar_url)
                emb.add_field(name='Сообщение', value=message.content, inline=False)

                for id in config['config']['check']['channels']:
                    channel = bot.get_channel(id)
                    await channel.send(embed=emb)


    async def create_role(name, action):
        role = discord.utils.get(user.guild.roles, name=name)
        if role not in guild.roles:
            await guild.create_role(name=name)

        role = discord.utils.get(user.guild.roles, name=name)
        if role in guild.roles:
            if action == 'add':
                await user.add_roles(role)
            elif action == 'remove':
                await user.remove_roles(role)


    async def update_data(config, user_id):
        if not user_id in config:
            config[user_id] = {}
            config[user_id]['exp'] = 0
            config[user_id]['lvl'] = 0
            config[user_id]['rank'] = 0
            config[user_id]['warn'] = 0


    async def add_exp(config, user_id, exp):
        if message.channel.id in config['config']['levels']['channels'] or config['config']['levels']['status'] == 'off':
            pass
        else:
            config[user_id]['exp'] += exp


    async def add_lvl(config, user_id):
        exp = config[user_id]['exp']
        lvl = config[user_id]['lvl']

        if exp >= lvl:
            config[user_id]['exp'] = 0
            config[user_id]['lvl'] += 1

            if lvl + 1 > 1:
                await create_role(f'Уровень {lvl + 1}', 'add')

                await create_role(f'Уровень {lvl}', 'remove')

                await create_role('Новичок', 'remove')


    async def add_rank(config, user_id):
        lvl = config[user_id]['lvl']
        rank = config[user_id]['rank']

        if lvl == 10:
            config[user_id]['exp'] = 0
            config[user_id]['lvl'] = 0
            config[user_id]['rank'] += 1
            try:
                emb = discord.Embed(title=f'**Профиль {message.author}**', colour=10181046)
                emb.add_field(name=f'Достиг уровня 10 на сервере {user.guild.name}', value=f'теперь ваш ранг = {rank + 1}',
                              inline=True)
                await user.send(embed=emb)
            except discord.errors.Forbidden:
                pass

            await create_role('Уровень 1', 'add')

            await create_role(f'Звание {rank + 1}', 'add')

            await create_role('Уровень 10', 'remove')

            if rank != 0:
                await create_role(f'Звание {rank}', 'remove')

    if not message.channel.id in config['config']['levels']['channels'] and config['config']['levels']['status'] == 'on':
        await update_data(config, str(user.id))
        await add_exp(config, str(user.id), 0.1)
        await add_lvl(config, str(user.id))
        await add_rank(config, str(user.id))

        with open(f'server data/{guild.id}-{guild.name}.json', 'w') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

# канал только с изображениямиб, ссылками и ответами
    with open(f'server data/{message.guild.id}-{message.guild.name}.json', 'r') as f:
        config = json.load(f)

    if message.channel.id in config['config']['photo']['channels'] and config['config']['photo']['status'] == 'on':
        if len(message.attachments) > 0 and message.attachments[0].url.split('.')[-1].lower() in ['png', 'jpg', 'gif', 'jpeg'] or '://' in message.content:
                emoji = '👍'
                await message.add_reaction(emoji)
                emoji = '👎'
                await message.add_reaction(emoji)
        elif message.reference != None:
            pass
        else:
            await message.delete()

# канал с опросом
    if message.channel.id in config['config']['news']['channels'] and config['config']['news']['status'] == 'on':
        if message.content.startswith('Опрос') or message.content.startswith('опрос') or message.content.startswith('**опрос') or message.content.startswith('**Опрос'):
            emoji = '1️⃣'
            await message.add_reaction(emoji)
            emoji = '2️⃣'
            await message.add_reaction(emoji)

    await bot.process_commands(message)