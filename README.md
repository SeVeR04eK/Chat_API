# Chat API Backend (FastAPI + PostgreSQL + WebSockets)

A production-oriented real-time chat API with authentication, room management, and WebSocket-based messaging.

---

## Overview

This project implements a fully-featured backend service for real-time chat functionality. It follows clean architecture principles, separates concerns, and supports both REST API and WebSocket connections for seamless communication.

**Key goals:**

* Build a secure and scalable real-time chat system
* Demonstrate WebSocket integration with FastAPI
* Provide room-based messaging with persistence

---

## Tech Stack

* **Python 3.12+**
* **FastAPI** — high-performance async web framework
* **WebSockets** — real-time bidirectional communication
* **Uvicorn** — ASGI server
* **PostgreSQL** — relational database
* **SQLAlchemy (async)** — database abstraction
* **Alembic** — database migrations
* **Pydantic v2** — data validation & serialization
* **Pydantic Settings** — environment configuration
* **asyncpg** — async PostgreSQL driver
* **psycopg2-binary** — sync PostgreSQL driver for alembic
* **JWT (JSON Web Tokens)** — authentication
* **Passlib / bcrypt** — password hashing
* **python-multipart** — form/file uploads
* **Black** — code formatting
* **Docker / Docker Compose** — containerization
* **Git** — version control

---

## Features

### Authentication & Authorization

* User registration & login
* Password hashing (bcrypt)
* JWT-based authentication (access tokens)
* Refresh token rotation
* Protected endpoints via dependencies

---

### User Management

* Create Account
* Get Account Information
* Update Account Information
* Delete Account
* Get Online Users Count

---

### Room Management

* Create Room
* Get Rooms (filtering & pagination)
* Get Room by Name
* Delete Room

---

### Message Management

* Send Message (via WebSocket)
* Get Message History (via REST API)
* Message persistence in database
* Real-time message broadcasting to room members

---

### WebSocket Chat

* Real-time bidirectional messaging
* Room-based chat channels
* Connection management
* Automatic disconnection handling
* Message broadcasting to all room participants
* Join/leave notifications
* System messages for errors
* Dead connection cleanup
* JSON validation for incoming messages

---

### Security

* Password hashing
* Protected endpoints via dependencies
* JWT token validation
* Database connection limiting
* Proper HTTP status codes (401 / 403 / 400)
* Proper websocket status codes (1008 / 1011)

---

### Architecture

```
Chat_API/
├── app/                      # main application package
│   ├── api/                  # API layer (routing, dependencies)
│   │   ├── http/             # REST API routers
│   │   └── websockets/       # WebSocket handlers
│   ├── core/                 # configuration, settings, security
│   ├── db/                   # database connection, session, engine
│   ├── migrations/           # Alembic migrations
│   │   └── versions/         # generated migration files
│   ├── models/               # SQLAlchemy ORM models
│   ├── repository/           # data access layer (CRUD repositories)
│   ├── schemas/              # Pydantic request/response schemas
│   ├── services/             # business logic layer
│   ├── utils/                # helper utilities
│   └── main.py               # FastAPI application entry point
├── scripts/                  # helper scripts (startup)
├── alembic.ini               # Alembic configuration
├── LICENSE                   # project license
├── README.md                 # project documentation
├── .env                      # environment variables (not committed)
├── .gitignore                # Git ignore rules
├── Dockerfile                # Production image
├── docker-compose.yml        # Docker Compose configuration
├── .env.example              # Template of environment variables
└── requirements.txt          # project dependencies
```

**Principle:**
`route → service → repository → database`

---

## Database Design

### Users

* id
* username (unique)
* password (hashed)

---

### Rooms

* id
* name (unique)
* created_at

---

### Messages

* id
* text
* user_id (FK)
* room_name (FK)
* created_at

---

### Refresh Tokens

* id
* user_id (FK)
* token
* expires_at

---

### Relationships

* Room ↔ Message: one-to-many (room contains multiple messages, CASCADE delete)
* User ↔ Message: one-to-many (user sends multiple messages, CASCADE delete)
* Message uses room_name as foreign key (not room_id)

---

## Authentication Flow

1. User registers/logs in
2. Server validates credentials
3. JWT token is issued
4. Client sends token in headers for REST API
5. WebSocket connection authenticates via query parameter
6. Protected endpoints validate token

---

## WebSocket Connection Flow

1. Client connects to `/ws/chat/{room_id}?token={access_token}`
2. Server validates JWT token
3. Client joins the specified room
4. Client can send/receive messages in real-time
5. Server broadcasts messages to all connected clients in the room
6. Connection closes on disconnect or error

---

## API Examples

### Auth

![Auth](screenshots/auth.png)

#### POST /auth/authentication

Request):
```
Content-Type: application/x-www-form-urlencoded

username=user
password=user12345
```

Response:
```
{
    "refresh_token": "example.refresh.token",
    "access_token": "example.access.token",
    "token_type": "bearer"
}
```

#### POST /auth/refresh

Request:
```
{
  "refresh_token": "example.refresh.token"
}
```

Response:
```
{
    "refresh_token": "example.new.refresh.token",
    "access_token": "example.new.access.token",
    "token_type": "bearer"
}
```

---

### User

![User](screenshots/user.png)

#### GET /user/me

Request:
```
Authorization: Bearer <access_token>
```

Response:
```
{
    "username": "user",
    "id": 1
}
```

#### POST /user/me

Request:
```
{
  "username": "user",
  "password": "user12345",
  "password_confirm": "user12345"
}
```

Response:
```
{
  "username": "user",
  "id": 1
}
```

#### PATCH /user/me

Request:
```
Authorization: Bearer <access_token>

{
  "username": "new_user",
  "password": "user12345",
  "password_confirm": "user12345"
}
```

Response:
```
{
    "username": "new_user",
    "id": 1,
    "is_active": true
}
```

#### DELETE /user/me

Request:
```
Authorization: Bearer <access_token>
```

#### GET /user/online

Request:

Response:
```
{
    "count": 0
}
```

---

### Rooms

![Room](screenshots/room.png)

#### GET /rooms

Request:
```
Authorization: Bearer <access_token>
```

Response:
```
[
    {
        "id": 1,
        "name": "General",
        "created_at": "2026-06-25T12:14:32.822814Z"
    }
]
```

#### POST /rooms

Request:
```
Authorization: Bearer <access_token>

{
  "name": "General"
}
```

Response:
```
{
    "id": 1,
    "name": "General",
    "created_at": "2026-06-25T12:14:32.822814Z"
}
```

#### Filters

```
GET /rooms?limit=10&offset=0&from_newest=True
```

#### GET /rooms/{room_id}

Request:
```
Authorization: Bearer <access_token>
```

Response:
```
{
    "id": 1,
    "name": "General",
    "created_at": "2026-06-25T12:14:32.822814Z"
}
```

#### DELETE /rooms/{room_id}

Request:
```
Authorization: Bearer <access_token>
```

---

### Messages (History)

#### GET /history/{name}

Request:
```
Authorization: Bearer <access_token>
```

Response:
```
[
  {
    "id": 1,
    "room_name": "General",
    "user_id": 1,
    "text": "text",
    "created_at": "2026-06-23T19:58:15.774061Z"
  }
]
```

---

### WebSocket Chat

#### Connect to WebSocket

```
ws://localhost:8000/ws/{room_name}?token={access_token}
```

#### Send Message

Client sends:
```
{
  "text": "Hello everyone!"
}
```

Server broadcasts to all room members:
```
{
    "text": "Hello everyone",
    "type": "message",
    "username": "user"
}
```

#### Message Types

The WebSocket supports different message types:

* **message** - Regular chat message from user
* **join** - Notification when a user joins the room
* **leave** - Notification when a user leaves the room
* **error** - System error messages (invalid JSON, invalid format, etc.)

Example join notification:
```
{
    "type": "join",
    "text": "user has joined the room",
    "username": "user"
}
```

Example error message:
```
{
    "type": "error",
    "text": "Invalid JSON format",
    "username": "system"
}
```

#### Filters

```
GET /history/{room_name}?limit=50&offset=0&from_newest=True
```

---

## Running the Project

The project supports two execution modes:

**Docker** — the primary mode for local development and production

**Manual Setup** — run the application without Docker using your own environment configuration

### Docker Mode

#### 1. Clone repository

```
git clone https://github.com/SeVeR04eK/Chat_API.git
cd Chat_API
```

---

#### 2. Generate secret key

```
python app/core/secret.py
```

---

#### 3. Setup environment variables

Create `.env` file using `.env.example` template:

```
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/chat_api
SECRET_KEY=your_secret_key
```

---

#### 4. Run docker compose

```
docker compose up --build
```

---

#### 5. Open docs

```
http://127.0.0.1:8000/docs
```

---

### Manual Setup

#### 1. Clone repository

```
git clone https://github.com/SeVeR04eK/Chat_API.git
cd Chat_API
```

---

#### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

---

#### 3. Install dependencies

```
pip install -r requirements.txt
```

---

#### 4. Create database

```
CREATE DATABASE chat_api;   #psql
```

---

#### 5. Generate secret key

```
python app/core/secret.py
```

---

#### 6. Setup environment variables

Create `.env` file using `.env.example` template:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/chat_api
SECRET_KEY=your_secret_key
```

---

#### 7. Run migrations

```
alembic upgrade head
```

---

#### 8. Start server

```
uvicorn app.main:app --reload
```

---

#### 9. Open docs

```
http://127.0.0.1:8000/docs
```

---

## Key Engineering Decisions

* Separation of concerns (routes vs services vs repository)
* Dependency injection via FastAPI
* WebSocket for real-time communication instead of polling
* Alembic migrations instead of manual DB changes
* Explicit error handling (401 vs 403 vs 400) / (1008, 1011)
* Dockerized architecture for consistent development
* Automatic migrations on container startup via startup script
* Database connection limiting for performance (asyncio semaphore)
* Proper database engine disposal in lifespan for clean shutdown
* Configurable pagination limits and offsets for API responses
* Environment-based configuration with Pydantic Settings
* Message persistence for chat history
* CASCADE delete for maintaining data integrity
* Timezone-aware datetime fields for accurate timestamps
* Global exception handlers for database integrity errors
* CORS middleware enabled for cross-origin requests
* Connection manager pattern for WebSocket state management
* Room name-based routing instead of numeric IDs
* FastAPI tags for organized API documentation

---

## Why This Project Matters

This project demonstrates:

* Real-time WebSocket integration with FastAPI
* Real-world backend architecture
* Secure authentication practices
* Database design for chat applications
* API design and filtering
* Room-based messaging patterns
* Ability to containerize applications using Docker
* Knowledge of environment variables and secrets management
* Connection management and broadcasting patterns
* Proper async/await patterns throughout the codebase
* Pydantic schemas for request/response validation
* Repository pattern for data access abstraction
* Service layer for business logic separation
* Dependency injection for testability and modularity

## License

MIT License
