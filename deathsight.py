import requests
import json
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import re

def getMoreData(): #pull the data from api
    re = requests.get("https://api.achaea.com/gamefeed.json?limit=10000")
    n = json.loads(re.text)
    #print((n))
    n = clearAllButPK(n)
    return n

def clearAllButPK(data): #remove non-death events
    return [x for x in data if x['caption'] == 'Player Death']

def saveDataToFile(data): #storage 
    with open("pk_data.json", "w") as outfile:
        json.dump(data, outfile)

def getCurrentData():
    d= open("pk_data.json", "r")
    o = json.loads(d.read())
    return o

def getCurrentPlayerData():
    d = open("player_data.json", "r")
    o = json.loads(d.read())
    return o

def getPlayerData(name):
    re = requests.get("https://api.achaea.com/characters/" + name + ".json")
    n = json.loads(re.text)
    return n

def storePlayerData(df, name_list):
    d_l = []
    checked_names = []
    for name in name_list: #eliminate duplicate calls
        if not (name in checked_names):
            d_l.append(getPlayerData(name))
            checked_names.append(name)
    tempDf = pd.DataFrame(data=d_l)
    return pd.concat([df, tempDf]).drop_duplicates(subset='name',keep='last')

def writePlayerData(df):
    df.to_json("player_data.json",orient="records",mode="w")

def getNames(df):
    p = re.compile("^(\S+) was slain by (\S+)\.$")
    n = []
    for i in df['description']:
        r = p.fullmatch(i)
        if r:
            if not (r.group(1) in n) & (r.group(1) != "misadventure"):
                n.append(r.group(1))
            if not (r.group(2) in n) & (r.group(2) != 'misadventure'):
                n.append(r.group(2))
    return n


def main():
    #saveDataToFile(getMoreData())
    oldData = getCurrentData()
    od = pd.DataFrame(oldData)
    #print(od)
    ps = pd.DataFrame(getCurrentPlayerData())
    d = pd.DataFrame(data=getMoreData())
    d.columns = od.columns.tolist()
    output = pd.concat([od, d]).drop_duplicates()
    #slain, killers = getNames(output)
    #players = storePlayerData(ps, slain)
    #players = storePlayerData(players, killers)
    
    #print(players)
    #print(slain)
    #print(killers)
    lastID = od['id'].iloc[-1]
    subsection = output.loc[output['id'] > lastID]
    names = getNames(subsection)
    #names = [*slain]
    players = storePlayerData(ps, names)
    print(players)
    #print(lastID)
    print(output)
    writePlayerData(players)
    output.to_json("pk_data.json",orient="records",mode="w")
    
    


main()