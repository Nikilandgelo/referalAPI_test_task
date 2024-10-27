# 🌐 Project Overview
This repository contains a `FastAPI` application for a referral system, featuring `JWT` authentication, unique referral code generation, user management, and referral tracking. It’s designed for efficient user registration and referral management within a modern, scalable API framework.

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Nikilandgelo/referalAPI_test_task/CI.yml?style=for-the-badge&logo=githubactions&logoColor=white&label=CI&labelColor=blue)

## 🚀 Key Features
- 🔐 JWT Authentication: Secure user authentication and session management.
- 🔗 Referral Code Generation: Generates unique referral codes for each user.
- 📊 Referral Tracking: Monitors referrals and rewards users based on successful referrals.
- 🐳 Dockerized Environment: Simplifies deployment with Docker for reproducible environments.

## 💻 Technologies Used
| [**Python 3.13**](https://www.python.org/)      | [**FastAPI**](https://fastapi.tiangolo.com)     | [**JWT (JSON Web Tokens)**](https://jwt.io/) | [**pip-tools**](https://github.com/jazzband/pip-tools) | [**PostgreSQL**](https://www.postgresql.org/) |  [**Docker**](https://docs.docker.com/)              | 
| ----------------------------------------------- | ----------------------------------------------- | -------------------------------------------- | ------------------------------------------------------ | ----------------------------------------------| ---------------------------------------------------- |
| The main language used for building the project | A high-performance, Python-based API framework. | For secure authentication                    | For managing Python dependencies                       | Database for user and referral data storage   | Containerize the application and manage dependencies |

## 🛠️ Setup Instructions

### 📋 Prerequisites
- `Docker` and `Docker Compose` are installed.
- Create a `.env` file in the root directory with the following environment variables:
    
    ```env
    POSTGRES_PASSWORD=<your_password>
    POSTGRES_USER=postgres
    POSTGRES_DB=<your_db_name>
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432

    SECRET_KEY=<your_app_secret_key>
    ```
### 📦 Dependency Management with `pip-tools`
1. Install `pip-tools`:

    ```bash
    pip install pip-tools
    ```
2. Compile dependencies into a `requirements.txt` file:

    ```bash
    pip-compile
    ```
3. Synchronize the dependencies in the virtual environment:

    ```bash
    pip-sync
    ```
This ensures only specified dependencies are installed and removes unnecessary packages.

### 🚀 Running the Application
1. Clone the Repository:

    ```bash
    git clone https://github.com/Nikilandgelo/referalAPI_test_task.git
    cd referalAPI_test_task
    ```
2. Start Services with Docker Compose:

   ```bash
   docker compose up -d --build
    ```
    This will build and start the `PostgreSQL` and `FastAPI` application containers.
3. Access Services:
- **`FastAPI`**: On port `8000`.
- **`PostgreSQL`**: On port `5432`.

### 📖 API Documentation
The API documentation for all available endpoints can be accessed locally:
- **`Swagger UI`**: Visit `http://localhost:8000/docs` for interactive API documentation.
- **`ReDoc`**: Visit `http://localhost:8000/redoc` for alternative API documentation.
