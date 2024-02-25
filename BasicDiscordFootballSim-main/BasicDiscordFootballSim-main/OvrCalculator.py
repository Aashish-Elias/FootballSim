#Overall calculator

#COEFFICIENTS:
#AtkCoef, DribCoef, DefCoef, PasCoef, PhyCoef
#Attackers coefficient (in order) :   3,3,1,1,2
#Midfielders coefficient (in order) : 2,2,2,3,2
#Defenders coefficient (in order) :   1,1,3,2,3
Coefficients={
    "F" : [3,3,1,2,2],
    "M" : [2,2,2,3,2],
    "D" : [1,1,3,1,3]
    }


def Team(Players):
    atk = []
    dri = []
    dff = []
    pss = []
    phy = []
    gk = 0
    for key in Players.keys():
        if len(Players[key]) > 1:
            Coef = Players[key][0]
            for i in range(Coefficients[Coef][0]):    
                atk.append(Players[key][1])
            for i in range(Coefficients[Coef][1]):
                dri.append(Players[key][2])
            for i in range(Coefficients[Coef][2]):
                dff.append(Players[key][3])
            for i in range(Coefficients[Coef][3]):
                pss.append(Players[key][4])
            for i in range(Coefficients[Coef][4]):
                phy.append(Players[key][5])
        else:
            gk = Players[key][0]
   # print("STATS: ",(sum(atk)/len(atk)),(sum(dri)/len(dri)),(sum(dff)/len(dff)),(sum(pss)/len(pss)),(sum(phy)/len(phy)),gk)
   # print("OVERALL:",((sum(atk)/len(atk))+(sum(dri)/len(dri))+(sum(dff)/len(dff))+(sum(pss)/len(pss))+(sum(phy)/len(phy))+gk)/5, "OR", round(((sum(atk)/len(atk))+(sum(dri)/len(dri))+(sum(dff)/len(dff))+(sum(pss)/len(pss))+(sum(phy)/len(phy))+gk)/5))
    #return [(sum(atk)/len(atk)),(sum(dri)/len(dri)),(sum(dff)/len(dff)),(sum(pss)/len(pss)),(sum(phy)/len(phy)),gk]
    return {
        "Att" : (sum(atk)/len(atk)),
        "Dri" : (sum(dri)/len(dri)),
        "Def" : (sum(dff)/len(dff)),
        "Pas" : (sum(pss)/len(pss)),
        "Phy" : (sum(phy)/len(phy)),
        "Gk"  : gk
        }




#Position, ATK, Drib, DEF, PAS, Phy
class mun():
    squad={
    "Cristiano Ronaldo" : ["F",90,78,62,74,75],
    "M. Rashford" :["F",84,81,63,77,85],
    "Antony" : ["F",79,88,56,76,81],
    "Bruno Fernandes" : ["M",85,83,64,88,78],
    "Casemiro" : ["M",74,74,85,75,80],
    "M. Sabitzer" :  ["M",81,81,71,81,81],
    "L. Shaw" : ["D",69,81,79,81,83],
    "L. Martinez" : ["D",65,74,78,72,76],
    "R. Varane" : ["D",56,63,82,67,76],
    "Diogo Dalot" : ["D",72,76,76,75,81],
    "De Gea" : [86]
    }
    formation = "433"
    gifs =[
        "https://tenor.com/view/manchester-united-manunited-rashford-lingard-gif-5881754",
        "https://tenor.com/view/lisandro-lisandro-martinez-martinez-lisandro-martinez-man-utd-manchester-united-gif-26549869",
        "https://tenor.com/view/man-manchester-united-utd-bruno-gif-24594137"
        ]
    
    Tm = Team(squad)
    
class fcb():
    squad={
    "O. Dembele" : ["F",78,87,57,77,79],
    "R. Lewandowski" : ["F",89,80,66,75,76],
    "Ferran Torres" : ["F",80,84,61,75,81],
    "Gavi" : ["M",72,89,70,76,76],
    "Pedri" :["M",74,90,69,79,79],
    "F. Kessie" : ["M",79,78,83,78,85],
    "Jordi Alba" : ["D",79,83,75,81,82],
    "Eric García" : ["D",67,78,82,77,79],
    "Pique" : ["D",69,75,85,74,74],
    "J. Kounde" : ["D",70,78,87,74,83],
    "M. ter Stegen" : [82]
    }
    formation = "433"
    gifs = [
        "https://tenor.com/view/xavi-xavier-hernandez-barca-barcelona-manager-goal-goat-messi-gif-25173845",
        "https://tenor.com/view/barcelona-barca-barcateam-gif-20607502",
        "https://tenor.com/view/messi-haha-celebration-cheering-gif-15318804"
        ]
    
    Tm = Team(squad)
    
class psg():
    squad={
    "Neymar Jr" : ["F",81,89,57,87,75],
    "K. Mbappe" : ["F",84,88,62,77,85],
    "L. Messi" : ["F",87,92,57,90,75],
    "M. Verratti" :["M",65,89,71,80,70],
    "Fabian Ruiz" : ["M",79,83,72,82,76],
    "Nuno Mendes" : ["D",70,79,70,73,85],
    "Marquinhos" : ["D",63,73,85,71,77],
    "Danilo Pereira" : ["D",71,73,83,72,80],
    "Sergio Ramos" : ["D",68,73,87,76,72],
    "A. Hakimi" : ["D",77,80,73,74,86],
    "G. Donnarumma" : [79]
    }
    formation = "523"
    gifs = [
        "https://tenor.com/view/kylian-mbapp%C3%A9-paris-saint-germain-psg-gif-13744115"
        ]
    
    Tm = Team(squad)
    
class mci():
    squad={
    "J. Alvarez" : ["F",84,83,70,79,80],
    "E. Haaland" : ["F",90,67,69,67,82],
    "K. De Bruyne" : ["M",83,82,62,88,76],
    "Bernardo Silva" : ["M",75,89,61,76,75],
    "Rodri" : ["M",74,79,82,74,76],
    "I. Gundogan" : ["M",83,86,71,86,79],
    "J. Cancelo" : ["D",75,84,73,85,81],
    "N. Ake" : ["D",58,68,79,64,74],
    "J. Stones" : ["D",61,76,79,70,75],
    "K. Walker" : ["D",67,70,73,71,82],
    "Ederson" : [82]
    }
    formation = "442"
    gifs = [
        "https://tenor.com/view/happy-football-yes-celebrate-goal-gif-25780750"
        ]
    
    Tm = Team(squad)
    
class ars():
    squad={
    "B. Saka" : ["F",77,85,61,78,82],
    "Gabriel Martinelli" : ["F",73,78,62,68,81],
    "L. Trossard" : ["F",81,88,62,82,81],
    "Jorginho" : ["M",70,82,75,81,72],
    "G. Xhaka" : ["M",78,77,76,84,78],
    "M. Ødegaard" :["M",77,89,65,84,76],
    "B. White" : ["D",67,77,85,75,81],
    "Gabriel" : ["D",62,68,85,68,79],
    "O. Zinchenko" : ["D",77,83,77,83,79],
    "W. Saliba" : ["D",62,72,81,70,78],
    "A. Ramsdale" : [84]
    }
    formation = "433"
    gifs = [
        "https://tenor.com/view/forshay-gif-20852560",
        "https://tenor.com/view/odegaard-arsenal-martin-odegaard-nld-spurs-gif-20744797"
        ]
    
    Tm = Team(squad)

    
class rma():
    squad={
    "K. Benzema" : ["F",88,83,65,74,75],
    "F. Valverde" : ["F",78,81,76,77,86],
    "Rodrygo" : ["F",79,85,62,76,80],
    "T. Kroos" :["M",80,81,70,88,73],
    "A.Tchouameni" : ["M",71,79,80,78,81],
    "L. Modric" : ["M",76,89,70,87,74],
    "D. Alaba" : ["D",71,76,79,82,77],
    "Carvajal" : ["D",71,80,78,78,83],
    "E. Camavinga" : ["D",76,83,79,78,79],
    "Nacho Fernandez" : ["D",68,76,86,73,82],
    "T. Courtois" : [83]
    }
    formation = "433"
    gifs = [
        "https://tenor.com/view/blancosksa-dy1ns-real-madrid-gif-21057646",
        "https://tenor.com/view/ronaldo-real-madrid-futbol-gif-25955148",
        "https://tenor.com/view/blancosksa-dy1ns-real-madrid-ancelotti-gif-22416338"
        ]
    
    Tm = Team(squad)
    
class tot():
    squad={
    "H. Kane" : ["F",90,73,64,77,77],
    "H. Son" : ["F",87,80,57,73,81],
    "D. Kulusevski" : ["F",76,78,61,76,79],
    "I. Perisic" :["M",73,74,69,73,77],
    "R. Bentancur" : ["M",71,76,74,78,76],
    "P. Højbjerg" : ["M",73,73,75,76,73],
    "Emerson" : ["M",66,70,69,66,76],
    "B. Davies" : ["D",64,71,73,68,74],
    "E. Dier" : ["D",65,66,78,73,74],
    "C. Romero" : ["D",66,69,88,65,81],
    "H. Lloris" : [80]
    }
    formation = "433"
    gifs = [
        "https://tenor.com/view/tottenham-hotspur-harry-kane-gif-19877562",
        "https://tenor.com/view/son-spurs-tottenham-heung-min-son-spider-man-gif-23998238",
        "https://tenor.com/view/tottenham-steven-bergwjin-ratio-hotspur-spurs-gif-26250257"
        ]
    
    Tm = Team(squad)
    
class lyo():
    squad={
    "A. Lacazette" : ["F",85,84,69,76,77],
    "A. Sarr" : ["F",68,64,53,60,73],
    "R. Cherki" : ["M",79,87,63,78,79],
    "J. Lepenant" :["M",59,70,66,66,69],
    "Thiago Mendes" : ["M",65,70,69,71,69],
    "S. Kumbedi" : ["M",54,65,61,58,69],
    "N. Tagliafico" : ["M",75,80,80,84,81],
    "S. Diomande" : ["D",65,70,82,70,78],
    "D. Lovren" : ["D",62,65,77,66,70],
    "C. Lukeba" : ["D",54,65,71,62,70],
    "A. Lopes" : [76]
    }
    formation = "352"
    gifs = [
        "https://tenor.com/view/houssem-aouar-french-footballer-olympique-lyonnais-brain-gif-16636710"
        ]
    
    Tm = Team(squad)
    
#TeamData getter
teams={
       "MUN" : mun(),
       "FCB" : fcb(),
       "PSG" : psg(),
       "MCI" : mci(),
       "ARS" : ars(),
       "RMA" : rma(),
       "TOT" : tot(),
       "LYO" : lyo()
       }

def GetTeam(teamName):
    teamName = teamName.upper()
    if teamName in teams.keys():
        return [
            teams[teamName].Tm,
            list(teams[teamName].squad.keys()),
            teams[teamName].gifs,
            teams[teamName].squad
                ]
    else: return None

def GetTeams():
    return list(teams.keys())

def GetLineups(teamName):
    teamName = teamName.upper()
    if teamName in teams.keys():
        return list(teams[teamName].squad.keys())
    
def GetLineupsnew(teamName):
    
    teamName = teamName.upper()
    if teamName in teams.keys():
        import Lineup as lp
        return lp.Getlineup(
            list(teams[teamName].squad.keys()),
            teams[teamName].formation)
    
def GetPlayersByPosition(team,pos):
    team = team.upper()
    pos = pos.upper()
    if team in teams.keys():
        """if pos == "G":
            return [list(teams[team].squad.keys())[4]]
        elif pos == "F":
            return [player for player in list(teams[team].squad.keys()) if teams[team].squad[player][0] == pos]
        elif pos == "M":
            return [player for player in list(teams[team].squad.keys()) if teams[team].squad[player][0] == pos]
        elif pos == "D":
            return [player for player in list(teams[team].squad.keys()) if teams[team].squad[player][0] == pos]"""
        if pos == "G":
            return [list(teams[team].squad.keys())[-1]]
        elif pos == "F":
            return [player for player in list(teams[team].squad.keys()) if teams[team].squad[player][0] == pos]
        elif pos == "M":
            return [player for player in list(teams[team].squad.keys()) if teams[team].squad[player][0] == pos]
        elif pos == "D":
            return [player for player in list(teams[team].squad.keys()) if teams[team].squad[player][0] == pos]
        
def GetPlayerStat(player,team):
    team = team.upper()
    if team in teams.keys():
        if player in list(teams[team].squad.keys()):
            return team[teams].squad[player]
        
def DetailedStatsTeam(team):
    team = team.upper()
    if team in teams.keys():
        tm = teams[team].Tm
        print("+++++++++++++++++++++")
        print(team)
        print(tm)
        print((tm["Att"] + tm["Dri"] + tm["Def"] + tm["Pas"] + tm["Phy"] + tm["Gk"])/5)
        print("+++++++++++++++++++++")
        return (tm["Att"] + tm["Dri"] + tm["Def"] + tm["Pas"] + tm["Phy"] + tm["Gk"])/5
    else:
        return None
    

    
#DetailedStatsTeam("mun")
