from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas, models, auth

from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional

app = FastAPI(title='Task Management API', version='1.0.0')

@app.get('/')
def read_root():
    return {'message': 'Task Management API'}

@app.post('/users/', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered'
        )
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already taken'
        )
    return crud.create_user(db=db, user=user)

@app.get('/users/', response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get('/users/{user_id}', response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user

@app.post('/auth/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token = auth.create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}

# Project endpoints
@app.post('/projects/', response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    return crud.create_project(db=db, project=project, owner_id=current_user.id)

@app.get('/projects/', response_model=List[schemas.ProjectResponse])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    projects = crud.get_projects(db=db, owner_id=current_user.id, skip=skip, limit=limit)
    return projects

@app.get('/projects/{project_id}', response_model=schemas.ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    project = crud.get_project(db=db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found')
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authorized to access this project')
    return project

@app.put('/projects/{project_id}', response_model=schemas.ProjectResponse)
def update_project(
    project_id: int,
    project: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    db_project = crud.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail='Project not found')
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authorized to update this project')
    return crud.update_project(db=db, project_id=project_id, project=project)
    
@app.delete('/projects/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    db_project = crud.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail='Project not found')
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authorized to delete this project')
    crud.delete_project(db=db, project_id=project_id)

# Task endpoints
@app.post('/tasks/', response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    # Verify user owns the project
    project = crud.get_project(db, task.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authorized to add tasks to this project')
    return crud.create_task(db=db, task=task, created_by=current_user.id)

@app.get('/tasks/project/{project_id}', response_model=List[schemas.TaskResponse])
def get_project_tasks(
    project_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    # Verify user owns the project
    project = crud.get_project(db, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authorized to view this project')
    query = db.query(models.Task).filter(models.Task.project_id == project_id)

    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)

    return query.offset(skip).limit(limit).all()

@app.get('/tasks/project/{project_id}/stats')
def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    
    # Verify user owns the project
    project = crud.get_project(db, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authorized to view this project')
    
    tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()

    stats = {
        'total_tasks': len(tasks),
        'todo': len([t for t in tasks if t.status == 'todo']),
        'in_progress': len([t for t in tasks if t.status == 'in_progress']),
        'done': len([t for t in tasks if t.status == 'done']),
        'high_priority': len([t for t in tasks if t.priority == 'high']),
        'medium_priority': len([t for t in tasks if t.priority == 'medium']),
        'low_priority': len([t for t in tasks if t.priority == 'low']),
        'unassigned': len([t for t in tasks if t.assigned_to is None])
    }

    return stats

@app.get('/tasks/my-tasks', response_model=List[schemas.TaskResponse])
def get_my_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    query = db.query(models.Task).filter(models.Task.assigned_to == current_user.id)
    
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)

    return query.offset(skip).limit(limit).all()

@app.get('/tasks/{task_id}', response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    # Verify user owns the project
    project = crud.get_project(db, task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authorized to view this task')
    return task

@app.put('/tasks/{task_id}', response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail='Task not found')
    # Verify user owns the project
    project = crud.get_project(db, db_task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authorized to update this task')
    return crud.update_task(db=db, task_id=task_id, task=task)

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail='Task not found')
    # Verify user owns the project
    project = crud.get_project(db, db_task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authorized to delete this task')
    crud.delete_task(db=db, task_id=task_id)
