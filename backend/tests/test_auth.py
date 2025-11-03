import unittest
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import create_app
from models.user import db, User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create a test user
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
    
    def tearDown(self):
        """Clean up test environment."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_register_user(self):
        """Test user registration."""
        response = self.client.post('/api/auth/register', 
                                  json={
                                      'username': 'newuser',
                                      'email': 'newuser@example.com',
                                      'password': 'NewPass123'
                                  },
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('user', data)
        self.assertEqual(data['user']['username'], 'newuser')
    
    def test_register_duplicate_user(self):
        """Test registration with duplicate username."""
        response = self.client.post('/api/auth/register',
                                  json={
                                      'username': 'testuser',  # Already exists
                                      'email': 'newemail@example.com',
                                      'password': 'NewPass123'
                                  },
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertIn('message', data)
    
    def test_login_success(self):
        """Test successful login."""
        response = self.client.post('/api/auth/login',
                                  json={
                                      'username': 'testuser',
                                      'password': 'testpassword'
                                  },
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['username'], 'testuser')
    
    def test_login_failure(self):
        """Test failed login with wrong credentials."""
        response = self.client.post('/api/auth/login',
                                  json={
                                      'username': 'testuser',
                                      'password': 'wrongpassword'
                                  },
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()