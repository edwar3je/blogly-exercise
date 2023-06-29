"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, initData, Post
from datetime import datetime

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
        posts = Post.query.filter(Post.user_id == path_id).all()
    return render_template('user.html', user=user, posts=posts)

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
    return redirect('/users')

# Deletes all of the user's posts (to not hit foreign key constraint) along with the user and redirects 
# the user to '/users'.
@app.route('/users/<ind>/delete', methods=["POST"])
def deleteUser(ind):
    path_id = int(request.path.replace('/users/', '').replace('/delete', ''))
    with app.app_context():
        all_posts = Post.query.filter(Post.user_id == path_id).all()
        if all_posts:
            for post in all_posts:
                post.query.delete()
                db.session.commit()
        User.query.filter_by(id=path_id).delete()
        db.session.commit()
    return redirect('/users')

# Displays the "add post" form and allows the user to add a new post upon click
@app.route('/users/<users_id>/posts/new')
def display_add_post(users_id):
    path_id = int(request.path.replace('/users/', '').replace('/posts/new', ''))
    with app.app_context():
        current_user = User.query.filter_by(id=path_id).first()
    return render_template('add_post.html', user=current_user)

# Upon click, takes the information from the form, creates a new Post instance, adds/commits
# to db.session and redirects user to the user detail page
@app.route('/users/<users_id>/posts/new', methods=["POST"])
def handle_add_post(users_id):
    title = request.form.get('title')
    content = request.form.get('content')
    path_id = int(request.path.replace('/users/', '').replace('/posts/new', ''))
    red = '/users/' + str(path_id)
    with app.app_context():
        new_post = Post(title, content, path_id)
        db.session.add(new_post)
        db.session.commit()
    return redirect(red)

# Displays a post from a user and allows user to either go back to the user detail page,
# edit the post or delete the post.
@app.route('/posts/<post_id>')
def display_post(post_id):
    path_id = int(request.path.replace('/posts/', ''))
    with app.app_context():
        current_post = Post.query.filter_by(id=path_id).first()
        current_user = User.query.filter(User.id == current_post.user_id).first()
    return render_template('post.html', post=current_post, user=current_user)

# Displays a form that allows a user to either edit the information in the post, or go back to the
# user detail page
@app.route('/posts/<post_id>/edit')
def display_edit_post(post_id):
    path_id = int(request.path.replace('/posts/', '').replace('/edit', ''))
    with app.app_context():
        current_post = Post.query.filter_by(id=path_id).first()
        current_user = User.query.filter(User.id == current_post.user_id).first()
    return render_template('edit_post.html', post=current_post, user=current_user)

# Upon click, takes the information from the form, edits the Post instance, adds/commits to
# db.session and redirects user to the post
@app.route('/posts/<post_id>/edit', methods=["POST"])
def handle_edit_post(post_id):
    path_id = int(request.path.replace('/posts/', '').replace('/edit', ''))
    title = request.form.get('title')
    content = request.form.get('content')
    with app.app_context():
        current_post = Post.query.get(path_id)
        red = '/posts/' + str(current_post.id)
        current_post.title = title
        current_post.content = content
        current_post.last_edited = datetime.now()
        db.session.commit()
    return redirect(red)

# Upon click, deletes the post instance and redirects user to the user detail page
@app.route('/posts/<post_id>/delete', methods=["POST"])
def deletePost(post_id):
    path_id = int(request.path.replace('/posts/', '').replace('/delete', ''))
    with app.app_context():
        current_post = Post.query.filter_by(id=path_id).first()
        red = '/users/' + str(current_post.user_id)
        Post.query.filter_by(id=path_id).delete()
        db.session.commit()
    return redirect(red)