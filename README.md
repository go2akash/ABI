# **ABI Backend — FastAPI, SQLAlchemy, Alembic, Docker**
A production-style backend built with **FastAPI**, **SQLAlchemy ORM**, **Alembic migrations**, and **Docker Compose**.  
Designed using a clean **service-layer architecture** and dependency-managed with **uv** for reproducible builds.

## **🚀 Features (Implemented & Verified)**

### **API & Backend**
- FastAPI REST API with automatic Swagger UI
- Modular router-based API structure
- Pydantic request/response schemas
- Centralized configuration using environment variables
- Service-layer architecture (clean separation of concerns)

### **Database**
- PostgreSQL integration
- SQLAlchemy ORM models + session management
- Alembic migrations (upgrade/downgrade/versioning)
- Autogenerate schema migrations

### **Tooling**
- `uv` for environment + package management  
- `uv.lock` for deterministic builds  
- Pinned dependencies in `pyproject.toml`

### **Docker (Implemented)**
- Dockerfile for building the FastAPI application  
- Docker Compose orchestration  
- Auto-start Postgres + API  
- Containerized Alembic migrations  

## **📁 Project Structure**
```
app/
 ├── api/                
 ├── core/               
 ├── models/             
 ├── schemas/            
 ├── services/           
 └── main.py             

migrations/              
alembic.ini              
Dockerfile               
docker-compose.yml       
pyproject.toml           
uv.lock                  
```

## **🛠 Requirements**
- Python 3.10+  
- uv   
- Docker & Docker Compose  

# **🔥 Quick Start (Using Docker — Recommended)**

### **1. Create your `.env` file**
```
cp .env.example .env
```

```
DATABASE_URL=postgresql+psycopg2://user:password@db:5432/abi_db
ENV=development
SECRET_KEY=your-secret
```

### **2. Start the entire stack**
```bash
docker compose up --build -d
```

👉 http://localhost:8000/docs

### **3. Run Alembic migrations**
```bash
docker compose exec api uv run alembic upgrade head
```

# **🧪 Local Development**

### Install deps:
```bash
uv sync
```

### Run migrations:
```bash
uv run alembic upgrade head
```

### Start server:
```bash
uv run uvicorn app.main:app --reload
```

# **📦 Database Migrations**
```bash
uv run alembic revision --autogenerate -m "msg"
uv run alembic upgrade head
uv run alembic downgrade -1
```

# **📐 Architecture Overview**
1. API Layer  
2. Service Layer  
3. Data Layer  
4. Migration Layer  
5. Config Layer  

```
Client → FastAPI Router → Pydantic → Service Layer → Database → Response
```

# **🐳 Docker Overview**
- Dockerfile uses uv  
- Compose starts API + DB  
- Env vars loaded via .env  

# **🧠 What This Project Demonstrates**
- Clean architecture  
- Containerization  
- ORM + Alembic migrations  
- Modern Python tooling  

# **👤 Author**
Akash Mondal  
Backend Developer | FastAPI | Docker | PostgreSQL
