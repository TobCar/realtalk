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
from gcs.Streamable import Streamable
from google.cloud import storage

AUDIO_FILE_BASE_PATH = './files'
# AUDIO_FILE_BASE_PATH = '/tmp'
GCS_BUCKET_NAME = 'realtalk-252903.appspot.com'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

storage_client = storage.Client.from_service_account_json('./gcs/realtalk-c580fb239c1b.json')


MOCK_1 = [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

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
# clear_data(db.session)

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
        self.dst_uri = ''

    def get(self):
        self.add_hardcoded()
        return {
            "result": "Cached video files"
        }, 200


    def add_hardcoded():
        mock_data = [
            ['cQ54GDm1eL0', 'https://www.youtube.com/watch?v=cQ54GDm1eL0', 'You Won’t Believe What Obama Says In This Video!', '', 'cQ54GDm1eL0',0, []],
            ['VnFC-s2nOtI', 'https://www.youtube.com/watch?v=VnFC-s2nOtI', 'This AI Can Clone Any Voice, Including Yours', '', 'VnFC-s2nOtI',0, []],
            ['YfU_sWHT8mo', 'https://www.youtube.com/watch?v=YfU_sWHT8mo', 'Lyrebird - Create a digital copy of your voice', '', 'YfU_sWHT8mo',0, []]
        ]

        for v in mock_data:
            video_info = VideoInfo(id=v[0], url=v[1], file_name=v[2],
                                   tag=v[3],video_id=v[4],
                                   count=v[5],output=",".join(map(str, v[6])))
            db.session.add(video_info)
            db.session.commit()


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
        # TODO-2 uncomment for gcs
        # with Streamable(client=storage_client, bucket_name=GCS_BUCKET_NAME, blob_name='pikachu-time2') as s:
        #     s.write(chunk)

        # self.dst_uri.new_key().set_contents_from_stream(chunk)
        # print('sent chunk:', chunk)

    def convert_to_mp3(self, stream, file_handle):
        name = os.path.splitext(file_handle.name)[0].replace(" ", "_").lower()
        self.file_name = '{name}.mp3'.format(name=name)

        ffmpeg.input(file_handle.name).output(self.file_name, **{'vn':None,'f':'mp3'}).overwrite_output().run()
        print('sending file to model', self.file_name)
        self.send_to_model(self.file_name)
        return


    def post(self):
        video_id = request.form['id']
        url = request.form['url']
        print("downloading youtube video:", video_id)

        cached, result = self.check_cache(video_id)

        if cached:
            print('returning cached result')
            return {
                "result": "OK",
                "data": result['output']
            }, 200

        # TODO: uncomment in prod
        # TODO: should use passed in url
        yt = YouTube(url)
        # yt = YouTube('https://www.youtube.com/watch?v=CrJ4KUjFheQ')
        yt.register_on_complete_callback(self.convert_to_mp3)
        yt.register_on_progress_callback(self.yt_progress_handler)
        stream = yt.streams.filter(only_audio=True, subtype='mp4').first()
        stream.download(output_path=AUDIO_FILE_BASE_PATH)
        # stream.stream_to_buffer() # TODO-2: uncomment for gcs

        # self.file_name = video_id
        # my_stream = open(filename, 'rb')
        # self.dst_uri = boto.storage_uri(GCS_BUCKET_NAME + '/' + self.file_name, 'gs')
        # dst_uri.new_key().set_contents_from_stream(stream)


        # TODO: following is temporary code for dev purposes
        # self.output = [0, 1, 0, 0, 1, 1]
        # self.file_name = 'highlights_of_trudeaus_victory_speech.mp3'

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
