import os
import uuid
import ffmpeg
import datetime
from flask import Flask, request
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pytube import YouTube

AUDIO_FILE_BASE_PATH = './files'

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


class Video(Resource):

    def send_to_model(self, filename):
        print('sending to model')
        # TODO: send the file to the ML model
        # TODO  grab return value of model endpoint
        # TODO save return value to database
        # TODO return value to client
        return

    def yt_progress_handler(self, stream, chunk, file_handler, bytes_remaining):
        print(bytes_remaining)

    def convert_to_mp3(self, stream, file_handle):
        print("its the stream", stream)
        print("its the file_handle", file_handle)
        name = os.path.splitext(file_handle.name)[0].replace(" ", "_").lower()
        output_name = '{name}.mp3'.format(name=name)
        ffmpeg.input(file_handle.name).output(output_name, **{'vn':None,
                                                              'f':'mp3'}).overwrite_output().run()

        print('finished converting file to mp3', output_name)
        self.send_to_model(output_name)
        return

    def post(self):
        video_id = request.form['id']
        url = request.form['url']
        print("video_id is: ", video_id)
        yt = YouTube('http://youtube.com/watch?v=f20lWy2BTr8')
        yt.register_on_complete_callback(self.convert_to_mp3)
        yt.register_on_progress_callback(self.yt_progress_handler)
        stream = yt.streams.filter(only_audio=True, subtype='mp4').first()

        stream.download(output_path=AUDIO_FILE_BASE_PATH)

        return {
            "result": "OK"
        }, 200

api.add_resource(Status, '/status')
api.add_resource(Video, '/video')

if __name__ == "__main__":
  app.run()
