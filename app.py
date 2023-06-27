"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, initData

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'it is a secret'

connect_db(app)
# Need to include this so Flask has context for running db.create_all()
# Included drop_all() so I don't have to keep resetting the database each time (will remove)
with app.app_context():
    db.drop_all()
    db.create_all()
    initData()

# Redirects users back to '/users' route.
@app.route('/')
def goBack():
    return redirect('/users')

# Shows a list of all the users. Makes the names into links to view a detailed page
# of the selected users. Also displays a link to go to the '/users/new' route.
@app.route('/users')
def display_home():
    with app.app_context():
        users = User.query.all()
        print(users)
    return render_template('home.html', users=users)

# Shows an add form form for users.
@app.route('/users/new')
def display_add_user():
    return render_template('create.html')

# Processes post request to create a new user and redirects to '/users'.
@app.route('/users/new', methods=["POST"])
def handle_add_user():
    first_name = request.form.get('first name')
    last_name = request.form.get('last name')
    image_url = request.form.get('image url')
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
    return redirect('/users')

# Displays information on a user and provides two buttons. One links to a form that
# allows a user to edit their information. The other links to a post route
# ('/users/<user-id>/delete') that deletes the user from the database.
@app.route('/users/<ind>')
def display_user(ind):
    path_id = int(request.path.replace('/users/', ''))
    with app.app_context():
        user = User.query.filter_by(id=path_id).first()
    return render_template('user.html', user=user)

# Displays the edit page for a user. Has a cancel button that redirects user back to
# user page and a save button that sends a POST request ('/users/<user-id>/edit) that
# updates the user.
@app.route('/users/<ind>/edit')
def display_edit(ind):
    path_id = int(request.path.replace('/users/', '').replace('/edit', ''))
    with app.app_context():
        user = User.query.filter_by(id=path_id).first()
    return render_template('edit.html', user=user)

# Processes the edit form and returns the user to '/users'.
@app.route('/users/<ind>/edit', methods=["POST"])
def handle_edit_user(ind):
    path_id = int(request.path.replace('/users/', '').replace('/edit', ''))
    f_name = request.form.get('first name')
    l_name = request.form.get('last name')
    i_url = request.form.get('image url')
    with app.app_context():
        user = User.query.get(path_id)
        user.first_name = f_name
        user.last_name = l_name
        user.image_url = i_url
        db.session.commit()
        print(User.query.get(path_id))
    return redirect('/users')

# Deletes the user and redirects the user to '/users'.
@app.route('/users/<ind>/delete', methods=["POST"])
def deleteUser(ind):
    path_id = int(request.path.replace('/users/', '').replace('/delete', ''))
    with app.app_context():
        User.query.filter_by(id=path_id).delete()
        db.session.commit()
        print(User.query.all())
    return redirect('/users')