import os,sys,subprocess
import asyncio
import urllib

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

libs = []

try:
    from apafy import pafy
except Exception as e:
    print(e)
    libs.append('youtube_dl')
    libs.append('apafy==0.5.6.1')

try:
    import discord
    from discord import FFmpegPCMAudio, PCMVolumeTransformer
    from discord.ext import commands, tasks
except Exception as e:
    print(e)
    libs.append('discord.py')
    libs.append('discord.py[voice]')


if (len(libs) > 0):
    libs.append('ffmpeg')
    for x in libs:
        install(x)
    sys.exit('Restart')


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}




@client.event
async def on_ready():
    print("Ti cho kibersportsmen?!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/silikonovieRoma"))

@client.command()
async def leaveRoma(ctx):
    if int(ctx.author.id) != 249287459672686593:
        voicetrue = ctx.author.voice
        mevoicetrue = ctx.guild.me.voice
        if voicetrue is None:
                return await ctx.send('You are not currently in the same voice channel as I am.')
        if mevoicetrue is None:
                return await ctx.send('Im not currently in any voice channel!')
        await ctx.voice_client.disconnect()


@client.command()
async def silikonovieRoma(ctx):
        if ctx.message.author.voice == None:
            await ctx.send("You need to be in a voice channel to use this command!")
            return
        channel = ctx.message.author.voice.channel
        print('Connecting to channel')
        voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        print('Getting voice channel')
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice_client == None:
            voice_client = await voice.connect()
        else:
            await voice_client.move_to(channel)
        print('Connected!')
        print('Getting song from yt')
        song = pafy.new("https://www.youtube.com/watch?v=9tYgaFMwodM")  
        audio = song.getbestaudio() 
        print('Song parsed')
        source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  
        print('play song')
        voice_client.play(source) 



client.run(str(input("INPUT_TOKEN: ")))
