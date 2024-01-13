import discord
from discord.ext import commands
import yt_dlp as youtube_dl
from youtubesearchpython import VideosSearch
import asyncio


def setup_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents ,help_command=None)
    return bot
async def typing(ctx, embed=None,time:int=2):
    async with ctx.typing():
        await asyncio.sleep(time)

    if embed:
        await ctx.send(embed=embed)

async def search_yt(item):
    if item.startswith("https://"):
        with youtube_dl.YoutubeDL({'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'ytsearch',
                'source_address': '0.0.0.0',}) as ydl:
            info = ydl.extract_info(item, download=False)
            title = info['title']
        return {'source': item, 'title': title,'img': info['formats'][0]['url'],'duration':info['formats'][0]['fragments'][0]['duration'] }
    else:
        search = VideosSearch(item, limit = 5)  # Realiza una búsqueda de videos con el nombre de la canción y obtiene hasta 5 resultados
        results = search.result().get('result', [])  # Obtiene todos los resultados de la búsqueda
        formatted_results = [{'source': video["link"], 'title': video["title"],'duration': video["duration"],'img': video["thumbnails"][0]["url"]} for video in results]  # Formatea los resultados
        return formatted_results  # Devuelve la lista de resultados para que puedas elegir uno
