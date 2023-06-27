from unittest import TestCase
from app import app
from models import db, User, initData

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()
    initData()

class UserModelTestCase(TestCase):
    def setUp(self):
        with app.app_context():
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
    def test_delete(self):
        with app.test_client() as c:
            response = c.post('/users/1/delete')
            # tests if route redirects
            self.assertEqual(response.status_code, 302)
            # tests if route actually deletes row where id = 1
            self.assertFalse(User.query.filter_by(id=1).first())