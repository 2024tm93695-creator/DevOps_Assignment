"""
Pytest configuration and fixtures for ACEest Fitness API.
Provides reusable test data, database setup, and application context.
"""

import pytest
import os
from datetime import datetime, date, timedelta
from app import app
from models.database import db
from models.member import Member
from models.workout import Workout, Exercise
from models.progress import Progress
from models.metric import Metric
from models.subscription import Subscription
from models.trainer import Trainer


@pytest.fixture(scope='session')
def app_config():
    """Configure app for testing with in-memory SQLite database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


@pytest.fixture(scope='session')
def app_instance(app_config):
    """Create application instance."""
    return app_config


@pytest.fixture
def client(app_instance):
    """Create test client for API testing."""
    with app_instance.app_context():
        db.drop_all()  # Clean slate before each test
        db.create_all()
        yield app_instance.test_client()
        db.session.remove()
        db.drop_all()  # Clean up after each test


@pytest.fixture
def db_session(app_instance):
    """Provide a database session for model testing."""
    with app_instance.app_context():
        db.drop_all()  # Clean slate before each test
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()  # Clean up after each test


@pytest.fixture
def sample_member_data():
    """Sample member data for testing."""
    return {
        'name': 'John Doe',
        'age': 30,
        'height': 180.0,
        'weight': 80.0,
        'program': 'Muscle Gain (MG) – PPL',
        'target_weight': 85.0,
        'target_adherence': 80,
        'membership_status': 'active'
    }


@pytest.fixture
def sample_member_data_minimal():
    """Minimal valid member data."""
    return {
        'name': 'Jane Smith',
        'age': 25,
        'height': 165.0,
        'weight': 65.0,
        'program': 'Fat Loss (FL) – 3 day',
        'target_weight': 60.0,
        'target_adherence': 75
    }


@pytest.fixture
def sample_invalid_member_data():
    """Invalid member data for negative testing."""
    return {
        'name': '',
        'age': 150,
        'height': -170.0,
        'weight': 0,
        'program': 'Invalid Program',
        'target_weight': -80.0,
        'target_adherence': 150
    }


@pytest.fixture
def created_member(db_session, sample_member_data):
    """Create a sample member in the database."""
    member = Member(
        name=sample_member_data['name'],
        age=sample_member_data['age'],
        height=sample_member_data['height'],
        weight=sample_member_data['weight'],
        program=sample_member_data['program'],
        calories=2500,
        target_weight=sample_member_data['target_weight'],
        target_adherence=sample_member_data['target_adherence']
    )
    db_session.session.add(member)
    db_session.session.commit()
    return member


@pytest.fixture
def multiple_members(db_session):
    """Create multiple members for list testing."""
    members_data = [
        {
            'name': 'Alice Johnson',
            'age': 28,
            'height': 170.0,
            'weight': 70.0,
            'program': 'Fat Loss (FL) – 5 day',
            'calories': 2200,
            'target_weight': 65.0,
            'target_adherence': 80
        },
        {
            'name': 'Bob Williams',
            'age': 35,
            'height': 185.0,
            'weight': 90.0,
            'program': 'Muscle Gain (MG) – PPL',
            'calories': 3000,
            'target_weight': 95.0,
            'target_adherence': 85
        },
        {
            'name': 'Carol Davis',
            'age': 22,
            'height': 160.0,
            'weight': 60.0,
            'program': 'Beginner (BG)',
            'calories': 2000,
            'target_weight': 58.0,
            'target_adherence': 70
        }
    ]
    
    members = []
    for data in members_data:
        member = Member(**data)
        db_session.session.add(member)
        members.append(member)
    
    db_session.session.commit()
    return members


@pytest.fixture
def sample_workout_data(created_member):
    """Sample workout data for testing."""
    return {
        'client_name': created_member.name,
        'date': datetime.now().date().isoformat(),
        'workout_type': 'Chest & Triceps',
        'duration_min': 60,
        'notes': 'Good workout'
    }


@pytest.fixture
def sample_exercise_data():
    """Sample exercise data."""
    return {
        'name': 'Bench Press',
        'sets': 4,
        'reps': 8,
        'weight': 100.0,
        'rest_sec': 90
    }


@pytest.fixture
def created_workout(db_session, created_member, sample_workout_data):
    """Create a sample workout in the database."""
    workout = Workout(
        client_name=sample_workout_data['client_name'],
        date=datetime.fromisoformat(sample_workout_data['date']),
        workout_type=sample_workout_data['workout_type'],
        duration_min=sample_workout_data['duration_min'],
        notes=sample_workout_data.get('notes', '')
    )
    db_session.session.add(workout)
    db_session.session.commit()
    return workout


@pytest.fixture
def sample_progress_data(created_member):
    """Sample progress data for testing."""
    return {
        'client_name': created_member.name,
        'week': '2024-W01',
        'adherence': 85
    }


@pytest.fixture
def sample_metric_data(created_member):
    """Sample metric data for testing."""
    return {
        'client_name': created_member.name,
        'date': datetime.now().date().isoformat(),
        'weight': 78.5,
        'waist': 85.0,
        'bodyfat': 20.5
    }


@pytest.fixture
def sample_subscription_data(created_member):
    """Sample subscription data for testing."""
    return {
        'client_name': created_member.name,
        'plan_name': 'Premium',
        'start_date': date.today().isoformat(),
        'end_date': (date.today() + timedelta(days=365)).isoformat()
    }


@pytest.fixture
def created_subscription(db_session, created_member, sample_subscription_data):
    """Create a sample subscription in the database."""
    from models.subscription import Subscription
    subscription = Subscription(
        client_name=sample_subscription_data['client_name'],
        plan_name=sample_subscription_data['plan_name'],
        start_date=date.fromisoformat(sample_subscription_data['start_date']),
        end_date=date.fromisoformat(sample_subscription_data['end_date']),
        fee=80.0
    )
    db_session.session.add(subscription)
    db_session.session.commit()
    return subscription


@pytest.fixture
def sample_trainer_data():
    """Sample trainer data for testing."""
    return {
        'name': 'Mike Coach',
        'specialization': 'Strength Training',
        'experience_years': 10,
        'certification': 'NASM',
        'clients_count': 15
    }


@pytest.fixture
def edge_case_member_data():
    """Edge case member data for boundary testing."""
    return {
        'name': 'E' * 100,  # Very long name
        'age': 1,           # Minimum age
        'height': 0.1,      # Very short
        'weight': 1000.0,   # Very heavy
        'program': 'Beginner (BG)',
        'target_weight': 999.9,
        'target_adherence': 0
    }


@pytest.fixture
def mock_external_api(mocker):
    """Mock external API calls."""
    mock_api = mocker.MagicMock()
    mock_api.get_nutrition_data.return_value = {
        'calories': 2500,
        'protein': 150,
        'carbs': 300,
        'fat': 80
    }
    return mock_api


# Pytest configuration options
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "unit: mark test as a unit test (queries are isolated and fast)"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test (uses multiple components)"
    )
    config.addinivalue_line(
        "markers",
        "edge_case: mark test as an edge case test"
    )
    config.addinivalue_line(
        "markers",
        "negative: mark test as a negative test (error cases)"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow (requires extended runtime)"
    )
