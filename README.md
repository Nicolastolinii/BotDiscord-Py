# Bot de Música para Discord

## Introducción
Este es un bot simple de Discord diseñado para reproducir música en canales de voz. El bot está construido utilizando [Discord.py](https://discordpy.readthedocs.io/) e incluye varios comandos relacionados con la música.

## Características
- Reproducir música en canales de voz
- Controlar el volumen
- Saltar canciones
- Pausar y reanudar la reproducción
- Desconectarse del canal de voz
- Mostrar información del usuario

## Pre-requisitos
Antes de ejecutar el bot, asegúrate de tener lo siguiente instalado:
- Python 3.7 o superior
- Biblioteca Discord.py (`pip install discord.py`)
- [python-decouple](https://pypi.org/project/python-decouple/) (`pip install python-decouple`)
- [FFmpeg](https://ffmpeg.org/download.html)

### Instalación de FFmpeg
Este bot utiliza FFmpeg para procesar y reproducir archivos de audio. Asegúrate de tener FFmpeg instalado en tu sistema antes de ejecutar el bot.

#### Windows
1. Descarga FFmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html).
2. Extrae el archivo zip descargado.
3. Agrega la ruta de la carpeta bin de FFmpeg al PATH del sistema.

#### Linux
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```
#### MacOS
```brew install ffmpeg```

Si ya tienes FFmpeg instalado, puedes omitir esta sección.

## Configuración
1. Crea un nuevo bot de Discord en el [Portal de Desarrolladores de Discord](https://discord.com/developers/applications).
2. Copia el token del bot.
3. Crea un archivo `.env` en el directorio del proyecto y agrega la siguiente línea:
DISCORD_TOKEN=TU_TOKEN_DEL_BOT
Reemplaza `TU_TOKEN_DEL_BOT` con el token que copiaste.
4. Guarda el archivo `.env`.

## Uso
1. Invita al bot a tu servidor de Discord utilizando el enlace de invitación generado en el Portal de Desarrolladores de Discord.
2. Ejecuta el bot usando el archivo `main.py` proporcionado.

## Comandos
- **!play (o !start o !p):** Reproducir música en el canal de voz actual.
- **!playlist (o !list o !l):** Mostrar la lista de reproducción actual.
- **!volumen (o !vol o !v):** Ajustar el volumen del bot (0-100).
- **!skip (o !s):** Saltar la canción actual.
- **!pause (o !pa):** Pausar la reproducción.
- **!resume (o !r):** Reanudar la reproducción.
- **!disconnect (o !dis o !desconectar):** Desconectar el bot del canal de voz.
- **!clear (o !limpiar o !c):** Limpiar la lista de reproducción actual.
- **!info (o !informacion o !i):** Mostrar información sobre un usuario.
- **!help (o !h o !ayuda):** Mostrar un mensaje de ayuda con todos los comandos disponibles.

## Contribuciones
Siéntete libre de contribuir al desarrollo de este bot enviando problemas o solicitudes de extracción.

 
