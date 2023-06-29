"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(18), nullable=False)
    last_name = db.Column(db.String(18), nullable=False)
    image_url = db.Column(db.String(150), nullable=False, default='https://identicons.github.com/jasonlong.png')

    def __init__(self, first_name, last_name, image_url):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

class Post(db.Model):
    __tablename__= 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_edited = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    us_er = db.relationship('User')

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

# Used to initialize 'users' table with data
def initData():
    james = User(first_name='James', last_name='Edwards', image_url='https://p1.hiclipart.com/preview/110/508/41/dog-brown-vizsla-puppy-thumbnail.jpg')
    duncan = User(first_name='Duncan', last_name='Edwards', image_url='https://pngimg.com/d/orangutan_PNG10.png')
    gracie = User(first_name='Gracie', last_name='Smith', image_url='https://i.pinimg.com/originals/f3/3d/c0/f33dc0b602ca13073826c008a8fc3aab.jpg')
    db.session.add(james)
    db.session.add(duncan)
    db.session.add(gracie)
    db.session.commit()
    sample_post_1 = Post('My first post', 'Hi guys, this is my first post', 1)
    sample_post_2 = Post('I have not posted in a while', 'Sorry I missed you guys, but I will post regularly more often', 2)
    sample_post_3 = Post('Hello blogly', 'Look out for my in-depth posts on lost media', 3)
    db.session.add(sample_post_1)
    db.session.add(sample_post_2)
    db.session.add(sample_post_3)
    db.session.commit()