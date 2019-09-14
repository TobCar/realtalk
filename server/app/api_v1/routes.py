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
        video_id = json_data['video_id']
        print("video_id is: ", video_id)

        return {
            "result": "OK"
        }, 200

api.add_resource(Status, '/status')
api.add_resource(Video, '/video')
