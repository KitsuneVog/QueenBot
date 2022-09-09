import discord

async def command():

    if command == 'sayM':
        user = await bot.fetch_user(console[1])

        content = ' '.join(console[2:])
        emb = discord.Embed(title=content, colour=10181046)
        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

        await user.send(embed=emb)