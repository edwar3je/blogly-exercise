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
    tags = db.relationship('Tag', secondary='tagged_posts', backref='post')
    p_tags = db.relationship('PostTag', backref='p_ost')

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

class Tag(db.Model):
    __tablename__= 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    posts = db.relationship('Post', secondary='tagged_posts', backref='tag')
    t_posts = db.relationship('PostTag', backref='t_ag')

    def __init__(self, name):
        self.name = name

class PostTag(db.Model):
    __tablename__= 'tagged_posts'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __init__(self, post_id, tag_id):
        self.post_id = post_id
        self.tag_id = tag_id

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
    # add a few rows for 'tags'
    sample_tag_1 = Tag(name='Fun')
    sample_tag_2 = Tag(name='Meme')
    sample_tag_3 = Tag(name='Cute')
    db.session.add(sample_tag_1)
    db.session.add(sample_tag_2)
    db.session.add(sample_tag_3)
    db.session.commit()
    # add a few rows for 'taggedposts'
    sample_tag_post_1 = PostTag(post_id=1, tag_id=1)
    sample_tag_post_2 = PostTag(post_id=1, tag_id=2)
    sample_tag_post_3 = PostTag(post_id=2, tag_id=1)
    sample_tag_post_4 = PostTag(post_id=2, tag_id=3)
    sample_tag_post_5 = PostTag(post_id=3, tag_id=2)
    sample_tag_post_6 = PostTag(post_id=3, tag_id=3)
    db.session.add(sample_tag_post_1)
    db.session.add(sample_tag_post_2)
    db.session.add(sample_tag_post_3)
    db.session.add(sample_tag_post_4)
    db.session.add(sample_tag_post_5)
    db.session.add(sample_tag_post_6)
    db.session.commit()