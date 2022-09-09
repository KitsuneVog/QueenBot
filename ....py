@commands.has_permissions(administrator=True)
async def add(ctx, function, action=None, status=None):
    guild = ctx.guild
    with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
        config = json.load(f)

    if action == 'add':
        if function == 'skills' or function == 'colors' or function == 'games':
            config['config'][function]['channels'].append(ctx.channel.id)
            config['config'][function]['channels'] = list(set(config['config'][function]['channels']))

            emb = discord.Embed(title=f'{function.upper()}', colour=10181046)
            if function == 'skills':

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

            if function == 'colors':
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

            if function == 'games':
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

        else:
            config['config'][function]['channels'].append(ctx.channel.id)
            config['config'][function]['channels'] = list(set(config['config'][function]['channels']))

            if function == 'rules':
                async for message in ctx.channel.history(limit=1, oldest_first=False):
                    emb = discord.Embed(
                        title=f'Теперь в канал -__{ctx.channel.name}__- добавлена функция {function}\nФункция __{function}__ **включена**',
                        colour=10181046)
                    await ctx.send(embed=emb, hidden=True)

                    await message.add_reaction(emoji='✅')

    elif action == 'delete':
        with open(f'server data/{guild.id}-{guild.name}.json', 'r') as f:
            config = json.load(f)

        if function == 'rules':
            for message in ctx.message.channel.history(limit=1, oldest_first=False):
                await message.clear_reactions()
            config['config'][function] = None

        else:
            config['config'][function]['channels'].remove(ctx.channel.id)
            config['config'][function]['channels'] = list(set(config['config'][function]['channels']))

        emb = discord.Embed(title=f'Теперь канал -__{ctx.channel.name}__- удалён из {function}', colour=10181046)
        await ctx.send(embed=emb, hidden=True)

        if status != None:
            config['config'][function]['status'] = status

            if status == 'on':
                emb = discord.Embed(title=f'Теперь функция __{function}__ **включена**', colour=10181046)
            else:
                emb = discord.Embed(title=f'Теперь функция __{function}__ **выключена**', colour=10181046)
            await ctx.send(embed=emb, hidden=True)

    with open(f'server data/{guild.id}-{guild.name}.json', 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)