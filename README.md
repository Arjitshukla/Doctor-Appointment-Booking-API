# Clinic API

Django REST API for managing doctors and appointments.

## Tech Stack

- Django 6.0.4
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose

## Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose

### Setup

1. Clone the project
2. Create `.env` file (copy from `.env` template)
3. Build and run:

```bash
docker-compose up --build
```

4. Apply migrations:

```bash
docker-compose exec web python manage.py migrate
```

5. Create superuser (optional):

```bash
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/doctors/` | List/Create doctors |
| GET/PUT/DELETE | `/api/doctors/{id}/` | Retrieve/Update/Delete doctor |
| GET/POST | `/api/appointments/` | List/Create appointments |
| GET/PUT/DELETE | `/api/appointments/{id}/` | Retrieve/Update/Delete appointment |
| GET/PUT/DELETE | `/api/appointments/?doctor={1}&date={2026-04-20}` | filter for doctor_id and date appointment |

## Development

```bash
# Local setup (without Docker)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (True/False) |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host |
| `DB_PORT` | Database port |