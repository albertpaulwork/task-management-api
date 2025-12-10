from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_and_project():
    """
    Helper function to get auth token and create a project
    """ 

    # Create and login user
    client.post(
        '/users/',
        json={
            'email': 'tasktest@email.com',
            'username': 'tasktestuser',
            'password': 'tasktestpass'
        }
    )

    login_reponse = client.post(
        '/auth/login',
        data={
            'username': 'tasktest@email.com',
            'password': 'tasktestpass'
        }
    )

    token = login_reponse.json()['access_token']

    # Create project
    project_response = client.post(
        '/projects/',
        json={
            'name': 'Task Test Project',
            'description': 'For testing tasks'
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    project_id = project_response.json()['id']
    
    return token, project_id 

def test_create_task():
    """
    Test creating a task
    """
    token, project_id = get_auth_and_project()
    response = client.post(
        '/tasks/',
        json={
            'title': 'Test Task',
            'description': 'A test task',
            'status': 'todo',
            'priority': 'high',
            'project_id': project_id
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'Test Task'
    assert data['status'] == 'todo'
    assert data['priority'] == 'high'
    assert 'id' in data

def test_get_project_tasks():
    """
    Test getting tasks for a project
    """
    token, project_id = get_auth_and_project()

    # Create task
    client.post(
        '/tasks/',
        json={
            'title': 'Task 1',
            'status': 'todo',
            'priority': 'medium',
            'project_id': project_id
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    # Get task
    response = client.get(
        f'/tasks/project/{project_id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_filter_tasks_by_status():
    """
    Test filtering tasks by status
    """
    token, project_id = get_auth_and_project()

    # Create tasks with different statuses
    client.post(
        '/tasks/',
        json={'title': 'Todo Task', 'status': 'todo', 'priority': 'low', 'project_id': project_id},
        headers={'Authorization': f'Bearer {token}'}
    )

    client.post(
        '/tasks/',
        json={
            'title': 'Done Task',
            'status': 'done',
            'priority': 'low',
            'project_id': project_id
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    # Filter by status
    response = client.get(
        f'/tasks/project/{project_id}?status=todo',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    data = response.json()
    for task in data:
        assert task['status'] == 'todo'

def test_project_stats():
    """
    Test getting project statistics
    """
    token, project_id = get_auth_and_project()

    # Create multiple tasks
    client.post(
        '/tasks/',
        json={
            'title': 'Task 1',
            'status': 'todo',
            'priority': 'high',
            'project_id': project_id
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    client.post(
        '/tasks/',
        json={
            'title': 'Task 2',
            'status': 'done',
            'priority': 'low',
            'project_id': project_id
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    response = client.get(
        f'/tasks/project/{project_id}/stats',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    data = response.json()
    assert data['total_tasks'] == 2
    assert 'todo' in data
    assert 'done' in data
    assert 'high_priority' in data

def test_create_task_invalid_status():
    """
    Test creating task with invalid status fails
    """
    token, project_id = get_auth_and_project()
    
    response = client.post(
        '/tasks/',
        json={
            'title': 'Bad Task',
            'status': 'invalid_status',
            'priority': 'high',
            'project_id': project_id
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 422
