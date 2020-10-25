import discord
import asyncio
import time
import sched

TOKEN = 'NzY5Mzg3MTk3NDEyODAyNjAw.X5ORqg.Rg1WVAakHEKO1-NzhOhbD1XbQXQ'
GUILD = "OreoShunment's Demonhack Server"
client = discord.Client()
classlist = []
isLecture = True


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(client.user, 'connected to guild ', guild.name, '#', guild.id)



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    prefix = "!"
    possCommand = (message.content.lower()).split(None, 1)

    if possCommand[0] == (prefix + "checkin"):
        if any(role.name.lower() == 'student' for role in message.author.roles):
            if isLecture:
                if message.author not in classlist:
                    classlist.append(message.author.name)
                    await message.channel.send("Checked in.", delete_after=10.0)
                else:
                    await message.channel.send("Already checked in", delete_after=10.0)
            else:
                await message.channel.send("Lecture has not started.")
        else:
            await message.channel.send("!checkin is for students only.")

    if possCommand[0] == (prefix + "attendance"):
        if any(role.name.lower() == 'staff' for role in message.author.roles):
            if not isLecture:
                attendancelist = ""
                for student in classlist:
                    print(student)
                    attendancelist = attendancelist + student + "\n"
                await message.channel.send(attendancelist + "End of list.")
            else:
                await message.channel.send("Lecture has not ended.")
        else:
            await message.channel.send("!attendance is for instructors only.")











client.run(TOKEN)

