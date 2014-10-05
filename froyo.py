import requests
import json
import urllib
import urllib2
import oauth2
from database import db, Yo
import datetime
import math
import locals

# see https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py
# also https://github.com/YoApp/BarRecommendor/blob/master/main.py
def yelpURL(lat,long):
    city_response = requests.get('http://nominatim.openstreetmap.org/reverse?format=json&lat=' + str(lat) + '&lon=' + str(long) + '&zoom=18&addressdetails=1')
    city_response_object = json.loads(city_response.text)
    city = city_response_object['address']['city']

    url_params = {"term": "froyo", 
                  "cll" : str(lat) + ',' + str(long),
                  "location": city,
                  "radius_filter": 3200,
                  "sort" : 0
    }
    encoded_params = urllib.urlencode(url_params)
    url = "http://api.yelp.com/v2/search/?{}".format(encoded_params)
    return url

def getNearest(lat, long): #this one returns a yelp business json thing
    consumer = oauth2.Consumer(locals.YELP_CONSUMER_KEY, locals.YELP_CONSUMER_SECRET)
    oauth_request = oauth2.Request('GET', yelpURL(lat, long), {})
    oauth_request.update({
        "oauth_nonce" : oauth2.generate_nonce(),
        "oauth_timestamp" : oauth2.generate_timestamp(),
        "oauth_token" : locals.YELP_TOKEN,
        "oauth_consumer_key" : locals.YELP_CONSUMER_KEY})
    token = oauth2.Token(locals.YELP_TOKEN, locals.YELP_TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()
    business_add = ', '.join(response['businesses'][0]['location']['display_address'])
    return business_add


def geolocate(address): #returns lat, long
    url_params = {'format' : 'json',
                  'addressdetails' : 1,
                  'limit' : 1}
    response = requests.get('http://nominatim.openstreetmap.org/search/' + urllib.quote(address), params = url_params)
    response_json = json.loads(response.text)[0]
    return (float(response_json['lat']), float(response_json['lon']))

def getdist(lat, long, froyolat, froyolong):
    return 2 * math.asin(math.sqrt(math.sin((lat - froyolat) / 2) * math.sin((lat - froyolat) / 2) + math.cos(froyolat) * math.cos(lat) * math.sin((froyolong - long) / 2) * math.sin((froyolong - long) / 2)))

def colder(username):
    api_token = locals.YO_COLDER
    requests.post("http://api.justyo.co/yo/", data={'api_token': api_token, 'username': username})
    
def warmer(username):
    api_token = locals.YO_WARMER
    requests.post("http://api.justyo.co/yo/", data={'api_token': api_token, 'username': username})

def receivedYo(username, lat, long):
    previousYos = Yo.query.filter_by(username=username).all()
    newYo = Yo(username=username, latitude=lat, longitude=long, timestamp=datetime.datetime.utcnow())
    if len(previousYos) == 0:
        pass #just storing initial location
    else:
        previousYoID = max([y.id for y in previousYos])
        previousYo = Yo.query.get(previousYoID)
        if newYo.timestamp - previousYo.timestamp > datetime.timedelta(hours=2):
            pass #that was an old froyo trip
        else:
            froyolat, froyolong = geolocate(getNearest(lat, long))
            previous_dist = getdist(previousYo.latitude, previousYo.longitude, froyolat, froyolong)
            new_dist = getdist(newYo.latitude, newYo.longitude, froyolat, froyolong)
            if new_dist <= previous_dist:
                warmer(username)
            else:
                colder(username)
    db.session.add(newYo)
    db.session.commit()
    return str(previousYo.timestamp)

