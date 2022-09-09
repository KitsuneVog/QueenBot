import json
import os

async def guild_join(bot, guild):
    print(f'Бота {bot.user} подключили к серверу {guild}')
    file = open(f'server data/{guild.id}-{guild.name}.json', 'w+')
    file.write('{}')
    file.close()

    with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
        config = json.load(f)

    config['config'] = {}

    config['config']['rules'] = {}
    config['config']['rules']['status'] = ''
    config['config']['rules']['channels'] = []

    config['config']['levels'] = {}
    config['config']['levels']['status'] = ''
    config['config']['levels']['channels'] = []

    config['config']['news'] = {}
    config['config']['news']['status'] = ''
    config['config']['news']['channels'] = []

    config['config']['photo'] = {}
    config['config']['photo']['status'] = ''
    config['config']['photo']['channels'] = []

    config['config']['check'] = {}
    config['config']['check']['status'] = ''
    config['config']['check']['channels'] = []

    config['config']['passage'] = {}
    config['config']['passage']['status'] = ''
    config['config']['passage']['channels'] = []

    config['config']['skills'] = {}
    config['config']['skills']['status'] = ''
    config['config']['skills']['channels'] = []

    config['config']['colors'] = {}
    config['config']['colors']['status'] = ''
    config['config']['colors']['channels'] = []

    config['config']['games'] = {}
    config['config']['games']['status'] = ''
    config['config']['games']['channels'] = []

    config['config']['data'] = {}
    config['config']['data']['roles'] = {}

    with open(f'server data/{guild.id}-{guild.name}.json', 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

async def guild_update(before, after):
    os.rename(f'{before.id}-{before.name}.json', f'{after.id}-{after.name}.json')
    print(f'{before.name} - теперь {after.name}')

async def guild_remove(bot, guild):
    print(f'Бота {bot.user} отключили от сервера {guild}')
    os.remove(f'server data/{guild.id}-{guild.name}.json')