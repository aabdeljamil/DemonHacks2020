import discord
import time

TOKEN = 'NzY5Mzg3ODIyMjY3NDk4NTA2.X5OSPw.waNaPotdxpLmBBgWA9OYsadOpRo' #deleted for security purposes
GUILD = "OreoShunment's Demonhack Server"

client = discord.Client()
defaultPoints = 10.0;

@client.event
async def on_ready():
    print('Running')

@client.event
async def on_message():
    if message.content.lower.startwith('add student') and message.author.role == 'Instrctor':
        print('Type student name.')
        lst = message.content.split()
        lst[2]
        name = lst[2]
        dict1[name] = defaultPoints
    
    
    
    
    
    
    
client.run(TOKEN)