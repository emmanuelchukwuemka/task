import unittest
import sys
import os
import json

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import create_app
from models.user import db, User
from models.task import Task

class TasksTestCase(unittest.TestCase):
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
            
            # Store user ID for later use
            self.user_id = user.id
            
            # Create a test task
            task = Task(
                title='Test Task',
                description='This is a test task',
                user_id=self.user_id
            )
            db.session.add(task)
            db.session.commit()
            
            # Store task ID for later use
            self.task_id = task.id
            
            # Create JWT token for authentication
            from flask_jwt_extended import create_access_token
            self.access_token = create_access_token(identity=self.user_id)
    
    def tearDown(self):
        """Clean up test environment."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_tasks(self):
        """Test getting tasks."""
        response = self.client.get('/api/tasks',
                                  headers={'Authorization': f'Bearer {self.access_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('tasks', data)
        self.assertGreaterEqual(len(data['tasks']), 1)
    
    def test_create_task(self):
        """Test creating a new task."""
        response = self.client.post('/api/tasks',
                                  headers={'Authorization': f'Bearer {self.access_token}'},
                                  json={
                                      'title': 'New Test Task',
                                      'description': 'This is a new test task',
                                      'status': 'pending',
                                      'priority': 'medium'
                                  },
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('task', data)
        self.assertEqual(data['task']['title'], 'New Test Task')
    
    def test_get_task_by_id(self):
        """Test getting a specific task."""
        response = self.client.get(f'/api/tasks/{self.task_id}',
                                  headers={'Authorization': f'Bearer {self.access_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('task', data)
        self.assertEqual(data['task']['id'], self.task_id)
    
    def test_update_task(self):
        """Test updating a task."""
        response = self.client.put(f'/api/tasks/{self.task_id}',
                                  headers={'Authorization': f'Bearer {self.access_token}'},
                                  json={
                                      'title': 'Updated Test Task',
                                      'status': 'completed'
                                  },
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('task', data)
        self.assertEqual(data['task']['title'], 'Updated Test Task')
        self.assertEqual(data['task']['status'], 'completed')
    
    def test_delete_task(self):
        """Test deleting a task."""
        response = self.client.delete(f'/api/tasks/{self.task_id}',
                                    headers={'Authorization': f'Bearer {self.access_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()