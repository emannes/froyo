import requests
import sqlite3


def getNearest(lat, long):
    pass

def getdist(lat, long, froyolat, froyolong):
    pass

def colder(username):
    api_token = '1a2131b6-573f-95bb-b12e-0e2d0b7486e8'
    requests.post("http://api.justyo.co/yo/", data={'api_token': api_token, 'username': username})
    
def warmer(username):
    api_token = '8cf17169-3f15-d994-8eaa-71148c5b8b02'
    requests.post("http://api.justyo.co/yo/", data={'api_token': api_token, 'username': username})

def receivedYo(username, lat, long):
    conn = sqlite3.connect('dists.db')
    c = conn.cursor()
    c.execute(
    froyolat, froyolong = getNearest(lat, long)
    dist = getdist(lat, long, froyolat, froyolong)
    if username in locations:
        if locations[username] < dist:
            colder(username)
        else:
            warmer(username)
    locations[username] = dist
    