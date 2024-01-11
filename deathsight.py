import requests
import json
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

def getMoreData(): #pull the data from api
    re = requests.get("https://api.achaea.com/gamefeed.json?limit=10000")
    n = json.loads(re.text)
    #print((n))
    n = clearAllButPK(n)
    return n

def clearAllButPK(data): #remove non-death events
    return [x for x in data if x['caption'] == 'Player Death']

def getLastID(data): #what's the last ID we have already?
    val = 0
    for i in data:
        if i['id'] > val:
            val = i['id']
    return val

def saveDataToFile(data):
    with open("pk_data.json", "w") as outfile:
        outfile.write(json.dumps(data))

def getCurrentData():
    d= open("pk_data.json", "r")
    o = json.load(d)
    return o

def main():
    #saveDataToFile(getMoreData())
    oldData = getCurrentData()
    od = pd.DataFrame(oldData)
    d = pd.DataFrame(data=getMoreData())
    od.merge(d,how='left', on='id')
    saveDataToFile(od.to_json(orient="records"))



main()