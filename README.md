# ACEest Fitness Management System

A full-stack fitness management application with a Flask REST API backend, Tkinter desktop UI, and a complete DevOps pipeline using Jenkins and GitHub Actions.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Local Setup and Execution](#local-setup-and-execution)
  - [Prerequisites](#prerequisites)
  - [Running the Flask API Locally](#running-the-flask-api-locally)
  - [Running the UI Locally](#running-the-ui-locally)
  - [Running with Docker Compose](#running-with-docker-compose)
- [Running Tests Manually](#running-tests-manually)
  - [Install Test Dependencies](#install-test-dependencies)
  - [Run All Tests](#run-all-tests)
  - [Run Specific Test Suites](#run-specific-test-suites)
  - [Run Tests with Coverage Report](#run-tests-with-coverage-report)
  - [Test Markers](#test-markers)
- [API Endpoints](#api-endpoints)
- [CI/CD Pipeline Overview](#cicd-pipeline-overview)
  - [Jenkins Pipeline](#jenkins-pipeline)
  - [GitHub Actions](#github-actions)
- [Project Structure](#project-structure)

---

## Project Overview

ACEest is a fitness management system that tracks members, workouts, subscriptions, and trainer assignments. It exposes a REST API (Flask + SQLAlchemy) and a desktop GUI (Tkinter) that communicates with the API. The project is containerised with Docker and includes automated CI/CD pipelines for both Jenkins (Windows) and GitHub Actions (Linux).

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| API Framework | Flask 2.3.3, Flask-SQLAlchemy, Flask-CORS |
| Database | SQLite |
| Desktop UI | Tkinter + Matplotlib (served over VNC via noVNC) |
| Containerisation | Docker (multi-stage), Docker Compose |
| Reverse Proxy | Nginx |
| CI/CD | Jenkins (Windows), GitHub Actions (Linux/Ubuntu) |
| Testing | Pytest, pytest-cov, pytest-mock |
| Code Quality | Flake8, Black, Pylint |
| Python Versions | 3.9, 3.10, 3.11 |

---

## Local Setup and Execution

### Prerequisites

- Python 3.9 or higher
- pip
- (Optional) Docker Desktop for containerised setup

### Running the Flask API Locally

```bash
# 1. Clone the repository
git clone <repo-url>
cd DevOps_Assignment

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
cd flask_app
pip install -r requirements.txt

# 4. Run the API server
flask run
# Or explicitly:
python -m flask run --host=0.0.0.0 --port=5000
```

The API will be available at `http://localhost:5000`.

### Running the UI Locally

The UI requires Tkinter (bundled with most Python distributions) and the Flask API to be running.

```bash
cd ui_app
pip install -r requirements.txt

# Set the API base URL (defaults to http://localhost:5000)
export API_BASE_URL=http://localhost:5000   # macOS/Linux
set API_BASE_URL=http://localhost:5000      # Windows

python aceest_ui.py
```

### Running with Docker Compose

The full stack (API + UI via VNC + Nginx reverse proxy + Jenkins) can be started with a single command:

```bash
# Start all services
docker-compose up --build

# Start only the API and Nginx
docker-compose up flask-app nginx

# Stop all services
docker-compose down
```

| Service | URL |
|---------|-----|
| Flask API | http://localhost:5000 |
| UI (noVNC) | http://localhost:6080 |
| Nginx proxy | http://localhost:80 |
| Jenkins | http://localhost:8081 |

To start only the Jenkins stack:

```bash
docker-compose -f docker-compose.jenkins.yml up --build
```

---

## Running Tests Manually

All test commands should be run from the `flask_app/` directory.

```bash
cd flask_app
```

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suites

```bash
# Routes (API endpoint tests)
pytest tests/test_routes.py -v

# Service layer tests
pytest tests/test_services.py -v

# Model tests
pytest tests/test_models.py -v

# Utility function tests
pytest tests/test_utils.py -v
```

### Run Tests with Coverage Report

```bash
# Terminal report
pytest tests/ -v --cov=. --cov-report=term-missing

# HTML report (opens htmlcov/index.html)
pytest tests/ -v --cov=. --cov-report=html:htmlcov

# XML report (used by CI/CD)
pytest tests/ -v --cov=. --cov-report=xml:coverage.xml
```

The project enforces a **minimum coverage threshold of 60%**.

### Test Markers

Tests are tagged with markers defined in `pytest.ini`:

```bash
# Run only unit tests
pytest tests/ -m unit

# Run only integration tests
pytest tests/ -m integration

# Run edge case and negative tests
pytest tests/ -m "edge_case or negative"

# Exclude slow tests (mirrors CI behaviour)
pytest tests/ -m "not slow"

# Exclude slow and integration tests (mirrors Jenkins behaviour)
pytest tests/ -m "not slow and not integration"
```

| Marker | Description |
|--------|-------------|
| `unit` | Isolated component tests with no external dependencies |
| `integration` | Multi-component tests that hit the database |
| `edge_case` | Boundary value and unusual input tests |
| `negative` | Error-path and validation failure tests |
| `slow` | Tests with extended runtime, excluded from fast CI runs |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/api/members` | List all members |
| GET | `/api/members/<id>` | Get member by ID |
| POST | `/api/members` | Create a new member |
| PUT | `/api/members/<id>` | Update a member |
| DELETE | `/api/members/<id>` | Delete a member |
| GET | `/api/members/<name>/summary` | Get member summary |
| GET | `/api/members/trainers` | List all trainers |
| POST | `/api/members/trainers` | Create a trainer |
| PUT | `/api/members/trainers/<id>` | Update a trainer |
| DELETE | `/api/members/trainers/<id>` | Delete a trainer |
| GET | `/api/workouts` | List workouts (filter by `?member=name`) |
| GET | `/api/workouts/<id>` | Get workout with exercises |
| POST | `/api/workouts` | Create a workout |
| PUT | `/api/workouts/<id>` | Update a workout |
| DELETE | `/api/workouts/<id>` | Delete a workout |
| GET/POST/PUT/DELETE | `/api/subscriptions` | Subscription CRUD |

---

## CI/CD Pipeline Overview

### Jenkins Pipeline

**File:** `Jenkinsfile`  
**Target:** Windows agent with Python 3.9 installed at `C:\Python39\python.exe`

The Jenkins declarative pipeline runs the following stages in order:

| Stage | What It Does |
|-------|-------------|
| **Checkout** | Pulls the `main` branch from the configured SCM repository |
| **Clean Environment** | Removes `__pycache__`, `.pyc` files, and stale coverage/test artifacts to ensure a clean build |
| **Install Dependencies** | Upgrades pip and installs all packages from `flask_app/requirements.txt` |
| **Code Quality** (parallel) | Runs **Flake8** (PEP 8, max complexity 10, max line 127) and **Black** (format check) in parallel; either failure fails the stage |
| **Build Validation** | Imports and instantiates the Flask app to confirm the application can start without errors |
| **Unit Tests** | Executes `pytest` excluding `slow` and `integration` markers; generates JUnit XML and an HTML coverage report |
| **Quality Gate** | Parses the coverage report and fails the build if total coverage falls below **60%** |
| **Docker Build** | Builds a Docker image tagged with `aceest-fitness:latest` and `aceest-fitness:<build-number>` |

Post-build actions archive JUnit test results and the HTML coverage report as Jenkins artifacts regardless of build outcome.

---

### GitHub Actions

Two workflow files are defined under `.github/workflows/`.

#### `main.yml` — Primary CI/CD Workflow

Triggered on every push and pull request to `main`. Runs on `ubuntu-latest` with Python 3.11.

| Job | Dependencies | What It Does |
|-----|-------------|-------------|
| **build-and-lint** | — | Installs dependencies; runs Flake8, Black, and Pylint; fails fast on any quality violation |
| **docker-build** | build-and-lint | Builds the multi-stage Docker image; runs a smoke test by starting the container and checking the `/` health endpoint; uploads the image as a 3-day artifact |
| **automated-testing** | docker-build | Starts the built container; runs `pytest` inside it with XML coverage output; publishes JUnit results; enforces the 60% coverage gate |
| **pipeline-summary** | automated-testing | Prints a final pass/fail summary with links to artifacts |

#### `test.yml` — Multi-Version Test Matrix

Triggered on push/PR and can be run manually (`workflow_dispatch`). Tests across a matrix of Python **3.9, 3.10, and 3.11**.

| Job | What It Does |
|-----|-------------|
| **test** | Runs unit tests with coverage on each Python version; uploads results to Codecov |
| **coverage-check** | Generates an HTML coverage report and uploads it as an artifact |
| **test-integration** | Runs only `@pytest.mark.integration` tests against a live in-memory database |
| **build-validation** | Final readiness check — imports the app and verifies it starts cleanly |

Both workflows enforce the **60% minimum coverage threshold** and will fail the run if it is not met.

---

## Project Structure

```
DevOps_Assignment/
├── .github/workflows/
│   ├── main.yml              # Primary CI/CD pipeline
│   └── test.yml              # Multi-version test matrix
├── flask_app/
│   ├── app.py                # Flask application factory
│   ├── config.py             # Configuration (env vars, DB URL)
│   ├── models/               # SQLAlchemy models (Member, Workout, etc.)
│   ├── routes/               # Blueprint route handlers
│   ├── services/             # Business logic layer
│   ├── utils/                # Validation and calculation helpers
│   ├── tests/                # Pytest test suite
│   │   ├── conftest.py       # Shared fixtures
│   │   ├── test_routes.py    # API endpoint tests
│   │   ├── test_services.py  # Service layer tests
│   │   ├── test_models.py    # ORM model tests
│   │   └── test_utils.py     # Utility function tests
│   ├── requirements.txt
│   └── pytest.ini
├── ui_app/
│   ├── aceest_ui.py          # Tkinter desktop application
│   ├── requirements.txt
│   └── Dockerfile            # VNC-based UI container
├── jenkins/                  # Jenkins plugins and init scripts
├── Dockerfile                # Multi-stage Flask API image
├── docker-compose.yml        # Full stack orchestration
├── docker-compose.jenkins.yml
├── Jenkinsfile               # Windows Jenkins pipeline
├── nginx.conf                # Reverse proxy configuration
└── azure-pipelines.yml       # Azure DevOps alternative pipeline
```
