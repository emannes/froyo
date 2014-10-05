import requests
import sqlite3
import simplejson
import urllib
from googlemaps import GoogleMaps
import database import db, Yo
import datetime

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
    previousYo = Yo.query.filter_by(username=username).last()
    newYo = Yo(username=username, latitude=lat, longitude=long, timestamp=datetime.utcnow())
    if previousYo == None:
        pass #just storing initial location
    elif newYo.timestamp - previousYo.timestamp > datetime.timedelta(hours=2):
        pass #that was an old froyo trip
    else:
        froyolat, froyolong = getNearest(lat, long)
        previous_dist = getdist(previousYo.latitude, previousYo.longitude, froyolat, froyolong)
        new_dist = getdist(newYo.latitude, newYo.longitude, froyolat, froyolong)
        if new_dist <= previous_dist:
            warmer(username)
        else:
            colder(username)

    locations[username] = dist
    db.session.add(newYo)
    db.session.commit()
