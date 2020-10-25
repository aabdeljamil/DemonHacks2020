import discord
import asyncio
import time
import sched

TOKEN = 'NzY5Mzg3MTk3NDEyODAyNjAw.X5ORqg.RCdGYZR23G4wMdP3K_ce5ewJFxM'
GUILD = "OreoShunment's Demonhack Server"
client = discord.Client()
classlist = []
isLecture = False
currentGuild = None

async def MuteAll(flag): # flag is True to mute, False to unmute
	global currentGuild
	if currentGuild == None:
		print("Not part of a guild")
		return
	for memb in currentGuild.members:
		if any(role.name.lower() == "student" for role in memb.roles) or len(memb.roles) == 1:
			if flag:
				classlist[memb] = 0
				await memb.edit(mute = True)
			else:
				classlist.pop(memb)
				await memb.edit(mute = False)



@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            global currentGuild
            currentGuild = guild
            break
    print(client.user, 'connected to guild ', guild.name, '#', guild.id)



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    prefix = "!"
    possCommand = (message.content.lower()).split(None, 1)

    if possCommand[0] == (prefix + "lecture"):  # command is !lecture
        if any(role.name.lower() == "student" for role in message.author.roles) or len(message.author.roles) == 1:
            await message.channel.send("You do not have permission to use the command '!lecture'", delete_after=10.0)
            return
        if len(possCommand) <= 1:
            await message.channel.send("Incorrect usage of '!lecture'\nproper usage is '!lecture (on/off)'",
                                       delete_after=20.0)
            return
        global isLecture
        if possCommand[1] == "on":
            if not isLecture:
                isLecture = True
                await MuteAll(True)
                await message.channel.send("Lecture is now in session", delete_after=10.0)
            else:
                await message.channel.send("Lecture is already active", delete_after=10.0)
        elif possCommand[1] == "off":
            if isLecture:
                isLecture = False
                await MuteAll(False)
                await message.channel.send("Lecture has concluded", delete_after=10.0)
            else:
                await message.channel.send("Lecture is already inactive", delete_after=10.0)
        else:
            await message.channel.send("Incorrect usage of '!lecture'\n\tproper usage is '!lecture (on/off)'",
                                       delete_after=20.0)
        return

    if possCommand[0] == (prefix + "checkin"):
        if any(role.name.lower() == 'student' for role in message.author.roles):
            if isLecture:
                if message.author not in classlist:
                    classlist.append(message.author.nick)
                    await message.channel.send("Checked in.", delete_after=10.0)
                else:
                    await message.channel.send("Already checked in", delete_after=10.0)
            else:
                await message.channel.send("Lecture has not started.")
        else:
            await message.channel.send("!checkin is for students only.")
        return

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
        return










client.run(TOKEN)

