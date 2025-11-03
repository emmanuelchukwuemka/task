import requests
import json

# Test the root endpoint
response = requests.get('http://localhost:5000/')
print("Root endpoint:")
print(response.status_code)
print(json.dumps(response.json(), indent=2))

# Test the health endpoint
response = requests.get('http://localhost:5000/health')
print("\nHealth endpoint:")
print(response.status_code)
print(json.dumps(response.json(), indent=2))

# Test registration
register_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test1234"
}

response = requests.post('http://localhost:5000/api/auth/register', json=register_data)
print("\nRegistration:")
print(response.status_code)
print(json.dumps(response.json(), indent=2))

# Test login
login_data = {
    "username": "testuser",
    "password": "Test1234"
}

response = requests.post('http://localhost:5000/api/auth/login', json=login_data)
print("\nLogin:")
print(response.status_code)
print(json.dumps(response.json(), indent=2))

# Store the access token for future requests
if response.status_code == 200:
    access_token = response.json()['access_token']
    print(f"\nAccess token: {access_token}")
    
    # Test creating a task
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending",
        "priority": "medium"
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post('http://localhost:5000/api/tasks', json=task_data, headers=headers)
    print("\nCreate task:")
    print(response.status_code)
    print(json.dumps(response.json(), indent=2))
    
    # Test getting tasks
    response = requests.get('http://localhost:5000/api/tasks', headers=headers)
    print("\nGet tasks:")
    print(response.status_code)
    print(json.dumps(response.json(), indent=2))