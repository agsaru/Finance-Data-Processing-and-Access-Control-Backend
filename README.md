# Finance Data Processing and Access Control Backend

A robust FastAPI-based backend service for managing financial transactions, user accounts, and role-based access control (RBAC). It features secure JWT authentication, data filtering based on user roles, and analytical dashboard endpoints.

## Features

* **Authentication & Security**: Secure user signup, login, and JWT-based endpoint protection using `passlib` and `python-jose`.
* **Role-Based Access Control (RBAC)**: Three distinct user roles (`viewer`, `analyst`, `admin`) with strict permission checking. 
    * **Admin**: Full CRUD access to all users and financial records. Sees global data on dashboards.
    * **Analyst**: Can view their own financial records and personal dashboard summaries.
    * **Viewer**: Default restricted role.
* **Financial Record Management**: Track income and expenses with categories, descriptions, and timestamps.
* **Dashboard & Analytics**: Endpoints for total summaries, category-wise breakdown, and recent transactions.
* **Database**: PostgreSQL integration via `SQLModel` (SQLAlchemy + Pydantic).

## Tech Stack

* **Framework**: FastAPI
* **ORM**: SQLModel
* **Database**: PostgreSQL (`psycopg2-binary`)
* **Authentication**: JWT, bcrypt (`passlib`)
* **Package Management**: `pyproject.toml` (setuptools)
* **Python Version**: >= 3.9

## Prerequisites

* Python 3.9 or higher
* PostgreSQL database running locally or remotely

## Setup & Installation

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd finance-backend
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the project dependencies:**
   Since the project uses a `pyproject.toml`, you can install it via:
   ```bash
   pip install -e .
   ```

4. **Environment Configuration:**
   Create a `.env` file in the root of your project and configure the following variables:
   ```env
   DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
   JWT_SECRET_KEY=your_super_secret_key_here
   ```

## Running the Application

You can start the FastAPI server by running the `main.py` file:

```bash
cd src
python main.py
```

Alternatively, use Uvicorn directly from the `src` directory:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The application will be accessible at: `http://127.0.0.1:8000`

## API Documentation

Once the server is running, FastAPI automatically generates interactive API documentation.
* **Swagger UI**: `http://127.0.0.1:8000/docs`
* **ReDoc**: `http://127.0.0.1:8000/redoc`

## Project Structure

```text
├── pyproject.toml
├── README.md
└── src/
    ├── main.py                 # Application entry point & router aggregation
    ├── config/
    │   ├── database.py         # DB engine and session management
    │   └── security.py         # JWT verification, hashing, and RBAC dependencies
    ├── models/
    │   ├── transaction.py      # SQLModel for Financial Records
    │   └── user.py             # SQLModel for Users
    ├── routes/
    │   ├── auth.py             # Login and Signup endpoints
    │   ├── dashboard.py        # Analytics and summary endpoints
    │   ├── transaction.py      # Financial records CRUD endpoints
    │   └── user.py             # User management endpoints
    ├── schemas/
    │   ├── auth.py             # Pydantic schemas for Auth (Login/Signup)
    │   ├── transaction.py      # Pydantic schemas for Transactions
    │   └── user.py             # Pydantic schemas for Users
    └── services/
        ├── auth.py             # Business logic for auth
        ├── dashboard.py        # Business logic for aggregations/summaries
        ├── transaction.py      # Business logic for transactions
        └── user.py             # Business logic for user management
```