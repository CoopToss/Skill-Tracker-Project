import unittest
from app import create_app, db
from app.models import User

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_signup(self):
        with self.app.test_client() as client:
            response = client.post('/signup', data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 302)  # redirect to dashboard

            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertTrue(user.check_password('password123'))

    def test_user_login(self):
        with self.app.test_client() as client:
            response = client.post('/signup', data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 302)

            response = client.post('/login', data={
                'email': 'test@example.com',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 302)  # redirect to dashboard

if __name__ == '__main__':
    unittest.main()
