import os
import time
import ffmpeg
from flask import Flask, request
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pytube import YouTube
from ml_model import inference
from gcs import GCS

AUDIO_FILE_BASE_PATH = './files'
GCS_BUCKET_NAME = 'realtalk-252903.appspot.com'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

api = Api(app)
db = SQLAlchemy(app)

# DB stuff -------------------------------------------------------------
def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clearing table {0}'.format(table))
        session.execute(table.delete())
    session.commit()

# start database from scratch
clear_data(db.session)

class VideoInfo(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.String(50), primary_key=True)
    url = db.Column(db.String(80), unique=True, nullable=False)
    file_name = db.Column(db.String(100), unique=True, nullable=False)
    tag = db.Column(db.String(120), nullable=True)
    video_id = db.Column(db.String(50), unique=True, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    ## Convert [0, 1, 1, 2, 1, 1, 0] to "0,1,1,2,1,1,0" for database storage
    ## This is the stream of values the model returns
    output = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return '<Video %r>' % self.url

db.create_all() # must come after above class definitions

# API stuff ------------------------------------------------------------
class Status(Resource):
    def get(self):
        return {
            "status": "Working!"
        }, 200


class Analytics(Resource):
    def get(self):
        print('retrieving analytics')
        result = []
        info = VideoInfo.query.all()
        for v in info:
            result.append({
                'id':v.id,
                'url':v.url,
                'file_name':v.file_name,
                'tag':v.tag,
                'video_id':v.video_id,
                'count':v.count,
                'output':v.output.split(',')
            })

        return {
            "result": "OK",
            "status": result
        }, 200




class Video(Resource):

    def __init__(self, _):
        self.output = []
        self.file_name = ''

    def cache(self, data):
        row = VideoInfo.query.filter_by(video_id=data['video_id']).first()
        if row:
            print('Entry already exists')
            return False

        print('caching data', data)
        output_string = ",".join(map(str, data['output']))
        video_info = VideoInfo(id=data['id'], url=data['url'],
                               file_name=data['file_name'], tag=data['tag'],
                               video_id=data['video_id'], count=data['count'],
                               output=output_string)
        db.session.add(video_info)
        db.session.commit()
        return True

    def check_cache(self, video_id):
        print('checking cache')
        row = VideoInfo.query.filter_by(video_id=video_id).first()
        if row:
            print('cache hit')
            video_info = {
                'id':row.id,
                'url':row.url,
                'file_name':row.file_name,
                'tag':row.tag,
                'video_id':row.video_id,
                'count':row.count,
                'output':row.output.split(',')
            }
            return True, video_info

        print('cache miss')
        return False, {}

    def send_to_model(self, filename):
        print('starting prediction')
        output = inference.classify(filename)
        self.output = output

    def yt_progress_handler(self, stream, chunk, file_handler, bytes_remaining):
        print('bytes remaining:', bytes_remaining)

    def convert_to_mp3(self, stream, file_handle):
        name = os.path.splitext(file_handle.name)[0].replace(" ", "_").lower()
        self.file_name = '{name}.mp3'.format(name=name)
        ffmpeg.input(file_handle.name).output(self.file_name, **{'vn':None,
                                                              'f':'mp3'}).overwrite_output().run()
        print('sending file to model', self.file_name)
        self.send_to_model(self.file_name)
        return

    def post(self):
        video_id = request.form['id']
        url = request.form['url']
        print("downloading youtube video:", video_id)

        cached, result = self.check_cache(video_id)
        # TODO: uncomment in prod 
        # if cached:
        #     print('returning cached result')
        #     return {
        #         "result": "OK",
        #         "data": result['output']
        #     }, 200

        # TODO: uncomment in prod
        # yt = YouTube('http://youtube.com/watch?v=f20lWy2BTr8')
        # yt.register_on_complete_callback(self.convert_to_mp3)
        # yt.register_on_progress_callback(self.yt_progress_handler)
        # stream = yt.streams.filter(only_audio=True, subtype='mp4').first()
        # stream.download(output_path=AUDIO_FILE_BASE_PATH)

        # TODO: following is temporary code for dev purposes
        self.output = [0, 1, 0, 0, 1, 1]
        self.file_name = 'highlights_of_trudeaus_victory_speech.mp3'
        gcs_url = GCS.upload_to_bucket('testing',
                             AUDIO_FILE_BASE_PATH + '/highlights_of_trudeaus_victory_speech.mp3',
                             GCS_BUCKET_NAME)
        print('finished uploading to GCS bucket at url:', gcs_url)
        print('filename is ', self.file_name)

        #print('url:', gcs_url)
        time_elapsed = 0
        while not self.output:
            print("developing prediction...", time_elapsed)
            time_elapsed += 1
            time.sleep(1)

        # cache the result
        id = video_id # video_id should be unique for youtube
        tag = 'youtube'
        count = 0
        cache_row = {
            'id':id,
            'url':url,
            'file_name':self.file_name,
            'tag':tag,
            'video_id':video_id,
            'count':0,
            'output':self.output
        }
        self.cache(cache_row)

        return {
            "result": "OK",
            "data": self.output
        }, 200

api.add_resource(Status, '/status')
api.add_resource(Video, '/video')
api.add_resource(Analytics, '/analytics')

if __name__ == "__main__":
  app.run()
