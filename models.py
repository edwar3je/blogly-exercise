"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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

# Used to initialize 'users' table with data
def initData():
    james = User(first_name='James', last_name='Edwards', image_url='https://p1.hiclipart.com/preview/110/508/41/dog-brown-vizsla-puppy-thumbnail.jpg')
    duncan = User(first_name='Duncan', last_name='Edwards', image_url='https://pngimg.com/d/orangutan_PNG10.png')
    gracie = User(first_name='Gracie', last_name='Smith', image_url='https://i.pinimg.com/originals/f3/3d/c0/f33dc0b602ca13073826c008a8fc3aab.jpg')
    db.session.add(james)
    db.session.add(duncan)
    db.session.add(gracie)
    db.session.commit()