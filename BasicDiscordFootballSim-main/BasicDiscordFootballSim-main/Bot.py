# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
# Made with Aaron D Cunha - https://github.com/AaronDcunha
import discord
import asyncio
import random
import yaml
import OvrCalculator as Data
from discord.ext import commands
import io
import nest_asyncio
nest_asyncio.apply()

#VARIABLES
GoalData = {}
AssistData = {}

GameOn = False

#Game Functions
async def AddTally(Player):
    global GoalData
    if Player in GoalData.keys():
        GoalData[Player] = GoalData[Player] + 1
    else:
        GoalData[Player] = 1
    
def SaveTally():
    global GoalData
    global AssistData
    print("SAVING")
    #print(GoalData)
    with open('GoalTally.yml', 'w') as file:
        yaml.dump(GoalData, file)
    with open('AssistTally.yml','w') as file:
        yaml.dump(AssistData,file)
        
async def AddAssist(Player):
    global AssistData
    if Player in AssistData.keys():
        AssistData[Player] = AssistData[Player] + 1
    else:
        AssistData[Player] = 1

def GetTopScorer():
    global GoalData
    sort = sorted(GoalData.items(), key=lambda x:x[1])
    sort = reversed(sort)
    string = ""
    for i in sort:
        string += str(i[0]) + ": " + str(i[1]) + "\n"
    print(string)
    return string

def GetTopAssist():
    global AssistData
    sort = sorted(AssistData.items(), key=lambda x:x[1])
    sort = reversed(sort)
    string = ""
    for i in sort:
        string += str(i[0]) + ": " + str(i[1]) + "\n"
    print(string)
    return string

def getAssister(players, scorer):
    Coefficients={
        "F" : 6,
        "M" : 4,
        "D" : 1
        }
    biasedList = []
    for p in players.keys():
        if p != scorer and len(players[p]) > 1:
            for i in range(Coefficients[players[p][0]]):
                biasedList.append(p)
    return biasedList[random.randint(0,len(biasedList)-1)]

def getGA():
    global AssistData
    global GoalData
    ga = {k: GoalData.get(k, 0) + AssistData.get(k, 0) for k in set(GoalData) | set(AssistData)}
    sort = sorted(ga.items(), key=lambda x:x[1])
    sort = reversed(sort)
    string = ""
    for i in sort:
        string += str(i[0]) + ": " + str(i[1]) + "\n"
    print(string)
    return string
    
def getRandomPlayer(team,owngoal):
    rand = random.random()
    if owngoal == False:
        if rand <= 0.75:
            lst = Data.GetPlayersByPosition(team, "F")
            return lst[random.randint(0,len(lst)-1)]
        elif rand <= 0.95:
            lst = Data.GetPlayersByPosition(team, "M")
            return lst[random.randint(0,len(lst)-1)]
        elif rand <= 0.99:
            lst = Data.GetPlayersByPosition(team, "D")
            return lst[random.randint(0,len(lst)-1)]
        else:
            lst = Data.GetPlayersByPosition(team, "G")
            return lst[random.randint(0,len(lst)-1)]
    else:
        if rand <= 0.01:
            lst = Data.GetPlayersByPosition(team, "F")
            return lst[random.randint(0,len(lst)-1)]
        elif rand <= 0.05:
            lst = Data.GetPlayersByPosition(team, "M")
            return lst[random.randint(0,len(lst)-1)]
        elif rand <= 0.9:
            lst = Data.GetPlayersByPosition(team, "D")
            return lst[random.randint(0,len(lst)-1)]
        else:
            lst = Data.GetPlayersByPosition(team, "G")
            return lst[random.randint(0,len(lst)-1)]
        

def DisplayPenScore(team1,score1,team2,score2):
    return str(team1 + " " + " ".join(str(e) for e in score1) + " : " + " ".join(str(e) for e in score2) + " " + team2)

async def Game(team1,team2,mode,homeAdv):
    global GameOn
    if Data.GetTeam(team1) == None or Data.GetTeam(team2) == None:
        GameOn = False
        return False
    GameOn = True
    Team1 = Data.GetTeam(team1)
    Team2 = Data.GetTeam(team2)
    if mode != "pens":
        T1 = Team1[0]
        T2 = Team2[0]
         
        AtkChanceTeam1 = (0.40 * T1["Att"]) + (0.40 * T1["Pas"]) + (0.20*T1["Dri"])
        AtkChanceTeam2 = (0.40 * T2["Att"]) + (0.40 * T2["Pas"]) + (0.20*T2["Dri"])
        
        DefChanceTeam1 = (0.4 * ((0.6*T1["Def"])+(0.4*T1["Phy"]))) + (0.6 * T1["Gk"])
        DefChanceTeam2 = (0.4 * ((0.6*T2["Def"])+(0.4*T2["Phy"]))) + (0.6 * T2["Gk"])
        
        ChanceTeam1 = 0
        ChanceTeam2 = 0  
        GoalChanceTeam1 = 0
        GoalChanceTeam2 = 0
        
        if homeAdv == True:
            ChanceTeam1 = random.randint(4 + round(max(1,((T1["Pas"] - T2["Def"]) / 4.5))),9 + round(max(1,((T1["Pas"] - T2["Def"]) / 4.5))))
            ChanceTeam2 = random.randint(4 + round(max(1,((T2["Pas"] - T1["Def"]) / 5))),7 + round(max(1,((T2["Pas"] - T1["Def"]) / 5))))  
            GoalChanceTeam1 = (AtkChanceTeam1 + max(0,(AtkChanceTeam1-DefChanceTeam2)/2)) / ((DefChanceTeam2 + max(0,(DefChanceTeam2-DefChanceTeam1)/2)) * 4.25)
            GoalChanceTeam2 = (AtkChanceTeam2 + max(0,(AtkChanceTeam2-DefChanceTeam1)/2)) / ((DefChanceTeam1+ max(0,(DefChanceTeam1-DefChanceTeam2)/2)) * 5)
        else:
            ChanceTeam1 = random.randint(3 + round(max(1,((T1["Pas"] - T2["Def"]) / 4))),7 + round(max(1,((T1["Pas"] - T2["Def"]) / 4))))
            ChanceTeam2 = random.randint(3 + round(max(1,((T2["Pas"] - T1["Def"]) / 4))),7 + round(max(1,((T2["Pas"] - T1["Def"]) / 4))))
            GoalChanceTeam1 = (AtkChanceTeam1 + max(0,(AtkChanceTeam1-DefChanceTeam2)/2)) / ((DefChanceTeam2 + max(0,(DefChanceTeam2-DefChanceTeam1)/2)) * 4.25)
            GoalChanceTeam2 = (AtkChanceTeam2 + max(0,(AtkChanceTeam2-DefChanceTeam1)/2)) / ((DefChanceTeam1+ max(0,(DefChanceTeam1-DefChanceTeam2)/2)) * 4.25)


        
        """print("+++")
        print(team1)
        print(ChanceTeam1,GoalChanceTeam1,DefChanceTeam1)
        print("++++")
        print(team2)
        print(ChanceTeam2,GoalChanceTeam2,DefChanceTeam2)"""
        
        T1Goal = 0
        T2Goal = 0
        Commentary = []
        GoalMessage = [
            "HAS SCORED!!",
            "HAS SCORED!!",
            "HAS SCORED!!",
            "takes the chance... AND ITS IN!!!!",
            "SCORES!!!",
            "SCORES!!!",
            "HAS SCORED!!",
            "takes the chance... AND ITS IN!!!!",
            "SCORES!!!",
            "SCORES!!!",
            "SCORES!!!",
            "SCORES!!!",
            "SCORES!!!",
            "SCORES!!!",
            "SCORES!!!",
            "takes the chance... AND ITS IN!!!!",
            "takes the chance... AND ITS IN!!!!",
            "HAS SCORED!!",
            "HAS SCORED!!",
            "HAS SCORED!!",
            "HAS SCORED!!",
            "WINS A PENALTY! AND SCORES!",
            "WINS A PENALTY! AND SCORES!",
            "SCORES!! There was no saving that!",
            "SCORES!! There was no saving that!",
            "#SCORED AN OWN GOAL!! OH MY!",
            ", YOU BEAUTY!!! WHAT A GOAL!",
            ", YOU BEAUTY!!! WHAT A GOAL!",
            ", YOU BEAUTY!!! WHAT A GOAL!",
            "strikes and nails it right in the top corner!",
            "strikes and nails it right in the top corner!",
            "strikes and nails it right in the top corner!",
            "has got 30 yards of space and he's going for it! AND HE SCORES!",
            "has got 30 yards of space and he's going for it! AND HE SCORES!",
            "has got 30 yards of space and he's going for it! AND HE SCORES!",
            "HAS SCORED A GOAL OF THE HIGHEST QUALITY!!!! WHAT A STRIKE!!",
            "HAS SCORED A GOAL OF THE HIGHEST QUALITY!!!! WHAT A STRIKE!!",
            "HAS SCORED A GOAL OF THE HIGHEST QUALITY!!!! WHAT A STRIKE!!",
            "is the man on the mission and he's going for it! AND HE SCORES!",
            "is the man on the mission and he's going for it! AND HE SCORES!",
            "is the man on the mission and he's going for it! AND HE SCORES!",
            "has made the goalkeeper look silly! What a goal!",
            "has made the goalkeeper look silly! What a goal!",
            "has made the goalkeeper look silly! What a goal!",
            "CANNOT BE STOPPED! WHAT A SHOT!",
            "CANNOT BE STOPPED! WHAT A SHOT!",
            "CANNOT BE STOPPED! WHAT A SHOT!",
            "with a cheeky finish from the edge of the box!",
            "with a cheeky finish from the edge of the box!",
            "with a cheeky finish from the edge of the box!",
            "HITS THE BAR BUT GETS LUCKY! IT'S IN!",
            "HITS THE BAR BUT GETS LUCKY! IT'S IN!",
            "HITS THE BAR BUT GETS LUCKY! IT'S IN!",
            ", IT HAD TO BE HIM! WHAT A GOAL!",
            ", IT HAD TO BE HIM! WHAT A GOAL!",
            ", IT HAD TO BE HIM! WHAT A GOAL!",
            "can't miss!!",
            "can't miss!!",
            "can't miss!!"
            
            ]
        #THe "#" indicates that the opposite team player has to be used
        MissMessage = [
            "takes the shot... and misses.",
            "takes the shot... and misses.",
            "takes the shot... and misses.",
            "takes the shot... and misses.",
            "misses an open goal! Wow, what a miss.",
            "had a good attempt, but the goalkeeper found it a bit too easy.",
            "misses an open goal! Wow, what a miss.",
            "had a good attempt, but the goalkeeper found it a bit too easy.",
            "misses an open goal! Wow, what a miss.",
            "had a good attempt, but the goalkeeper found it a bit too easy.",
            "misses an open goal! Wow, what a miss.",
            "had a good attempt, but the goalkeeper found it a bit too easy.",
            "missed.",
            "missed.",
            "missed.",
            "missed.",
            "missed.",
            "missed.",
            "missed.",
            "missed.",
            "takes the shot... and misses.",
            "takes the shot... and misses.",
            "takes the shot... and misses.",
            "takes the shot... and misses.",
            "takes the shot... and misses.",
            "takes the shot... and misses.",
            "SCORES!, but the goal has been overturned by VAR! (OFFSIDE!)",
            "SCORES!, but the goal has been overturned by VAR! (FOUL!)",
            "SCORES!, but the REF claims the ball wasn't over the line!",
            "ALMOST SCORES! but the ball was knocked away just as it was about to get in!",
            "MISSED A PENALTY!",
            "is surely going to score! But oh no! He's missed!",
            "is surely going to score! But oh no! He's missed!",
            "is surely going to score! But oh no! He's missed!",
            "has got it all wrong! Chance wasted!!",
            "has got it all wrong! Chance wasted!!",
            "has got it all wrong! Chance wasted!!",
            "thought he had it, but the goalkeeper had other ideas!",
            "thought he had it, but the goalkeeper had other ideas!",
            "thought he had it, but the goalkeeper had other ideas!",
            "is going to think about that miss all day after this match!",
            "is going to think about that miss all day after this match!",
            "is going to think about that miss all day after this match!",
            "has hit the post! So close!",
            "has hit the post! So close!",
            "has hit the post! So close!"
            
            ]
        
        global GoalData
        Team1Scorers = []
        Team2Scorers = []
        #Team1 Chances
        for i in range(ChanceTeam1):
            if random.random() <= GoalChanceTeam1 :
                RandomPlayer = str(getRandomPlayer(team1,False))#Team1[1][random.randint(0,3)]
                message = GoalMessage[random.randint(1,len(GoalMessage)-1)]
                if message[0] != "#":
                    playerStat = Team1[3][RandomPlayer]
                    #Individual Goal or Assisted Goal
                    if random.random() <= ((playerStat[1]/100)/2.5):
                        #Individual Goal
                        Commentary.append("GH"+RandomPlayer + " " + message )
                    else:
                        #Assisted Goal
                        Assister = getAssister(Team1[3],RandomPlayer)
                        await AddAssist(Assister)
                        Commentary.append("GH"+RandomPlayer + " " + message + " (Assist : " + Assister + ")")
                    
                    Team1Scorers.append(RandomPlayer)
                    await AddTally(RandomPlayer)
                else:
                    RandomPlayer = getRandomPlayer(team2,True)
                    Commentary.append("GH"+ RandomPlayer + " " + message[1:] )
                    Team1Scorers.append("(OG)"+ RandomPlayer)
            else:
                RandomPlayer = getRandomPlayer(team1,False)
                Commentary.append("MI" +RandomPlayer + " " + str(MissMessage[random.randint(1,len(MissMessage)-1)]))
                
        #Team2 Chances
        for i in range(ChanceTeam2):
            if random.random() <= GoalChanceTeam2 :
                RandomPlayer = str(getRandomPlayer(team2,False))
                message = GoalMessage[random.randint(1,len(GoalMessage)-1)]
                if message[0] != "#":
                    playerStat = Team2[3][RandomPlayer]
                    #Individual Goal or Assisted Goal
                    if random.random() <= ((playerStat[1]/100)/2.5):
                        #Individual Goal
                        Commentary.append("GA"+RandomPlayer + " " + message )
                    else:
                        #Assisted Goal
                        Assister = getAssister(Team2[3],RandomPlayer)
                        await AddAssist(Assister)
                        Commentary.append("GA"+RandomPlayer + " " + message + " (Assist : " + Assister + ")")
                    await AddTally(RandomPlayer)
                    Team2Scorers.append(RandomPlayer)
                else:
                    RandomPlayer = getRandomPlayer(team1,True)
                    Commentary.append("GA"+RandomPlayer + " " + message[1:])
                    Team2Scorers.append("(OG)"+RandomPlayer)
                
            else:
                RandomPlayer = getRandomPlayer(team2,False)
                Commentary.append("MI" +RandomPlayer + " " + str(MissMessage[random.randint(1,len(MissMessage)-1)]))
                
        random.shuffle(Commentary)
        
        FirstHalf = Commentary[:len(Commentary)//2]
        SecondHalf = Commentary[len(Commentary)//2:]
        
        FinalMessage = [
            "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",
            "Welcome to KDD Shawarma League",
            "This is Beter Doury live from the commentary box presenting",
            str("**" + team1 + " VS " + team2 + "**"),
            "Here are the lineups",
            "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",
            str("**" + team1 + ":**")
            ]
        
        #Lineups
        #FinalMessage.append("\n".join(str(e) for e in Team1[1]))
        FinalMessage.append("&" + team1)
        FinalMessage.append("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        FinalMessage.append(str("**" + team2 + ":**"))
        #FinalMessage.append("\n".join(str(e) for e in Team2[1]))
        FinalMessage.append("&" + team2)
        FinalMessage.append("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        """FinalMessage.append(str("**" + team2 + ":**"))
        for plr in TeamList[team2]:
            FinalMessage.append(plr)"""
            
        FinalMessage.append("**First Half Starting:**")
        
        #+ " (" + str(T1Goal) + "-" + str(T2Goal) + ")"
        for msg in FirstHalf:
            code = msg[0:2]
            if code == "GH":
                T1Goal += 1
            elif code == "GA":
                T2Goal += 1
                
            FinalMessage.append(msg[2:]+ " (" + str(T1Goal) + "-" + str(T2Goal) + ")")
            if code == "GH" or code == "GA":
                FinalMessage.append("PAUSE")
            
        FinalMessage.append("**Half Time!**")
        FinalMessage.append("PAUSE")
        for msg in SecondHalf:
            code = msg[0:2]
            if code == "GH":
                T1Goal += 1
            elif code == "GA":
                T2Goal += 1
            FinalMessage.append(msg[2:]+ " (" + str(T1Goal) + "-" + str(T2Goal) + ")")
            if code == "GH" or code == "GA":
                FinalMessage.append("PAUSE")
        FinalMessage.append("**FULLTIME! Final Score:**")
        FinalMessage.append(str(team1 + " " + str(T1Goal) + " - " + str(T2Goal) + " " + team2))
        
        Team1Gif = Team1[2]
        Team2Gif = Team2[2]
        
        if mode != "quick":
            if T1Goal > T2Goal:
                FinalMessage.append(Team1Gif[random.randint(0,len(Team1Gif)-1)])
            elif T2Goal > T1Goal:
                FinalMessage.append(Team2Gif[random.randint(0,len(Team2Gif)-1)])
        else:
            goalMessage = ""
            if T1Goal > 0:
                goalMessage = goalMessage + ", ".join(str(e) for e in Team1Scorers) + "\n"
            if T2Goal > 0:
                goalMessage = goalMessage + ", ".join(str(e) for e in Team2Scorers)
            if goalMessage == "" : goalMessage = "No Goal Scorers"
            FinalMessage.append(goalMessage)
    
        SaveTally()
        return FinalMessage
    else:
        Lineup1 = Data.GetLineups(team1)
        Lineup2 = Data.GetLineups(team2)
        Score1 = [":white_circle: ",":white_circle: ",":white_circle: ",":white_circle: ",":white_circle: "]
        Score2 = [":white_circle: ",":white_circle: ",":white_circle: ",":white_circle: ",":white_circle: "]
        FinalMessage = [
            "We are now headed towards penalties!",
            str(team1 + " will be taking it first.")
            ]
        #Penalties
        G1 = 0
        G2 = 0
        Team1Chance = max(0.35,min(1,0.7 + ( random.randint(-1, 1) / 10 ) + (max(0,((Team1[0]["Att"]*1.1)-Team2[0]["Gk"]))/25)))
        Team2Chance = max(0.35,min(1,0.7 + ( random.randint(-1, 1) / 10 ) + (max(0,((Team2[0]["Att"]*1.1)-Team1[0]["Gk"]))/25)))
        for i in range(5):
            if random.random() <= Team1Chance :
                G1 += 1
                Score1[i] = ":green_circle: "
                FinalMessage.append(str(i+1) + ". " + Lineup1[i] + " scores!" + "(" + str(G1) + "-" + str(G2)+")")
                
            else:
                Score1[i] = ":red_circle: "
                FinalMessage.append(str(i+1) + ". " +Lineup1[i] + " misses!" + "(" + str(G1) + "-" + str(G2)+")")
            
            if random.random() <= Team2Chance :
                G2 += 1
                Score2[i] = ":green_circle: "
                FinalMessage.append(str(i+1) + ". " +Lineup2[i] + " scores!" + "(" + str(G1) + "-" + str(G2)+")")
                
            else:
                Score2[i] = ":red_circle: "
                FinalMessage.append(str(i+1) + ". " +Lineup2[i] + " misses!" + "(" + str(G1) + "-" + str(G2)+")")
         
        Team1Gif = Team1[2]
        Team2Gif = Team2[2]
        if G1 > G2:
            FinalMessage.append("AND " + team1 + " WINS IT IN PENALTIES!!")
            FinalMessage.append(Team1Gif[random.randint(0,len(Team1Gif)-1)])
            #DisplayPenScore(team1,Score1,team2,Score2)
        if G2 > G1:
            FinalMessage.append("AND " + team2 + " WINS IT IN PENALTIES!!")
            FinalMessage.append(Team2Gif[random.randint(0,len(Team2Gif)-1)])
            #DisplayPenScore(team1,Score1,team2,Score2)
        FinalMessage.append(DisplayPenScore(team1,Score1,team2,Score2))
        return FinalMessage
        

async def GameTask(team_1,team_2,mode,homeAdv,interaction):
    global GameOn
    result = await Game(team_1,team_2,mode,homeAdv)
    if result == False:
        await interaction.response.send_message("Unknown Teams")
    else:
        await interaction.response.send_message("Loading Sim...")
        Channel = interaction.channel
        if mode != "quick":
            for msg in result:
                try:
                    if msg == "PAUSE":
                        await asyncio.sleep(2)
                    else:
                        if GameOn == True:
                            if msg[0] != "~" and msg[0] != "&":
                                await Channel.send(msg)
                            elif msg[0] == "&":
                                #Lineup message
                                team = msg[1:]
                                image = Data.GetLineupsnew(team)
                                with io.BytesIO() as image_binary:
                                    image.save(image_binary, 'PNG')
                                    image_binary.seek(0)
                                    await Channel.send(file=discord.File(fp=image_binary, filename='image.png'))
                                    await Channel.send(", ".join(str(e) for e in Data.GetLineups(team.upper())))
                            """else:
                                tm = msg[1:]
                                #gif = TeamGif[tm][random.randint(0,len(TeamGif[tm])-1)]
                                #await Channel.send(gif)"""
                        else:
                            break
                    await asyncio.sleep(2.5)
                except:
                    pass
        else:
            await Channel.send(result[-3])
            await asyncio.sleep(2)
            await Channel.send(result[-2])
            await asyncio.sleep(1)
            await Channel.send(result[-1])
        GameOn = False


#BOT STUFF

intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.guild_messages = True
intents.guild_typing = True
intents.messages = True
intents.message_content = True

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot=commands.Bot(command_prefix=".",intents=intents)

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    global GoalData
    global AssistData
    try:
        with open("GoalTally.yml",'r') as file:
            GoalData = yaml.safe_load(file)
            if GoalData == None:
                GoalData = {}
        with open("AssistTally.yml",'r') as file:
            AssistData = yaml.safe_load(file)
            if AssistData == None:
                AssistData = {}
        await bot.tree.sync()
    except:
        pass
    
    
    
# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
    if message.content == "ksl":
        await message.channel.send(message.author.avatar)
	#if message.content == "hello":
        #print("hm")
		#await message.channel.send("hey dirtbag")
        
@bot.tree.command(name="sim")
async def sim(interaction: discord.Interaction, team_1:str, team_2:str, mode:str):
    global GameOn
    team_1 = team_1.upper()
    team_2 = team_2.upper()
    mode = mode.lower()
    if GameOn == False:   
        asyncio.run(GameTask(team_1,team_2,mode,True,interaction))
    else:
        await interaction.response.send_message("Game On Going!", ephemeral=True)
        
@bot.tree.command(name="simfinal")
async def simfinal(interaction: discord.Interaction, team_1:str, team_2:str, mode:str):
    global GameOn
    team_1 = team_1.upper()
    team_2 = team_2.upper()
    mode = mode.lower()
    if GameOn == False:   
        asyncio.run(GameTask(team_1,team_2,mode,False,interaction))
    else:
        await interaction.response.send_message("Game On Going!", ephemeral=True)
        
        
@bot.tree.command(name="stopgame")
async def stopgame(interaction: discord.Interaction):
    global GameOn 
    GameOn = False
    await interaction.response.send_message("GameStopped!", ephemeral=True)
                
@bot.tree.command(name="teamlist")
async def teamlist(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("\n".join(str(e) for e in Data.GetTeams()))
    except:
        await interaction.response.send_message("Unknown?")
        
@bot.tree.command(name="lineup")
async def lineup(interaction: discord.Interaction, team:str):
    response = Data.GetLineups(team)
    if response != None:
        await interaction.response.send_message("\n".join(str(e) for e in response))
        
@bot.tree.command(name="lineupimg")
async def lineupimg(interaction: discord.Interaction, team:str):
    
    #try:
        image = Data.GetLineupsnew(team)
        with io.BytesIO() as image_binary:
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await interaction.response.send_message(file=discord.File(fp=image_binary, filename='image.png'))
            Channel = interaction.channel
            await Channel.send("**"+team.upper()+":** " + ", ".join(str(e) for e in Data.GetLineups(team.upper())))
    #except :
        #await interaction.response.send_message("Error :/ Did you put the right team?")

   
        
@bot.tree.command(name="topscorer")
async def topscorer(interaction: discord.Interaction):
    await interaction.response.send_message(GetTopScorer())
    
@bot.tree.command(name="topassist")
async def topassist(interaction: discord.Interaction):
    await interaction.response.send_message(GetTopAssist())
    
@bot.tree.command(name="ga")
async def ga(interaction: discord.Interaction):
    await interaction.response.send_message(getGA())
    
@bot.tree.command(name="ovr")
async def ovr(interaction:discord.Interaction, team:str):
    team = team.upper()
    response = Data.DetailedStatsTeam(team)
    msg = "Invalid team?"
    if response != None:
        msg = response
    await interaction.response.send_message(str(team +" : "+ str(msg)))
    
