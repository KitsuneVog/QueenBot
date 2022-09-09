import discord

async def help(ctx):
    emb = discord.Embed(title='', colour=10181046)

    emb.add_field(name='**Help**',
                  value='Используйте /help <команда> чтобы узнать информацию о команде.',
                  inline=False)

    emb.add_field(name='_**Участник**_',
                  value='help \nlvl',
                  inline=False)

    emb.add_field(name='_**Модерация**_',
                  value='info \nclear',
                  inline=True)

    emb.add_field(name='_**Администрация**_',
                  value='add \ndelete \nlever \ndeletion',
                  inline=True)

    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb, hidden=True)

async def help_info(ctx):
    emb = discord.Embed(title='**HELP**', description='Присылает список всех команд', colour=10181046)

    emb.add_field(name='**Написание**',
                  value='/help',
                  inline=False)

    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb, hidden=True)

async def lvl_info(ctx):
    emb = discord.Embed(title='**LVL**', description='Присылает карточку с информацией о вас', colour=10181046)

    emb.add_field(name='**Написание**',
                  value='/lvl',
                  inline=False)

    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb, hidden=True)

async def info_info(ctx):
    emb = discord.Embed(title='**INFO**', description='Присылает карточку с информацией об указанном пользователе', colour=10181046)

    emb.add_field(name='**Написание**',
                  value='/info <упоминание>',
                  inline=False)

    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb, hidden=True)

async def deletion_info(ctx):
    emb = discord.Embed(title='**DELETION**', description='Обнуляет (rank,lvl,exp) до нуля', colour=10181046)

    emb.add_field(name='**Написание**',
                  value='/deletion <упоминание>',
                  inline=False)

    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb, hidden=True)

async def clear_info(ctx):
    emb = discord.Embed(title='**CLEAR**', description='Удаляет последние <число> сообщений. Если не указывать <число> удалит 100 сообщений', colour=10181046)

    emb.add_field(name='**Написание**',
                  value='/clear _<число>_',
                  inline=False)

    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb, hidden=True)

async def add_info(ctx):
    emb = discord.Embed(title='**ADD**', description='Добавляет в данный канал <функция>(функцию)', colour=10181046)

    emb.add_field(name='**Написание**',
                  value='/add <функция>',
                  inline=False)

    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb, hidden=True)

async def delete_info(ctx):
    emb = discord.Embed(title='**DELETE**', description='Удаляет <функция>(функцию) из данного канала', colour=10181046)

    emb.add_field(name='**Написание**',
                  value='/delete <функция>',
                  inline=False)

    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb, hidden=True)

async def lever_info(ctx):
    emb = discord.Embed(title='**LEVER**', description='Включает/Выключает функцию на сервере', colour=10181046)

    emb.add_field(name='**Написание**',
                  value='/lever <функция> <статус>',
                  inline=False)

    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb, hidden=True)