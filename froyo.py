import requests
import sqlite3
import simplejson
import urllib
from googlemaps import GoogleMaps


def getNearest(lat, long):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(lat)+","+str(long)+"&radius=50000&keyword=froyo&rankby=distance&key=AIzaSyCf4chQsasbHzMsEIS_5xGUYczXcraKSgU"
    results = json.load(urllib.urlopen(url))
    result = results["results"][0]["geometry"]["location"]
    return result[lat], result[lng]
    #AIzaSyCf4chQsasbHzMsEIS_5xGUYczXcraKSgU

def getdist(lat, long, froyolat, froyolong):
    return 2 * math.asin(math.sqrt(math.sin((lat - froyolat) / 2) * math.sin((lat - froyolat) / 2) + math.cos(froyolat) * math.cos(lat) * math.sin((froyolong - long) / 2) * math.sin((froyolong - long) / 2)))
    

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
    