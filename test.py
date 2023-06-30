from unittest import TestCase
from app import app
from models import db, User, initData, Post, Tag, PostTag
from datetime import datetime


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()
    initData()

class UserModelTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            PostTag.query.delete()
            Tag.query.delete()
            Post.query.delete()
            User.query.delete()
    def tearDown(self):
        with app.app_context():
            db.session.rollback()
    def test_access_users(self):
        with app.test_client() as c:
            response = c.get('/users')
            # tests if route is successful
            self.assertEqual(response.status_code, 200)
    def test_access_specific_user(self):
        with app.test_client() as c:
            response = c.get('/users/1')
            html = response.get_data(as_text=True)
            # tests if route is successful
            self.assertEqual(response.status_code, 200)
            # tests if the first name from the first row displays on the user page
            self.assertIn('<p>First Name: James</p>', html)
    def test_redirect_to_users(self):
        with app.test_client() as c:
            response = c.get('/')
            # tests if route redirects
            self.assertEqual(response.status_code, 302)
            # tests if route doesn't lead to page
            self.assertNotEqual(response.status_code, 200)
    def test_user_delete(self):
        with app.test_client() as c:
            response = c.post('/users/1/delete')
            # tests if route redirects
            self.assertEqual(response.status_code, 302)
            # tests if route actually deletes row in 'users' where id = 1
            self.assertFalse(User.query.filter_by(id=1).first())
    

class PostModelTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            PostTag.query.delete()
            Tag.query.delete()
            Post.query.delete()
            User.query.delete()
    def tearDown(self):
        with app.app_context():
            db.session.rollback()
    def test_access_post(self):
        with app.test_client() as c:
            response = c.get('/posts/1')
            html = response.get_data(as_text=True)
            # check if you can reach the post
            self.assertEqual(response.status_code, 200)
            # check if the data is actually in the post
            self.assertIn('<h1>My first post</h1>', html)
    def test_post_delete(self):
        with app.test_client() as c:
            response = c.post('/posts/1/delete')
            # test if route redirects
            self.assertEqual(response.status_code, 302)
            # tests if route actually deletes row in 'posts' where id = 1
            self.assertFalse(Post.query.filter_by(id=1).first())
    def test_access_add_post(self):
        with app.test_client() as c:
            response = c.get('/users/1/posts/new')
            # tests if you can reach the form to add a post
            self.assertEqual(response.status_code, 200)
    def test_process_add_post(self):
        with app.test_client() as c:
            response = c.post('/users/1/posts/new', data={
                'title': 'My second post',
                'content': 'This is my second post',
                'selected_tags': ['2', '3'],
            })
            # tests if the route redirects the user to '/users/1' (user detail page)
            #self.assertEqual(response.status_code, 302)
            # tests if post was added
            self.assertTrue(Post.query.filter_by(id=4).first())

class TagModelTestCase(TestCase):
    def setUp(self):
        with app.app_context(): 
            PostTag.query.delete()
            Tag.query.delete()
            Post.query.delete()
            User.query.delete()
    def tearDown(self):
        with app.app_context():
            db.session.rollback()
    def add_tag(self):
        with app.test_client() as c:
            response = c.post('/tags/new', data={
                'name': 'Test tag'
            })
            new_tag = Tag.query.filter(Tag.id == 4).first()
            # test if new tag was added
            self.assertEqual(new_tag.name, 'Test tag')
    def edit_tag(self):
        with app.test_client() as c:
            response = c.post('/tags/1/edit', data={
                'name': 'Edit Test'
            })
            edited_tag = Tag.query.filter(Tag.id == 1).first()
            # test if the route actually edits the tag's name
            self.assertEqual(edited_tag.name, 'Edit Test')
    def delete_tag(self):
        with app.test_client() as c:
            response = c.post('/tags/1/delete')
            # test if the route successfully redirects
            self.assertEqual(response.status_code, 302)
            # test if the route actually deletes the tag
            self.assertFalse(Tag.query.get(1))

class PostTagModelTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            PostTag.query.delete()
            Tag.query.delete()
            Post.query.delete()
            User.query.delete()
    def tearDown(self):
        with app.app_context():
            db.session.rollback()
    def add_a_tagged_post(self):
        with app.test_client() as c:
            response = c.post('/users/1/posts/new', data={
                'title': 'My second post',
                'content': 'This is my second post',
                'selected_tags': [1, 2]
            })
            # test if a new row was added to reference table 'tagged_posts'
            self.assertTrue(PostTag.query.filter(PostTag.post_id == 4).first())
            # test if more than one row was added to reference table 'tagged_posts'
            self.assertTrue(len(PostTag.query.filter(PostTag.post_id == 4).all()) > 1)
    def delete_a_tagged_post(self):
        with app.test_client() as c:
            response = c.post('/users/1/delete')
            # test if all rows in 'tagged posts' where post_id = 1 are deleted
            self.assertFalse(PostTag.query.filter(PostTag.post_id == 1).all())