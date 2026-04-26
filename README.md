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

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/login/` | Obtain JWT access and refresh tokens |
| POST | `/api/refresh/` | Refresh JWT access token |

### Doctors

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/doctors/` | List all doctors |
| POST | `/api/doctors/` | Create a new doctor |
| GET | `/api/doctors/{id}/` | Retrieve a specific doctor |
| PUT/PATCH | `/api/doctors/{id}/` | Update a doctor |
| DELETE | `/api/doctors/{id}/` | Delete a doctor |
| GET | `/api/doctors/{id}/available-slots/?date=YYYY-MM-DD` | Get available time slots for a doctor on a specific date |

### Appointments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/appointments/` | List all appointments (supports filtering by `doctor` and `date`) |
| POST | `/api/appointments/` | Book a new appointment |
| GET | `/api/appointments/{id}/` | Retrieve a specific appointment |
| PUT/PATCH | `/api/appointments/{id}/` | Update an appointment |
| DELETE | `/api/appointments/{id}/` | Cancel/delete an appointment |
| PATCH | `/api/appointments/{id}/cancel/` | Mark appointment as cancelled |
| PATCH | `/api/appointments/{id}/reschedule/` | Reschedule appointment (cancels old and creates new) |

### Filtering Examples

- `/api/appointments/?doctor=1` — filter by doctor ID
- `/api/appointments/?date=2026-04-20` — filter by date
- `/api/appointments/?doctor=1&date=2026-04-20` — filter by both doctor and date

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