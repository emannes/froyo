from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

sqlite_path = '???'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_path
db = SQLAlchemy(app)

class Yo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string(80), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
