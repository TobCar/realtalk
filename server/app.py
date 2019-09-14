import os
import uuid
import datetime
from flask import Flask, request
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pytube import YouTube

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS


api = Api(app)
db = SQLAlchemy(app)

db.drop_all()

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=True, nullable=False)
    tag = db.Column(db.String(120), unique=True, nullable=False)
    video_id = db.Column(db.Integer, unique=True, nullable=False)
    ## Convert [0, 1, 1, 2, 1, 1, 0] to "0,1,1,2,1,1,0" for database storage
    ## This is the stream of values the model returns
    model_stream = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return '<Video %r>' % self.url

db.create_all()

# Dashboard Stuff ---------------------
class Status(Resource):
    def get(self):
        return {
            "status": "Working!"
        }, 200

## TODO transform data into flac.file
def convert_to_flac(stream, file_handle):
    return  # do work

class Video(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        video_id = json_data['id']
        url = json_data['url']
        tag = json_data['tag']
        ## TODO Call Youtube API with video id
        YouTube('http://youtube.com/watch?v=9bZkp7q19f0').streams.filter(only_audio=True, subtype='mp4').first().download().register_on_complete_callback(convert_to_flac)
        ## TODO call model script
        ## TODO  grab return value of model endpoint
        ## TODO save return value to database
        ## TODO return value to client
        print("video_id is: ", video_id)

        return {
            "result": "OK"
        }, 200

api.add_resource(Status, '/status')
api.add_resource(Video, '/video')

if __name__ == "__main__":
  app.run()
