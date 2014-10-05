from flask import Flask, request

import string
import froyo

valid_username_chars = string.ascii_letters + string.digits

app = Flask(__name__)

@app.route('/froyo')
def froyo_handler():
    try: 
        username = request.args.get('username','')
        location = request.args.get('location','')
        
        username = string.join([i for i in username if i in valid_username_chars], '')

        coordinates = location.split(';')
        latitude = float(coordinates[0])
        longitude = float(coordinates[1])

        return froyo.receivedYo(username, latitude, longitude)
    except:
        pass

if __name__ == '__main__':
    app.run(debug=True)
