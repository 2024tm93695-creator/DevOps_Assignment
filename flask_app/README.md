# ACEest Fitness & Gym Management API

A modular Flask-based web application for fitness and gym management.

## Features

- **Member Management**: Register, update, and manage gym members
- **Trainer Management**: Manage fitness trainers and their specializations
- **Workout Planning**: Create and track workout plans with exercises
- **Subscription & Billing**: Handle membership subscriptions and payments
- **Progress Tracking**: Monitor member progress and adherence
- **RESTful API**: Complete REST API with proper HTTP methods

## Project Structure

```
flask_app/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── models/             # Database models
│   ├── __init__.py
│   ├── database.py
│   ├── member.py
│   ├── trainer.py
│   ├── workout.py
│   ├── metric.py
│   ├── progress.py
│   └── subscription.py
├── routes/             # API endpoints
│   ├── __init__.py
│   ├── members.py
│   ├── workouts.py
│   └── subscriptions.py
├── services/           # Business logic
│   ├── __init__.py
│   ├── member_service.py
│   ├── trainer_service.py
│   ├── workout_service.py
│   └── subscription_service.py
└── utils/              # Utilities and helpers
    ├── __init__.py
    ├── validations.py
    └── calculations.py
```

## Installation

1. Navigate to the flask_app directory:
   ```bash
   cd flask_app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Members
- `GET /api/members` - Get all members
- `GET /api/members/<id>` - Get member by ID
- `POST /api/members` - Create new member
- `PUT /api/members/<id>` - Update member
- `DELETE /api/members/<id>` - Delete member
- `GET /api/members/<name>/summary` - Get member summary

### Trainers
- `GET /api/members/trainers` - Get all trainers
- `POST /api/members/trainers` - Create new trainer
- `PUT /api/members/trainers/<id>` - Update trainer
- `DELETE /api/members/trainers/<id>` - Delete trainer

### Workouts
- `GET /api/workouts?member=<name>` - Get workouts by member
- `GET /api/workouts/<id>` - Get workout with exercises
- `POST /api/workouts` - Create new workout
- `PUT /api/workouts/<id>` - Update workout
- `DELETE /api/workouts/<id>` - Delete workout

### Subscriptions
- `GET /api/subscriptions` - Get all subscriptions
- `GET /api/subscriptions?member=<name>` - Get subscriptions by member
- `GET /api/subscriptions/<id>` - Get subscription by ID
- `POST /api/subscriptions` - Create new subscription
- `PUT /api/subscriptions/<id>` - Update subscription
- `DELETE /api/subscriptions/<id>` - Delete subscription
- `GET /api/subscriptions/active` - Get active subscriptions

## Sample API Usage

### Create a Member
```bash
curl -X POST http://localhost:5000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 30,
    "height": 175,
    "weight": 80,
    "program": "Fat Loss (FL) – 3 day",
    "target_weight": 75,
    "target_adherence": 80
  }'
```

### Create a Workout
```bash
curl -X POST http://localhost:5000/api/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "John Doe",
    "date": "2024-01-15",
    "workout_type": "Upper Body",
    "duration_min": 60,
    "notes": "Great session",
    "exercises": [
      {
        "name": "Bench Press",
        "sets": 4,
        "reps": 10,
        "weight": 80
      }
    ]
  }'
```

## Testing

The application includes input validation and error handling. Test the APIs using tools like Postman or curl.

## Database

The application uses SQLite by default. The database file `aceest_fitness.db` will be created automatically when the app starts.

## Development

- Follow clean code practices
- Use meaningful variable and function names
- Add proper error handling
- Maintain separation of concerns across modules