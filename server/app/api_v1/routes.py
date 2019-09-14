from flask import Flask, jsonify, request
from flask_restplus import Resource

from . import api


class Status(Resource):
    def get(self):
        return {
            "status": "Working!"
        }, 200

class Video(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        video_id = json_data['id']
        url = json_data['url']
        tag = json_data['tag']
        ## TODO Call Youtube API with video id
        ## TODO transform data into flac.file
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
