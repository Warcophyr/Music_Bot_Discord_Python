import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
import asyncio
import nest_asyncio
nest_asyncio.apply()
from spotdl import Spotdl

BOT_TOKEN = "YOUR TOKEN"
CHANNEL_REPLAY = "Where the bot write"

yt_dl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {'options': "-vn"}

spotdl = Spotdl(client_id='your-client-id', client_secret='your-client-secret')

command_prefix = "$"
bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Hello! i'm ready!")
    # channel = bot.get_channel(CHANNEL_ID)
    # await channel.send("Hello! i'm ready!")

@bot.command()
async def play(ctx, url : str):
    '''
    $play link, bot dont have the queue yet
    '''
    channel = bot.get_channel(CHANNEL_REPLAY)
    if ctx.author.voice== None:
        await channel.send("join a channel")
        return
    
    # await channel.send("your song is start soon")
    if "https://" not in url:
        await  ctx.send("use a link from YouTube or Spotify")
        return
    
    if "list=" in url or "playlist" in url:
        await ctx.send("playlist link are not suported yet")
        return

    if "spotify" in url:
        # await ctx.send("spotify link are not suported yet")
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("wait the end of the song or $help to see other command")
            return
        
        await channel.send("your song is start soon")
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        try:
            await voiceChannel.connect()
        except Exception:
            pass

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        songs = spotdl.search([url])
        song = songs[0].name
        artis = songs[0].artist
        # # results = spotdl.download_songs(songs)
        sp_dw(songs)
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        return
    
    if "youtube" in url: 

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("wait the end of the song or $help to see other command")
            return
        
        await channel.send("your song is start soon")
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        try:
            await voiceChannel.connect()
        except Exception:
            pass
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

 
    
async def sp_dw(songs):
    path, song = spotdl.download(songs[0])
    return song

@bot.command()
async def pause(ctx):
    '''
    Pause the music at that specific time
    '''
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.pause()
    except Exception:
        await ctx.send("Currently no audio is playing.")

@bot.command()
async def resume(ctx):
    '''
    Resume the music at the time you have stop with the command $pause
    '''
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.resume()
    except Exception:
        await ctx.send("The audio is not paused.")

@bot.command()
async def stop(ctx):
    '''
    Disconnect the bot
    '''
    voice = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel)
    try:
        # await voice.disconnect()
        await ctx.voice_client.disconnect(force=True)
    except Exception:
        await ctx.send("The bot is not connected to a voice channel.")


bot.run(BOT_TOKEN)
