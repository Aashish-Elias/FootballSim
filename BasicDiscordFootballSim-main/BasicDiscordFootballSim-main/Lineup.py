from PIL import Image
import urllib.request
import csv
import pandas as pd
import requests
from io import BytesIO

#LINEUPS ARE TOP TO BOTTOM, LEFT TO RIGHT
LineupData = {
    "433" :[
        (198, 92),
        (378, 76),
        (558, 92),
        (232, 154),
        (378, 140),
        (524, 154),
        (176, 236),
        (300, 236),
        (456, 236),
        (580 , 236),
        (378, 312)
        ],
    "523" :[
        (198, 92),
        (378, 76),
        (558, 92),
        (232, 154),
        (524, 154),
        (165, 236),
        (271, 236),
        (378, 236),
        (485, 236),
        (591 , 236),
        (378, 312)
        ],
    "352" :[
        (271, 76),
        (485, 76),
        (165, 154),
        (271, 154),
        (378, 154),
        (485, 154),
        (591, 154),
        (271, 236),
        (378, 236),
        (485 , 236),
        (378, 312)
        ],
    "442" :[
        (271, 76),
        (485, 76),
        (176, 140),
        (300, 140),
        (456, 140),
        (580, 140),
        (176, 236),
        (300, 236),
        (456, 236),
        (580 , 236),
        (378, 312)
        ]
    }

data = pd.read_csv("playerdata.csv")

def Getlineup(lineup,formation):
    Lineupimage =  Image.open(r"pitch.png")
    Lineupimage.save("finalpitch.png")
    FinalLineup = Image.open("finalpitch.png")
    for i in range(11):
        try:
            name = lineup[i]
            IMG = data.loc[data['Known As'] == name]["Image Link"].values[0]
            #print(IMG)
            #urllib.request.urlretrieve(str(IMG),"player.png")
            r = requests.get(IMG)
            img =  Image.open(BytesIO(r.content)) #Image.open("player.png")
            FinalLineup.paste(img,LineupData[formation][i],mask=img)
            FinalLineup.save("finalpitch.png")
        except:
            pass
    return FinalLineup
    
Getlineup(
    [
     "M. Rashford",
     "Cristiano Ronaldo",
     "Antony",
     "M. Sabitzer",
     "Bruno Fernandes",
     "Casemiro",
     "L. Shaw",
     "Lisandro Martinez",
     "R. Varane",
     "Diogo Dalot",
     "De Gea"
     ],
    "433")