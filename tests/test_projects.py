from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    """
    Helper function to get auth token
    """

    # Create and login user
    client.post(
        '/users/',
        json={
            'email': 'projecttest@email.com',
            'username': 'projecttestuser',
            'password': 'projecttestpass'
        }
    )

    response = client.post(
        '/auth/login',
        data={
            'username': 'projecttest@email.com',
            'password': 'projecttestpass'
        }
    )

    return response.json()['access_token']

def test_create_project():
    """
    Test creating a project
    """
    token = get_auth_token()
    response = client.post(
        '/projects',
        json={
            'name': 'Test Project',
            'description': 'A test project'
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Test Project'
    assert data['description'] == 'A test project'
    assert 'id' in data
    assert 'owner_id' in data

def test_get_projects():
    """
    Test getting user projects
    """
    token = get_auth_token()

    # Create a project first
    client.post(
        '/projects/',
        json={
            'name': 'My Project',
            'description': 'Test'
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    # Get projects
    response = client.get(
        '/projects/',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_project_unauthorized():
    """
    Test getting project without auth fails
    """
    response = client.get('/projects/')
    
    assert response.status_code == 401
