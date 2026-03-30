"""Tests for business logic services."""

import pytest
from datetime import datetime, date
from models.member import Member
from services.member_service import MemberService
from models.progress import Progress
from models.workout import Workout
from models.metric import Metric
from services.subscription_service import SubscriptionService
from services.workout_service import WorkoutService
from services.trainer_service import TrainerService
from models.trainer import Trainer
from models.workout import Exercise
from models.subscription import Subscription


class TestMemberService:
    """Test MemberService business logic."""

    def test_get_all_members(self, db_session, multiple_members):
        """Test retrieving all members."""
        members = MemberService.get_all_members()
        assert len(members) == 3
        assert all(isinstance(m, Member) for m in members)

    def test_get_all_members_empty(self, db_session):
        """Test retrieving members when none exist."""
        members = MemberService.get_all_members()
        assert len(members) == 0

    def test_get_member_by_id(self, db_session, created_member):
        """Test retrieving a specific member by ID."""
        member = MemberService.get_member_by_id(created_member.id)
        assert member is not None
        assert member.id == created_member.id
        assert member.name == created_member.name

    @pytest.mark.negative
    def test_get_member_by_id_nonexistent(self, db_session):
        """Test retrieving a non-existent member."""
        member = MemberService.get_member_by_id(9999)
        assert member is None

    def test_get_member_by_name(self, db_session, created_member):
        """Test retrieving a member by name."""
        member = MemberService.get_member_by_name(created_member.name)
        assert member is not None
        assert member.name == created_member.name

    @pytest.mark.negative
    def test_get_member_by_name_nonexistent(self, db_session):
        """Test retrieving a non-existent member by name."""
        member = MemberService.get_member_by_name('Nonexistent Person')
        assert member is None

    def test_create_member_valid(self, db_session, sample_member_data):
        """Test creating a member with valid data."""
        member = MemberService.create_member(sample_member_data)
        assert member.id is not None
        assert member.name == sample_member_data['name']
        assert member.age == sample_member_data['age']
        assert member.calories > 0

    @pytest.mark.negative
    def test_create_member_invalid_data(self, db_session):
        """Test creating a member with invalid data raises error."""
        invalid_data = {
            'name': '',  # Invalid: empty name
            'age': 30,
            'height': 180.0,
            'weight': 80.0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 80
        }
        with pytest.raises(ValueError):
            MemberService.create_member(invalid_data)

    @pytest.mark.negative
    def test_create_member_missing_required_field(self, db_session):
        """Test creating a member with missing required field."""
        incomplete_data = {
            'name': 'John',
            'age': 30
            # Missing other required fields
        }
        with pytest.raises(ValueError):
            MemberService.create_member(incomplete_data)

    @pytest.mark.negative
    def test_create_member_duplicate_name(self, db_session, created_member):
        """Test creating a member with duplicate name."""
        duplicate_data = {
            'name': created_member.name,  # Same as existing
            'age': 25,
            'height': 170.0,
            'weight': 70.0,
            'program': 'Fat Loss (FL) – 3 day',
            'target_weight': 65.0,
            'target_adherence': 75
        }
        with pytest.raises(Exception):  # Database integrity error
            MemberService.create_member(duplicate_data)

    def test_update_member_valid(self, db_session, created_member):
        """Test updating a member with valid data."""
        update_data = {
            'weight': 75.0,
            'age': 31
        }
        updated_member = MemberService.update_member(created_member.id, update_data)
        assert updated_member.weight == 75.0
        assert updated_member.age == 31

    @pytest.mark.negative
    def test_update_member_nonexistent(self, db_session):
        """Test updating a non-existent member."""
        with pytest.raises(ValueError, match="Member not found"):
            MemberService.update_member(9999, {'weight': 70.0})

    @pytest.mark.negative
    def test_update_member_invalid_data(self, db_session, created_member):
        """Test updating a member with invalid data."""
        invalid_update = {
            'age': 150  # Invalid: exceeds maximum
        }
        with pytest.raises(ValueError):
            MemberService.update_member(created_member.id, invalid_update)

    def test_update_member_recalculates_calories(self, db_session, created_member):
        """Test that calories are recalculated when relevant fields change."""
        original_calories = created_member.calories
        
        # Update weight which should trigger calorie recalculation
        update_data = {'weight': 90.0}
        updated_member = MemberService.update_member(created_member.id, update_data)
        
        # Calories should have changed (likely increased)
        assert updated_member.calories != original_calories

    def test_delete_member(self, db_session, created_member):
        """Test deleting a member."""
        member_id = created_member.id
        MemberService.delete_member(member_id)
        
        # Verify member is deleted
        deleted_member = MemberService.get_member_by_id(member_id)
        assert deleted_member is None

    @pytest.mark.negative
    def test_delete_member_nonexistent(self, db_session):
        """Test deleting a non-existent member raises error."""
        with pytest.raises(ValueError, match="Member not found"):
            MemberService.delete_member(9999)

    def test_get_member_summary(self, db_session, created_member):
        """Test getting comprehensive member summary."""
        # Add some related data
        progress = Progress(
            client_name=created_member.name,
            week='2024-W01',
            adherence=85
        )
        workout = Workout(
            client_name=created_member.name,
            date=datetime.now().date(),
            workout_type='Chest',
            duration_min=60,
            notes='Test workout'
        )
        metric = Metric(
            client_name=created_member.name,
            date=date.today(),
            weight=78.5,
            waist=85.0,
            bodyfat=20.5
        )
        db_session.session.add_all([progress, workout, metric])
        db_session.session.commit()
        
        summary = MemberService.get_member_summary(created_member.name)
        
        assert 'member' in summary
        assert 'bmi' in summary
        assert 'recent_progress' in summary
        assert 'recent_workouts' in summary
        assert 'latest_metrics' in summary
        assert len(summary['recent_progress']) > 0
        assert len(summary['recent_workouts']) > 0
        assert summary['latest_metrics'] is not None

    @pytest.mark.negative
    def test_get_member_summary_nonexistent(self, db_session):
        """Test getting summary for non-existent member."""
        with pytest.raises(ValueError, match="Member not found"):
            MemberService.get_member_summary('Nonexistent Member')

    @pytest.mark.edge_case
    def test_get_member_summary_no_related_data(self, db_session, created_member):
        """Test member summary when no progress/workouts exist."""
        summary = MemberService.get_member_summary(created_member.name)
        
        assert summary['member'] is not None
        assert summary['bmi'] > 0
        assert len(summary['recent_progress']) == 0
        assert len(summary['recent_workouts']) == 0
        assert summary['latest_metrics'] is None

    @pytest.mark.integration
    def test_member_service_data_consistency(self, db_session, sample_member_data):
        """Test that member service maintains data consistency."""
        # Create
        member = MemberService.create_member(sample_member_data)
        member_id = member.id
        
        # Retrieve
        retrieved = MemberService.get_member_by_id(member_id)
        assert retrieved.name == sample_member_data['name']
        
        # Update
        updated = MemberService.update_member(member_id, {'weight': 85.0})
        assert updated.weight == 85.0
        
        # Verify update persisted
        verified = MemberService.get_member_by_id(member_id)
        assert verified.weight == 85.0

    @pytest.mark.edge_case
    def test_create_member_boundary_values(self, db_session):
        """Test creating members with boundary values."""
        boundary_data = {
            'name': 'Boundary Test',
            'age': 1,  # Minimum valid age
            'height': 100.0,  # Very short
            'weight': 30.0,  # Very light
            'program': 'Beginner (BG)',
            'target_weight': 40.0,
            'target_adherence': 0  # Minimum adherence
        }
        member = MemberService.create_member(boundary_data)
        assert member.age == 1
        assert member.weight == 30.0
        assert member.target_adherence == 0

    def test_update_member_partial_fields(self, db_session, created_member):
        """Test updating only specific fields."""
        original_program = created_member.program
        
        # Update only age
        update_data = {'age': 35}
        updated = MemberService.update_member(created_member.id, update_data)
        
        assert updated.age == 35
        assert updated.program == original_program  # Unchanged


class TestSubscriptionService:
    """Test SubscriptionService business logic."""

    def test_get_all_subscriptions(self, db_session, created_subscription):
        """Test retrieving all subscriptions."""
        subscriptions = SubscriptionService.get_all_subscriptions()
        assert len(subscriptions) >= 1
        assert all(isinstance(sub, Subscription) for sub in subscriptions)

    def test_get_subscriptions_by_member(self, db_session, created_subscription):
        """Test retrieving subscriptions by member."""
        subscriptions = SubscriptionService.get_subscriptions_by_member(created_subscription.client_name)
        assert len(subscriptions) >= 1
        assert all(sub.client_name == created_subscription.client_name for sub in subscriptions)

    def test_get_subscription_by_id(self, db_session, created_subscription):
        """Test retrieving a specific subscription by ID."""
        subscription = SubscriptionService.get_subscription_by_id(created_subscription.id)
        assert subscription is not None
        assert subscription.id == created_subscription.id

    @pytest.mark.negative
    def test_get_subscription_by_id_nonexistent(self, db_session):
        """Test retrieving a non-existent subscription."""
        subscription = SubscriptionService.get_subscription_by_id(9999)
        assert subscription is None

    def test_create_subscription_valid(self, db_session, sample_subscription_data):
        """Test creating a subscription with valid data."""
        subscription = SubscriptionService.create_subscription(sample_subscription_data)
        assert subscription.id is not None
        assert subscription.client_name == sample_subscription_data['client_name']
        assert subscription.plan_name == sample_subscription_data['plan_name']
        assert subscription.fee > 0

    @pytest.mark.negative
    def test_create_subscription_invalid_data(self, db_session):
        """Test creating a subscription with invalid data raises error."""
        invalid_data = {
            'client_name': '',
            'plan_name': 'Basic',
            'start_date': '2024-01-01',
            'end_date': '2023-12-31'  # End before start
        }
        with pytest.raises(ValueError):
            SubscriptionService.create_subscription(invalid_data)

    def test_update_subscription_valid(self, db_session, created_subscription):
        """Test updating a subscription."""
        update_data = {'plan_name': 'VIP'}
        updated = SubscriptionService.update_subscription(created_subscription.id, update_data)
        assert updated.plan_name == 'VIP'

    @pytest.mark.negative
    def test_update_subscription_not_found(self, db_session):
        """Test updating a non-existent subscription."""
        with pytest.raises(ValueError, match="Subscription not found"):
            SubscriptionService.update_subscription(9999, {'plan_name': 'Basic'})

    def test_delete_subscription(self, db_session, created_subscription):
        """Test deleting a subscription."""
        result = SubscriptionService.delete_subscription(created_subscription.id)
        assert result is True

        # Verify deletion
        deleted = SubscriptionService.get_subscription_by_id(created_subscription.id)
        assert deleted is None

    @pytest.mark.negative
    def test_delete_subscription_not_found(self, db_session):
        """Test deleting a non-existent subscription."""
        with pytest.raises(ValueError, match="Subscription not found"):
            SubscriptionService.delete_subscription(9999)

    def test_get_active_subscriptions(self, db_session, created_subscription):
        """Test retrieving active subscriptions."""
        active = SubscriptionService.get_active_subscriptions()
        assert isinstance(active, list)
        # Should include our created subscription if it's active
        active_ids = [sub.id for sub in active]
        assert created_subscription.id in active_ids


class TestWorkoutService:
    """Test WorkoutService business logic."""

    def test_get_workouts_by_member(self, db_session, created_workout):
        """Test retrieving workouts by member."""
        workouts = WorkoutService.get_workouts_by_member(created_workout.client_name)
        assert len(workouts) >= 1
        assert all(workout.client_name == created_workout.client_name for workout in workouts)

    def test_get_workout_by_id(self, db_session, created_workout):
        """Test retrieving a specific workout by ID."""
        workout = WorkoutService.get_workout_by_id(created_workout.id)
        assert workout is not None
        assert workout.id == created_workout.id

    @pytest.mark.negative
    def test_get_workout_by_id_nonexistent(self, db_session):
        """Test retrieving a non-existent workout."""
        workout = WorkoutService.get_workout_by_id(9999)
        assert workout is None

    def test_create_workout_valid(self, db_session, sample_workout_data):
        """Test creating a workout with valid data."""
        workout = WorkoutService.create_workout(sample_workout_data)
        assert workout.id is not None
        assert workout.client_name == sample_workout_data['client_name']
        assert workout.workout_type == sample_workout_data['workout_type']

    def test_create_workout_with_exercises(self, db_session, sample_workout_data):
        """Test creating a workout with exercises."""
        workout_data = sample_workout_data.copy()
        workout_data['exercises'] = [
            {
                'name': 'Bench Press',
                'sets': 4,
                'reps': 8,
                'weight': 100.0
            },
            {
                'name': 'Push-ups',
                'sets': 3,
                'reps': 15
            }
        ]

        workout = WorkoutService.create_workout(workout_data)
        assert workout.id is not None

        # Check exercises were created
        exercises = db_session.session.query(Exercise).filter_by(workout_id=workout.id).all()
        assert len(exercises) == 2
        assert exercises[0].name == 'Bench Press'
        assert exercises[1].name == 'Push-ups'

    @pytest.mark.negative
    def test_create_workout_invalid_data(self, db_session):
        """Test creating a workout with invalid data raises error."""
        invalid_data = {
            'client_name': 'John Doe',
            'date': '2024-01-01',
            'workout_type': 'Chest',
            'duration_min': -30  # Invalid negative duration
        }
        with pytest.raises(ValueError):
            WorkoutService.create_workout(invalid_data)

    def test_update_workout_valid(self, db_session, created_workout):
        """Test updating a workout."""
        update_data = {'duration_min': 75, 'notes': 'Updated notes'}
        updated = WorkoutService.update_workout(created_workout.id, update_data)
        assert updated.duration_min == 75
        assert updated.notes == 'Updated notes'

    def test_update_workout_with_exercises(self, db_session, created_workout):
        """Test updating workout exercises."""
        update_data = {
            'exercises': [
                {
                    'name': 'Squat',
                    'sets': 5,
                    'reps': 5,
                    'weight': 150.0
                }
            ]
        }
        updated = WorkoutService.update_workout(created_workout.id, update_data)

        # Check exercises were updated
        exercises = db_session.session.query(Exercise).filter_by(workout_id=created_workout.id).all()
        assert len(exercises) == 1
        assert exercises[0].name == 'Squat'

    @pytest.mark.negative
    def test_update_workout_not_found(self, db_session):
        """Test updating a non-existent workout."""
        with pytest.raises(ValueError, match="Workout not found"):
            WorkoutService.update_workout(9999, {'duration_min': 60})

    def test_delete_workout(self, db_session, created_workout):
        """Test deleting a workout."""
        result = WorkoutService.delete_workout(created_workout.id)
        assert result is True

        # Verify deletion and cascade delete of exercises
        workout = WorkoutService.get_workout_by_id(created_workout.id)
        assert workout is None

    @pytest.mark.negative
    def test_delete_workout_not_found(self, db_session):
        """Test deleting a non-existent workout."""
        with pytest.raises(ValueError, match="Workout not found"):
            WorkoutService.delete_workout(9999)

    def test_get_workout_with_exercises(self, db_session, created_workout):
        """Test getting workout with exercises."""
        # Add an exercise to the workout
        exercise = Exercise(
            workout_id=created_workout.id,
            name='Bench Press',
            sets=4,
            reps=8,
            weight=100.0
        )
        db_session.session.add(exercise)
        db_session.session.commit()

        result = WorkoutService.get_workout_with_exercises(created_workout.id)
        assert result['id'] == created_workout.id
        assert 'exercises' in result
        assert len(result['exercises']) == 1
        assert result['exercises'][0]['name'] == 'Bench Press'

    @pytest.mark.negative
    def test_get_workout_with_exercises_not_found(self, db_session):
        """Test getting workout with exercises for non-existent workout."""
        with pytest.raises(ValueError, match="Workout not found"):
            WorkoutService.get_workout_with_exercises(9999)


class TestTrainerService:
    """Test TrainerService business logic."""

    def test_get_all_trainers(self, db_session):
        """Test retrieving all trainers."""
        # Create a test trainer first
        trainer = Trainer(
            name='Test Trainer',
            specialization='Fitness',
            experience_years=5,
            email='test@example.com'
        )
        db_session.session.add(trainer)
        db_session.session.commit()

        trainers = TrainerService.get_all_trainers()
        assert len(trainers) >= 1
        assert all(isinstance(t, Trainer) for t in trainers)

    def test_get_trainer_by_id(self, db_session):
        """Test retrieving a specific trainer by ID."""
        trainer = Trainer(
            name='Test Trainer',
            specialization='Fitness',
            experience_years=5,
            email='test@example.com'
        )
        db_session.session.add(trainer)
        db_session.session.commit()

        retrieved = TrainerService.get_trainer_by_id(trainer.id)
        assert retrieved is not None
        assert retrieved.id == trainer.id

    @pytest.mark.negative
    def test_get_trainer_by_id_nonexistent(self, db_session):
        """Test retrieving a non-existent trainer."""
        trainer = TrainerService.get_trainer_by_id(9999)
        assert trainer is None

    def test_get_trainer_by_name(self, db_session):
        """Test retrieving a trainer by name."""
        trainer = Trainer(
            name='Unique Trainer',
            specialization='Yoga',
            experience_years=8,
            email='unique@example.com'
        )
        db_session.session.add(trainer)
        db_session.session.commit()

        retrieved = TrainerService.get_trainer_by_name('Unique Trainer')
        assert retrieved is not None
        assert retrieved.name == 'Unique Trainer'

    @pytest.mark.negative
    def test_get_trainer_by_name_nonexistent(self, db_session):
        """Test retrieving a non-existent trainer by name."""
        trainer = TrainerService.get_trainer_by_name('Nonexistent Trainer')
        assert trainer is None

    def test_create_trainer_valid(self, db_session, sample_trainer_data):
        """Test creating a trainer with valid data."""
        # Update sample data to match actual model
        trainer_data = {
            'name': sample_trainer_data['name'],
            'specialization': sample_trainer_data['specialization'],
            'experience_years': sample_trainer_data['experience_years'],
            'email': 'trainer@example.com'  # Use valid email
        }

        trainer = TrainerService.create_trainer(trainer_data)
        assert trainer.id is not None
        assert trainer.name == trainer_data['name']
        assert trainer.specialization == trainer_data['specialization']

    @pytest.mark.negative
    def test_create_trainer_invalid_data(self, db_session):
        """Test creating a trainer with invalid data raises error."""
        invalid_data = {
            'name': '',  # Invalid: empty name
            'specialization': 'Fitness',
            'experience_years': 5,
            'email': 'trainer@example.com'
        }
        with pytest.raises(ValueError):
            TrainerService.create_trainer(invalid_data)

    def test_update_trainer_valid(self, db_session):
        """Test updating a trainer."""
        trainer = Trainer(
            name='Update Test',
            specialization='Fitness',
            experience_years=3,
            email='update@example.com'
        )
        db_session.session.add(trainer)
        db_session.session.commit()

        update_data = {'experience_years': 5, 'specialization': 'Strength Training'}
        updated = TrainerService.update_trainer(trainer.id, update_data)
        assert updated.experience_years == 5
        assert updated.specialization == 'Strength Training'

    @pytest.mark.negative
    def test_update_trainer_not_found(self, db_session):
        """Test updating a non-existent trainer."""
        with pytest.raises(ValueError, match="Trainer not found"):
            TrainerService.update_trainer(9999, {'experience_years': 5})

    def test_delete_trainer(self, db_session):
        """Test deleting a trainer."""
        trainer = Trainer(
            name='Delete Test',
            specialization='Fitness',
            experience_years=2,
            email='delete@example.com'
        )
        db_session.session.add(trainer)
        db_session.session.commit()

        result = TrainerService.delete_trainer(trainer.id)
        assert result is True

        # Verify deletion
        deleted = TrainerService.get_trainer_by_id(trainer.id)
        assert deleted is None

    @pytest.mark.negative
    def test_delete_trainer_not_found(self, db_session):
        """Test deleting a non-existent trainer."""
        with pytest.raises(ValueError, match="Trainer not found"):
            TrainerService.delete_trainer(9999)

    @pytest.mark.integration
    def test_member_list_operations(self, db_session, multiple_members):
        """Test operations on list of members."""
        all_members = MemberService.get_all_members()
        assert len(all_members) == len(multiple_members)
        
        # Verify all expected members are present
        member_names = {m.name for m in all_members}
        expected_names = {m.name for m in multiple_members}
        assert member_names == expected_names

    @pytest.mark.slow
    def test_member_service_with_large_dataset(self, db_session):
        """Test service performance with larger dataset."""
        # Create 50 members
        for i in range(50):
            data = {
                'name': f'Member {i}',
                'age': 20 + (i % 40),
                'height': 150.0 + (i % 50),
                'weight': 50.0 + (i % 60),
                'program': 'Beginner (BG)',
                'target_weight': 70.0 + (i % 40),
                'target_adherence': 70
            }
            MemberService.create_member(data)
        
        all_members = MemberService.get_all_members()
        assert len(all_members) == 50
