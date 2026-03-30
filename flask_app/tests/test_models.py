"""Tests for database models and data persistence."""

import pytest
from datetime import datetime, date
from models.member import Member
from models.workout import Workout, Exercise
from models.progress import Progress
from models.metric import Metric
from models.subscription import Subscription
from models.trainer import Trainer


class TestMemberModel:
    """Test Member model."""

    def test_member_creation(self, created_member):
        """Test member object creation."""
        assert created_member.id is not None
        assert created_member.name == 'John Doe'
        assert created_member.age == 30
        assert created_member.weight == 80.0

    def test_member_to_dict(self, created_member):
        """Test member serialization to dictionary."""
        member_dict = created_member.to_dict()
        assert isinstance(member_dict, dict)
        assert member_dict['name'] == 'John Doe'
        assert member_dict['age'] == 30
        assert 'id' in member_dict

    @pytest.mark.integration
    def test_member_relationships(self, db_session, created_member):
        """Test member relationships with other models."""
        progress = Progress(
            client_name=created_member.name,
            week='2024-W01',
            adherence=85
        )
        db_session.session.add(progress)
        db_session.session.commit()
        
        # Verify relationship
        assert len(created_member.progress) == 1
        assert created_member.progress[0].week == '2024-W01'

    @pytest.mark.edge_case
    def test_member_unique_name_constraint(self, db_session, created_member):
        """Test that member names must be unique."""
        duplicate_member = Member(
            name=created_member.name,  # Same name
            age=25,
            height=170.0,
            weight=70.0,
            program='Fat Loss (FL) – 3 day',
            calories=2000,
            target_weight=65.0,
            target_adherence=75
        )
        db_session.session.add(duplicate_member)
        
        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            db_session.session.commit()

    def test_member_nullable_fields(self, db_session):
        """Test nullable fields in member model."""
        member = Member(
            name='Nullable Test',
            age=30,
            height=180.0,
            weight=80.0,
            program='Beginner (BG)',
            calories=2500,
            target_weight=85.0,
            target_adherence=80,
            membership_end=None
        )
        db_session.session.add(member)
        db_session.session.commit()
        assert member.membership_end is None


class TestWorkoutModel:
    """Test Workout model."""

    def test_workout_creation(self, created_workout):
        """Test workout object creation."""
        assert created_workout.id is not None
        assert created_workout.workout_type == 'Chest & Triceps'
        assert created_workout.duration_min == 60

    def test_workout_to_dict(self, created_workout):
        """Test workout serialization."""
        workout_dict = created_workout.to_dict()
        assert isinstance(workout_dict, dict)
        assert workout_dict['workout_type'] == 'Chest & Triceps'

    def test_workout_date_storage(self, db_session, created_member):
        """Test workout date is properly stored."""
        test_date = date(2024, 1, 15)
        workout = Workout(
            client_name=created_member.name,
            date=test_date,
            workout_type='Back',
            duration_min=45,
            notes='Test'
        )
        db_session.session.add(workout)
        db_session.session.commit()
        
        retrieved = db_session.session.query(Workout).filter_by(id=workout.id).first()
        assert retrieved.date == test_date


class TestProgressModel:
    """Test Progress model."""

    def test_progress_creation(self, db_session, created_member):
        """Test progress record creation."""
        progress = Progress(
            client_name=created_member.name,
            week='2024-W02',
            adherence=90
        )
        db_session.session.add(progress)
        db_session.session.commit()
        
        assert progress.id is not None
        assert progress.week == '2024-W02'
        assert progress.adherence == 90

    def test_progress_to_dict(self, db_session, created_member):
        """Test progress serialization."""
        progress = Progress(
            client_name=created_member.name,
            week='2024-W01',
            adherence=85
        )
        db_session.session.add(progress)
        db_session.session.commit()
        
        progress_dict = progress.to_dict()
        assert isinstance(progress_dict, dict)
        assert progress_dict['week'] == '2024-W01'

    @pytest.mark.edge_case
    def test_progress_boundary_values(self, db_session, created_member):
        """Test progress with boundary values."""
        progress = Progress(
            client_name=created_member.name,
            week='2024-W52',
            adherence=0
        )
        db_session.session.add(progress)
        db_session.session.commit()
        assert progress.adherence == 0


class TestMetricModel:
    """Test Metric model."""

    def test_metric_creation(self, db_session, created_member):
        """Test metric record creation."""
        metric = Metric(
            client_name=created_member.name,
            date=date.today(),
            weight=78.5,
            waist=85.0,
            bodyfat=22.5
        )
        db_session.session.add(metric)
        db_session.session.commit()
        
        assert metric.id is not None
        assert metric.bodyfat == 22.5

    def test_metric_to_dict(self, db_session, created_member):
        """Test metric serialization."""
        metric = Metric(
            client_name=created_member.name,
            date=date.today(),
            weight=78.5,
            waist=85.0,
            bodyfat=20.5
        )
        db_session.session.add(metric)
        db_session.session.commit()
        
        metric_dict = metric.to_dict()
        assert isinstance(metric_dict, dict)
        assert metric_dict['bodyfat'] == 20.5

    @pytest.mark.edge_case
    def test_metric_boundary_values(self, db_session, created_member):
        """Test metric with boundary values."""
        metric = Metric(
            client_name=created_member.name,
            date=date.today(),
            weight=30.0,
            waist=150.0,
            bodyfat=45.0
        )
        db_session.session.add(metric)
        db_session.session.commit()
        assert metric.bodyfat == 45.0


class TestSubscriptionModel:
    """Test Subscription model."""

    def test_subscription_creation(self, db_session, created_member):
        """Test subscription creation."""
        subscription = Subscription(
            client_name=created_member.name,
            plan_name='Premium',
            start_date=date.today(),
            end_date=date(2025, 12, 31),
            fee=80.0
        )
        db_session.session.add(subscription)
        db_session.session.commit()
        
        assert subscription.id is not None
        assert subscription.plan_name == 'Premium'
        assert subscription.fee == 80.0

    def test_subscription_different_plans(self, db_session, created_member):
        """Test different subscription plans."""
        plans = [
            ('Basic', 50.0),
            ('Premium', 80.0),
            ('VIP', 120.0)
        ]
        
        for plan_name, price in plans:
            subscription = Subscription(
                client_name=created_member.name,
                plan_name=plan_name,
                start_date=date.today(),
                end_date=date(2025, 12, 31),
                fee=price
            )
            db_session.session.add(subscription)
        
        db_session.session.commit()
        
        all_subscriptions = db_session.session.query(Subscription).filter_by(client_name=created_member.name).all()
        assert len(all_subscriptions) == 3


class TestTrainerModel:
    """Test Trainer model."""

    def test_trainer_creation(self, db_session):
        """Test trainer creation."""
        trainer = Trainer(
            name='John Smith',
            specialization='Strength Training',
            experience_years=10,
            email='john@example.com'
        )
        db_session.session.add(trainer)
        db_session.session.commit()
        
        assert trainer.id is not None
        assert trainer.name == 'John Smith'

    def test_trainer_to_dict(self, db_session):
        """Test trainer serialization."""
        trainer = Trainer(
            name='Jane Doe',
            specialization='Yoga',
            experience_years=5,
            email='jane@example.com'
        )
        db_session.session.add(trainer)
        db_session.session.commit()
        
        trainer_dict = trainer.to_dict()
        assert trainer_dict['specialization'] == 'Yoga'

    @pytest.mark.edge_case
    def test_trainer_experience_boundary(self, db_session):
        """Test trainers with boundary experience values."""
        new_trainer = Trainer(
            name='Fresh Trainer',
            specialization='Fitness',
            experience_years=0,
            email='fresh@example.com'
        )
        veteran_trainer = Trainer(
            name='Veteran Trainer',
            specialization='Fitness',
            experience_years=50,
            email='veteran@example.com'
        )
        db_session.session.add_all([new_trainer, veteran_trainer])
        db_session.session.commit()
        
        assert new_trainer.experience_years == 0
        assert veteran_trainer.experience_years == 50


@pytest.mark.integration
class TestModelIntegration:
    """Test integration between multiple models."""

    def test_member_with_all_relationships(self, db_session, created_member):
        """Test a member with all related records."""
        # Create progress
        progress = Progress(
            client_name=created_member.name,
            week='2024-W01',
            adherence=85
        )
        
        # Create workout
        workout = Workout(
            client_name=created_member.name,
            date=datetime.now().date(),
            workout_type='Chest',
            duration_min=60,
            notes='Test'
        )
        
        # Create metric
        metric = Metric(
            client_name=created_member.name,
            date=date.today(),
            weight=78.5,
            waist=85.0,
            bodyfat=20.5
        )
        
        db_session.session.add_all([progress, workout, metric])
        db_session.session.commit()
        
        # Verify all relationships
        assert len(created_member.progress) == 1
        assert len(created_member.workouts) == 1
        assert len(created_member.metrics) == 1
