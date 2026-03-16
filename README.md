# example-fastapi

A RESTful API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, featuring user authentication, post management, and a voting system.

## Features

- JWT-based authentication
- User registration and management
- Post CRUD operations
- Vote on posts
- Alembic database migrations
- Password hashing with bcrypt

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.104.1 |
| ORM | SQLAlchemy 2.0.22 |
| Database | PostgreSQL |
| Migrations | Alembic |
| Auth | JWT (python-jose) |
| Password Hashing | bcrypt 4.1.1 |
| Validation | Pydantic 2.5.0 |
| Server | Uvicorn 0.24.0 |

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

```bash
git clone https://github.com/kyaw-khaing77/example-fastapi.git
cd example-fastapi
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run Migrations

```bash
alembic upgrade head
```

### Start the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive docs: `http://localhost:8000/docs`

## API Endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | Login and receive JWT token |

### Users

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/users/` | Register a new user | No |
| GET | `/users/` | Get all users | No |
| GET | `/users/{id}` | Get user by ID | No |
| PUT | `/users/{id}` | Update user | No |
| DELETE | `/users/{id}` | Delete user | No |

### Posts

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/posts/` | Get all posts | Yes |
| GET | `/posts/{id}` | Get post by ID | Yes |
| POST | `/posts/` | Create a post | Yes |
| PUT | `/posts/{id}` | Update a post | Yes |
| DELETE | `/posts/{id}` | Delete a post | Yes |

### Votes

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/votes/` | Vote on a post | Yes |

## Project Structure

```
.
├── main.py               # App entry point
├── alembic/              # Database migrations
├── alembic.ini
├── requirements.txt
└── app/
    ├── config.py         # Environment settings
    ├── database.py       # DB connection
    ├── schemas.py        # Pydantic models
    ├── models/
    │   ├── post.py
    │   ├── user.py
    │   └── vote.py
    └── routes/
        ├── auth.py
        ├── oauth.py
        ├── posts.py
        ├── users.py
        └── votes.py
```
