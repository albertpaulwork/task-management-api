from fastapi.testclient import TestClient
from app.main import app
import random

client = TestClient(app)

def test_create_user():
    """
    Test user registration
    """
    random_num = random.randint(1000, 9999)

    response = client.post(
        '/users',
        json={
            'email': f'newtest{random_num}@email.com',
            'username': f'newtestuser{random_num}',
            'password': 'newtestpass'
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data['email'] == f'newtest{random_num}@email.com'
    assert data['username'] == f'newtestuser{random_num}'
    assert 'id' in data

def test_create_duplicate_user():
    """
    Test duplicate email registration fails
    """
    
    # First user
    client.post(
        '/users/',
        json={
            'email': 'duplicate@email.com',
            'username': 'duplicateuser',
            'password': 'duplicatepass'
        }
    )

    # Duplicate email
    response = client.post(
        '/users/',
        json={
            'email': 'duplicate@email.com',
            'username': 'duplicateuser2',
            'password': 'duplicatepass2'
        }
    )

    assert response.status_code == 400
    assert 'already registered' in response.json()['detail']

def test_login():
    """Test user login"""

    # Create user first
    client.post(
        '/users/',
        json={
            'email': 'logintest@email.com',
            'username': 'logintestuser',
            'password': 'logintestpass'
        }
    )

    # Login
    response = client.post(
        '/auth/login',
        data={
            'username': 'logintest@email.com',
            'password': 'logintestpass'
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'

def test_login_invalid_credentials():
    """
    Test login with wrong password
    """
    response = client.post(
        '/auth/login',
        data={
            'username': 'nonexistent@email.com',
            'password': 'nonexistentpass'
        }
    )

    assert response.status_code == 401
