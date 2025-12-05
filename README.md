# Task Management API

A production-ready RESTful API built with FastAPI for managing projects and tasks with secure authentication and role-based authorization.

## 🚀 Features

- **User Management**: Registration, authentication, and profile management
- **JWT Authentication**: Secure token-based authentication with OAuth2
- **Project Management**: Create, read, update, and delete projects
- **Task Management**: Full CRUD operations for tasks with assignment capabilities
- **Advanced Filtering**: Filter tasks by status, priority, and assignment
- **Project Statistics**: Real-time task statistics and progress tracking
- **Role-Based Access**: Users can only access and modify their own resources
- **Input Validation**: Enum-based validation for task status and priority
- **RESTful Design**: Clean API architecture following REST principles

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.116.1
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt via passlib
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **API Documentation**: OpenAPI (Swagger UI)

## 📋 Prerequisites

- Python 3.12.0
- PostgreSQL
- pip and virtualenv

## ⚙️ Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/albertpaulwork/task-management-api
cd task_management_api
```

2. **Create virtual environment**
```bash
python -m venv tma
source tma/bin/activate  # On Windows: tma\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL database**
```bash
createdb tma_db
```

5. **Configure environment variables**
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/tma_db
SECRET_KEY=your-super-secret-key-change-in-production
ENVIRONMENT=development
```

6. **Run database migrations**
```bash
alembic upgrade head
```

7. **Start the server**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## 📚 API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🔑 API Endpoints

### Authentication
- `POST /auth/login` - Login and receive JWT token

### Users
- `POST /users/` - Register new user (public)
- `GET /users/` - List all users (protected)
- `GET /users/{user_id}` - Get specific user (protected)

### Projects
- `POST /projects/` - Create new project
- `GET /projects/` - Get all user's projects
- `GET /projects/{project_id}` - Get specific project
- `PUT /projects/{project_id}` - Update project
- `DELETE /projects/{project_id}` - Delete project

### Tasks
- `POST /tasks/` - Create new task
- `GET /tasks/project/{project_id}` - Get project tasks (with filters)
- `GET /tasks/my-tasks` - Get tasks assigned to current user
- `GET /tasks/{task_id}` - Get specific task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task
- `GET /tasks/project/{project_id}/stats` - Get project statistics

### System
- `GET /health` - Health check endpoint

## 🔐 Authentication Flow

1. Register a new user via `POST /users/`
2. Login via `POST /auth/login` to receive a JWT token
3. Include the token in subsequent requests:
   - Header: `Authorization: Bearer <your_token>`
4. Tokens expire after 30 minutes

## 📊 Task Status & Priority

**Status Options:**
- `todo` - Task not started
- `in_progress` - Task in progress
- `done` - Task completed

**Priority Options:**
- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority

## 🧪 Example Usage

### Register a User
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### Login
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

### Create a Project
```bash
curl -X POST "http://127.0.0.1:8000/projects/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign",
    "description": "Redesign company website"
  }'
```

### Create a Task
```bash
curl -X POST "http://127.0.0.1:8000/tasks/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design homepage mockup",
    "description": "Create initial design concepts",
    "status": "todo",
    "priority": "high",
    "project_id": 1
  }'
```

### Filter Tasks
```bash
# Get high priority tasks
curl "http://127.0.0.1:8000/tasks/project/1?priority=high" \
  -H "Authorization: Bearer <your_token>"

# Get tasks in progress
curl "http://127.0.0.1:8000/tasks/project/1?status=in_progress" \
  -H "Authorization: Bearer <your_token>"
```

## 🗂️ Project Structure

```
task_management_api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and routes
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py           # Database operations
│   ├── auth.py           # Authentication logic
│   ├── enums.py          # Enum definitions
│   └── exceptions.py     # Custom exception classes
├── alembic/              # Database migrations
├── tests/                # Test files
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── .gitignore
└── README.md
```

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## 🚀 Deployment

### Using Docker (Coming Soon)
```bash
docker-compose up -d
```

### Manual Deployment
1. Set production environment variables
2. Run database migrations
3. Deploy to your preferred platform (Render, Railway, Heroku)

## 🔒 Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- SQL injection prevention via ORM
- Input validation with Pydantic
- Owner-based authorization for all resources
- Token expiration (30 minutes)

## 🤝 Contributing

This is a personal learning project, but suggestions are welcome!

## 📝 License

MIT License - feel free to use this project for learning purposes.

## 👤 Author

**Albert Paul**
- GitHub: [@albertpaulwork](https://github.com/albertpaulwork)
- LinkedIn: [albertpaulwork](https://www.linkedin.com/in/albertpaulwork/)

## 🙏 Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- Python community

---

⭐ If you found this project helpful, please give it a star!