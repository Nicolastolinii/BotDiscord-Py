import discord
from utils.bot_utils import search_yt,typing
import yt_dlp as youtube_dl
import asyncio

queue = []  # Cola de reproducción global
options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -loglevel error' # Opciones antes de iniciar la reproducción
}
# info user
async def info_command(ctx, member): 
    roles = ' '.join([f'<@&{role.id}>' for role in member.roles])
    joined_date = member.joined_at.strftime("%Y-%m-%d -- %H:%M:%S")
    if member.public_flags.__bool__:
            account_status = "True."
    else:
            account_status = "False."
    embed = discord.Embed(title="User Information", description=None, color=0x2e6a64)
    embed.add_field(name="Username", value=member.display_name, inline=True).set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True).add_field(name="Status", value=member.status)
    embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d -- %H:%M:%S"), inline=False)
    embed.add_field(name="Joined Server At", value=joined_date, inline=True)
    embed.add_field(name="In Mobile", value=member.is_on_mobile(),inline=False)
    embed.add_field(name="Roles", value=roles,inline=False)
    embed.add_field(name="Bot", value=member.bot,inline=True)
    embed.add_field(name="Verified", value=account_status,inline=True)
    await typing(ctx,embed=embed,time=1)
# funcion para reproducir la url
async def play_next(ctx,voice,bot):
    global queue
    print(f'LISTA ANTES DEL DURANTE Y ANTES DE LA LOGICA:{queue}')

    if len(queue) > 0:
        song = queue.pop(0)
        try:
            
                with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
                    info = ydl.extract_info(song['source'], download=False)
                    url = info['url']
                def after_playing(e):
                    asyncio.run_coroutine_threadsafe(play_next(ctx, voice,bot), bot.loop)
                await typing(ctx)
                voice.play(discord.FFmpegPCMAudio(url, **options), after=after_playing)
                embed_now_playing = discord.Embed(title="Now Playing", description=f"[{song['title']}]({song['source']})\nRequested by: {ctx.message.author.mention}", color=0xff0000).set_thumbnail(url=song['img'])
                embed_now_playing.add_field(name="Duracion", value=song["duration"])
                await typing(ctx,embed_now_playing,2)
        except Exception as e:
                print(e)
                await ctx.channel.send(f'No se pudo reproducir la canción.{e}')
# reproduce la cola de las canciones si es que las hay 
async def play_song_command(ctx,voice,bot):
    """
     Esta función maneja la reproducción de canciones, ya sea buscando o agregando enlaces a la cola.
     Utiliza funciones como search_yt y typing para interactuar con la cola y enviar mensajes.
     Puedes personalizar esto según tus necesidades."""
    global queue
    if ctx.message.content.startswith('!play'):
        search_term = ctx.message.content[6:].strip()  # Obtén el término de búsqueda de la canción
    if ctx.message.content.startswith('!p'):
         search_term = ctx.message.content[3:].strip()
    
    result = await search_yt(search_term)
    if result:
        try:
            if search_term.startswith("https://"):
                # Manejar el caso del enlace directo
                queue.append(result)  # Agregar el enlace a la cola directamente
                if len(queue) == 1 and not voice.is_playing():
                    await play_next(ctx, voice,bot)
                else:
                    embed_queue = discord.Embed(title="Add PlayList", description=f"[{queue[-1]['title']}]({queue[-1]['source']})\nRequested by: {ctx.message.author.mention}", color=0xff0000).set_thumbnail(url=queue[-1]['img'])
                    await ctx.channel.purge(limit=1)  # Borra el mensaje original
                    await typing(ctx,embed_queue,1)
            else:
                embed = discord.Embed(title="Result:", description=None, color=0x2e6a64)
                for i, res in enumerate(result[:5]):
                    embed.add_field(name="\u200b", value=(f"{i+1}. {res['title']}"), inline=False)
                await typing(ctx,embed,2)
                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                selection = await bot.wait_for('message', check=check, timeout=70)
                choice = int(selection.content) - 1
                if 0 <= choice < 5:
                    selected_source = result[choice]['source']
                    if selected_source.startswith("https://"):
                        queue.append(result[choice])
                        if len(queue) == 1 and not voice.is_playing():
                            await play_next(ctx, voice,bot)
                        else:
                            embed_queue = discord.Embed(title="Add PlayList", description=queue[-1]['title'], color=0xff0000)
                            await typing(ctx,embed,1)
                    else:    
                        await ctx.channel.send('No se encontró la canción.')
                else:
                    await ctx.channel.send('Por favor, elige un número del 1 al 5.')
        except asyncio.TimeoutError:
            await ctx.channel.send('Tiempo de espera agotado. Inténtalo de nuevo.')
    else:
        await ctx.channel.send('No se encontraron resultados para la búsqueda o se proporcionó un enlace directo inválido.')
# muestra la lista de reproduccion si es existente
async def play_list(ctx):
    """Esta función muestra la lista de reproducción actual, si existe.
     Utiliza un objeto Embed de Discord para dar formato a la lista y enviarla al canal."""
    global queue
    if not queue:
        await ctx.send("La lista de reproducción está vacía.")
        return
    embed_list = discord.Embed(title="PlayList",description=None , color=0xff0000)
    for i, song in enumerate(queue):
            title = song.get('title', 'Desconocido')
            duration = song.get('duration', 'Desconocida')

            embed_list.add_field(
                name=f"{i+1}. {title}",
                value=f"Duración: {duration}",
                inline=False
            )
  

    await ctx.send(embed=embed_list)
# para a la siguiente cancion
async def skip_command(ctx, voice, bot):
    if voice.is_playing() and len(queue) > 0:
        voice.stop()
        print(f'LISTA ANTES DEL SKIP:{queue}')
        await play_next(ctx, voice, bot)
        print(f'LISTA ANTES DEL DESPUES:{queue}')

    else:
        await ctx.channel.send('No hay canciones en la lista para saltar.')
# limpia la lista de reproduccion
async def clear_list(ctx):
     queue.clear()
     await ctx.send("PlayList Clear")