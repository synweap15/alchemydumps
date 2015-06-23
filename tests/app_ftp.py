# coding: utf-8

from decouple import config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask_alchemydumps import AlchemyDumps, AlchemyDumpsCommand

# create a Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
ftp_settings = ['ALCHEMYDUMPS_FTP_SERVER',
                'ALCHEMYDUMPS_FTP_USER',
                'ALCHEMYDUMPS_FTP_PASSWORD',
                'ALCHEMYDUMPS_FTP_PATH']
for setting in ftp_settings:
    app.config[setting] = config(setting, default=False)
db = SQLAlchemy(app)
manager = Manager(app)
alchemydumps = AlchemyDumps(app, db, basedir='tests/')
manager.add_command('alchemydumps', AlchemyDumpsCommand)


# create models
class Base(db.Model):
    __abstract__ = True
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime,
                           default=db.func.now(),
                           onupdate=db.func.now())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(140), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')


class Post(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# run
if __name__ == '__main__':
    manager.run()
