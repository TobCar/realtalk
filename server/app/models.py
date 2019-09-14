from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=True, nullable=False)
    tag = db.Column(db.String(120), unique=True, nullable=False)
    video_id = db.Column(db.Integer, unique=True, nullable=False)
    ## Convert [0, 1, 1, 2, 1, 1, 0] to "0,1,1,2,1,1,0" for database storage
    ## This is the stream of values the model returns
    model_stream = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return '<Video %r>' % self.url
