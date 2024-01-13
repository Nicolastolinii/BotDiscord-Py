import discord
from discord.ext import commands
from utils.bot_utils import setup_bot,typing
from command.command_handlers import *

# pybot\Scripts\activate

bot = setup_bot()
voice_context = {}
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
   
@bot.command(name="info",aliases=['informacion','i'], category='Info')
async def info(ctx, *, member: discord.Member):
    await info_command(ctx, member)
@bot.command(name='list', aliases=['l','playlist'])
async def playlist(ctx):
    await play_list(ctx)
@bot.command(name='volumen', aliases=['vol','v'])
async def change_volume(ctx, vol: float):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        if 0 <= vol <= 100:
            vol = vol / 100  # Discord.py utiliza valores de volumen entre 0 y 1
            if not isinstance(voice.source, discord.PCMVolumeTransformer):
                voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = vol
            embed_vol = discord.Embed(title="Volumen:", description=(f"Volumen ajustado {vol * 100}%"), color=0xff0000)
            await ctx.send(embed=embed_vol)
        else:
            await ctx.send('El volumen debe estar entre 0 y 100')
    else:
        await ctx.send('No se está reproduciendo nada actualmente.')
@bot.command(name='skip', aliases=['s'])
async def skip_song(ctx):
    global voice_context
    guild_id = ctx.guild.id
    voice_client = voice_context[guild_id]
    await skip_command(ctx,voice_client,bot)
@bot.command(name="start",aliases=['play','p'], category='music')
async def play(ctx):
    global voice_context
    guild_id = ctx.guild.id
    if ctx.author == bot.user:
                return
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if guild_id in voice_context and voice_context[guild_id].is_connected():
            await voice_context[guild_id].move_to(channel)
            voice_client = voice_context[guild_id]
        else:
            voice_context[guild_id] = await channel.connect()
            voice_client = voice_context[guild_id]
            # await ctx.channel.send(f'Joined {channel}')
    await play_song_command(ctx,voice_client,bot)

@bot.command(name='pause', aliases=['pa'])
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
    embed_pause = discord.Embed(title="Pause", description=(f"Requested by:{ctx.message.author.mention}"), color=0xff0000)
    await ctx.send(embed=embed_pause)

@bot.command(name='resume', aliases=['r'])
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
    embed_resume = discord.Embed(title="Resume", description=(f"Requested by:{ctx.message.author.mention}"), color=0xff0000)
    await ctx.send(embed=embed_resume)

@bot.command(name='disconnect', aliases=['dis','desconectar'])
async def disconnect(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        await voice.disconnect()
    else:
        await ctx.send("Nada que desconectar.")
    embed_disconnect = discord.Embed(title="Disconnect", description=(f"Requested by:{ctx.message.author.mention}"), color=0xff0000)   
    await ctx.send(embed=embed_disconnect)

@bot.command(name="clear",aliases=["limpiar","c"])
async def clear_play_list(ctx):
    await clear_list(ctx)

@bot.command(name="help",aliases=["h","ayuda"])
async def helper(ctx):
    embed_help=discord.Embed(title="**Helper**", color=0xff0000)
    embed_help.add_field(name="**Music**", value="**!play !p\n !playlist !list !l\n !skip !s\n !volumen !vol !v\n !pause !pa\n !resume !r\n disconnect !dis !desconectar\n !clear !limpiar !c**", inline=True)
    embed_help.add_field(name="**UserInfo**",value="**!informacion !info !i**")
    embed_help.set_footer(text=ctx.message.author.display_name)
    await typing(ctx,embed=embed_help,time=1)




bot.run('MTE5Mjk2ODU4NTQzNDM3MDA3OA.GNHbGF.kmIhYQqk82SE6Vo2RqgK256VQ9KLBRtdRpZrmg')