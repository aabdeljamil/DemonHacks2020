import discord
import asyncio
import time
import random

TOKEN = 'NzY5Mzg0MDg1MTM4ODMzNDM5.X5OOxA.qdPCzJQBdrGpUJxB2GE75XypAu0' #delete before pushing
GUILD = "OreoShunment's Demonhack Server"

client = discord.Client()

saveChnl = None
currentGuild = None
prefix = '!'
groupCreated = False
answerOptions = ['A', 'B', 'C', 'D']
groupRoles = []
groupVCs = []
groupTCs = []



@client.event
async def on_message(message):
    def check(reaction, user):
        emoji1 = discord.utils.get(message.author.guild.emojis, name='one')
        emoji2 = discord.utils.get(message.author.guild.emojis, name='two')
        emoji3 = discord.utils.get(message.author.guild.emojis, name='three')
        emoji4 = discord.utils.get(message.author.guild.emojis, name='four')
        return user == message.author and str(reaction.emoji) == emoji1 or emoji2 or emoji3 or emoji4

    global currentGuild
    global groupCreated
    global saveChnl
    global groupTCs
    global groupVCs
    global groupRoles
    
    if message.author == client.user: #don't want bot replying to itself
        return
    
    if message.content.lower().startswith(prefix + 'group create'):
        if any(role.name.lower() == 'staff' for role in message.author.roles):#check for 'instructor' role (required)
            targetVoiceChnl = message.author.voice.channel
            saveChnl = targetVoiceChnl
            listMbrsInVoiceChnl = targetVoiceChnl.members
            for i in range(len(listMbrsInVoiceChnl)-1):
                if listMbrsInVoiceChnl[i] == message.author:
                    del listMbrsInVoiceChnl[i]
                if any(role.name.lower() == 'staff' for role in listMbrsInVoiceChnl[i].roles):
                    del listMbrsInVoiceChnl[i]

            numStudentsInVoiceChnl = len(listMbrsInVoiceChnl)

            msgList = message.content.split()
            if len(msgList) != 3:
                await message.channel.send("Invalid usage!\nProper usage: '!group create <n>', where <n> is the max number of students that should be in a breakout group")
                return
            maxNumOfStudentsInGroup = int(msgList[2])

            if maxNumOfStudentsInGroup < 1:
                await message.channel.send('Must be a positive non-zero number')
                return
            
            if int(msgList[2]) > numStudentsInVoiceChnl:
                await message.channel.send('Number of students per group cannot be larger than total number of students')
                return

            numChnlsToCreate = numStudentsInVoiceChnl // maxNumOfStudentsInGroup
            remainder = numStudentsInVoiceChnl % maxNumOfStudentsInGroup
            every1Role = discord.utils.get(currentGuild.roles, name='@everyone')
            
            for i in range(numChnlsToCreate):
                group = 'Group'
                chnlName = group + str(i)
                roleName1 = group + str(i)
                ROLE = await currentGuild.create_role(name=roleName1)
                TXTCHNL = await currentGuild.create_text_channel(chnlName)
                VOICECHNL = await currentGuild.create_voice_channel(chnlName)
                groupRoles.append(ROLE)
                groupTCs.append(TXTCHNL)
                groupVCs.append(VOICECHNL)

                  
                for _ in range(maxNumOfStudentsInGroup):
                    rand = random.randint(0, numStudentsInVoiceChnl-1)
                    await listMbrsInVoiceChnl[rand].add_roles(ROLE)
                    del listMbrsInVoiceChnl[rand]
                    numStudentsInVoiceChnl -= 1


                await TXTCHNL.set_permissions(ROLE, read_messages=True, send_messages=True)
                await TXTCHNL.set_permissions(every1Role, read_messages=False, send_messages=False)

                await VOICECHNL.set_permissions(ROLE, connect=True)
                await VOICECHNL.set_permissions(every1Role, connect=False)

            if remainder != 0:
                k = 0
                for member in listMbrsInVoiceChnl:
                    await member.add_roles(groupRoles[k])
                    k += 1
            
            groupCreated = True

        else:
            await message.channel.send('Must be staff member')


    elif message.content.lower() == prefix + 'group delete':
        for groupVC in groupVCs:
            await groupVC.delete()
        for groupTC in groupTCs:
            await groupTC.delete()
        for groupRole in groupRoles:
            await groupRole.delete()

        groupTCs = []
        groupVCs = []
        groupRoles = []

        groupCreated = False

    elif message.content.lower() == prefix + 'group start':
        l = 0
        targetVoiceChnl = message.author.voice.channel
        saveChnl = targetVoiceChnl
        listMbrsInVoiceChnl = targetVoiceChnl.members
        for i in range(len(listMbrsInVoiceChnl)-1):
            if listMbrsInVoiceChnl[i] == message.author:
                del listMbrsInVoiceChnl[i]
            if any(role.name.lower() == 'staff' for role in listMbrsInVoiceChnl[i].roles):
                del listMbrsInVoiceChnl[i]

        if groupCreated:
            for groupVC in groupVCs:
                for mem in listMbrsInVoiceChnl:
                    grpName = 'group' + str(l)
                    if any(role.name.lower() == grpName for role in mem.roles):
                        await mem.move_to(groupVC)
                l += 1
        else:
            await message.channel.send('Groups never created\nRun "!group create <n>"')


    elif message.content.lower() == prefix + 'group end':
        for mem in currentGuild.members:
            if any(role.name.lower().startswith('group') for role in mem.roles):
                if mem.voice:
                    await mem.move_to(saveChnl)

        #delete all roles and channels that were created
        for groupVC in groupVCs:
            await groupVC.delete()
        for groupTC in groupTCs:
            await groupTC.delete()
        for groupRole in groupRoles:
            await groupRole.delete()

        groupTCs = []
        groupVCs = []
        groupRoles = []
        
        groupCreated = False


    elif message.content.lower() == prefix + 'poll':
        answers = []
        x = 4
        lstIndex = 0
        t_end = time.time() + 60
        await message.channel.send('Enter question')
        try:
            msg1 = await client.wait_for('message', timeout=30.0)
        except asyncio.TimeoutError:
            await message.channel.send('No response, poll cancelled')
        question = msg1.content
        while x > 0:
            msg = 'Enter option ' + answerOptions[lstIndex] + ", or enter 'end' to cancel poll"
            await message.channel.send(msg)
            try:
                msg2 = await client.wait_for('message', timeout=30.0)
                if msg2.content == 'end':
                    await message.channel.send('Poll cancelled')
                    return
                answers.append(msg2.content)
                lstIndex += 1
                x -= 1
            except asyncio.TimeoutError:
                await message.channel.send('No response, poll cancelled')
                return
        
        message1 = await message.channel.send('**Poll:**\n' + question + '\n\n:one:  ' + answers[0] + '\n:two:  ' + answers[1] + '\n:three:  ' + answers[2] + '\n:four:  ' + answers[3] + '\n\nPoll will end in 60 seconds' + '\nAnswer by reacting to this message with the corresponding emojis:') 
        await message1.add_reaction('1️⃣')
        await message1.add_reaction('2️⃣')
        await message1.add_reaction('3️⃣')
        await message1.add_reaction('4️⃣')

        while time.time() < t_end:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=35.0, check=check)
            except asyncio.TimeoutError:
                pass

        await message.channel.send('Poll ended')


    elif message.content.lower() == prefix + 'question':
        return
@client.event
async def on_ready():
    for guild1 in client.guilds:
        if guild1.name == GUILD:
            global currentGuild
            currentGuild = guild1
            break
    print(client.user, 'connected to guild ', currentGuild.name, '#', currentGuild.id)

client.run(TOKEN)