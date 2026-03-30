"""Tests for API routes and endpoints."""

import pytest
import json
from datetime import datetime, date
from unittest.mock import patch, MagicMock


class TestMembersRoutes:
    """Test members API endpoints."""

    def test_get_members_empty(self, client):
        """Test GET /api/members when no members exist."""
        response = client.get('/api/members/')
        assert response.status_code == 200
        assert response.json == []

    def test_get_members_success(self, client, multiple_members):
        """Test GET /api/members returns all members."""
        response = client.get('/api/members/')
        assert response.status_code == 200
        data = response.json
        assert len(data) == 3
        assert all(isinstance(member, dict) for member in data)
        assert all('name' in member for member in data)

    def test_get_member_by_id_success(self, client, created_member):
        """Test GET /api/members/<id> returns specific member."""
        response = client.get(f'/api/members/{created_member.id}')
        assert response.status_code == 200
        data = response.json
        assert data['id'] == created_member.id
        assert data['name'] == created_member.name

    @pytest.mark.negative
    def test_get_member_by_id_not_found(self, client):
        """Test GET /api/members/<id> with non-existent ID."""
        response = client.get('/api/members/9999')
        assert response.status_code == 404
        assert 'error' in response.json
        assert 'not found' in response.json['error'].lower()

    def test_create_member_success(self, client, sample_member_data):
        """Test POST /api/members creates new member."""
        response = client.post(
            '/api/members/',
            data=json.dumps(sample_member_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.json
        assert data['name'] == sample_member_data['name']
        assert data['age'] == sample_member_data['age']
        assert 'id' in data

    @pytest.mark.negative
    def test_create_member_invalid_data(self, client):
        """Test POST /api/members with invalid data."""
        invalid_data = {
            'name': '',  # Invalid: empty
            'age': 30,
            'height': 180.0,
            'weight': 80.0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 80
        }
        response = client.post(
            '/api/members/',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'error' in response.json

    @pytest.mark.negative
    def test_create_member_missing_field(self, client):
        """Test POST /api/members with missing required field."""
        incomplete_data = {
            'name': 'John',
            'age': 30
            # Missing other fields
        }
        response = client.post(
            '/api/members/',
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'error' in response.json

    def test_update_member_success(self, client, created_member):
        """Test PUT /api/members/<id> updates member."""
        update_data = {
            'weight': 75.0,
            'age': 31
        }
        response = client.put(
            f'/api/members/{created_member.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.json
        assert data['weight'] == 75.0
        assert data['age'] == 31

    @pytest.mark.negative
    def test_update_member_not_found(self, client):
        """Test PUT /api/members/<id> with non-existent ID."""
        response = client.put(
            '/api/members/9999',
            data=json.dumps({'weight': 70.0}),
            content_type='application/json'
        )
        assert response.status_code in [400, 404, 500]

    @pytest.mark.negative
    def test_update_member_invalid_data(self, client, created_member):
        """Test PUT /api/members/<id> with invalid data."""
        invalid_update = {
            'age': 150  # Invalid: exceeds maximum
        }
        response = client.put(
            f'/api/members/{created_member.id}',
            data=json.dumps(invalid_update),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'error' in response.json

    def test_delete_member_success(self, client, created_member):
        """Test DELETE /api/members/<id> deletes member."""
        response = client.delete(f'/api/members/{created_member.id}')
        assert response.status_code == 200
        assert 'deleted' in response.json['message'].lower()

    @pytest.mark.negative
    def test_delete_member_not_found(self, client):
        """Test DELETE /api/members/<id> with non-existent ID."""
        response = client.delete('/api/members/9999')
        assert response.status_code == 404
        assert 'error' in response.json

    def test_get_member_summary_success(self, client, created_member):
        """Test GET /api/members/<name>/summary returns member summary."""
        response = client.get(f'/api/members/{created_member.name}/summary')
        assert response.status_code == 200
        data = response.json
        assert 'member' in data
        assert 'bmi' in data
        assert 'recent_progress' in data
        assert 'recent_workouts' in data
        assert 'latest_metrics' in data

    @pytest.mark.negative
    def test_get_member_summary_not_found(self, client):
        """Test GET /api/members/<name>/summary with non-existent member."""
        response = client.get('/api/members/NonexistentMember/summary')
        assert response.status_code == 404
        assert 'error' in response.json


class TestRootRoute:
    """Test root and general routes."""

    def test_api_root_endpoint(self, client):
        """Test GET / returns API information."""
        response = client.get('/')
        assert response.status_code == 200
        data = response.json
        assert 'message' in data
        assert 'ACEest' in data['message']


class TestTrainerRoutes:
    """Test trainer endpoints."""

    def test_get_trainers_empty(self, client):
        """Test GET /api/members/trainers when no trainers exist."""
        response = client.get('/api/members/trainers')
        assert response.status_code == 200
        assert response.json == []

    def test_create_trainer_success(self, client, sample_trainer_data):
        """Test POST /api/members/trainers creates trainer."""
        response = client.post(
            '/api/members/trainers',
            data=json.dumps(sample_trainer_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.json
        assert data['name'] == sample_trainer_data['name']
        assert 'id' in data

    @pytest.mark.negative
    def test_create_trainer_invalid_data(self, client):
        """Test POST /api/members/trainers with invalid data."""
        invalid_data = {
            'name': '',  # Invalid: empty
            'specialization': 'Fitness',
            'experience_years': 5,
            'certification': 'NASM'
        }
        response = client.post(
            '/api/members/trainers',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        assert response.status_code == 400 or response.status_code == 500


class TestSubscriptionRoutes:
    """Test subscription endpoints."""

    def test_get_subscriptions_empty(self, client):
        """Test GET /api/subscriptions when no subscriptions exist."""
        response = client.get('/api/subscriptions/')
        assert response.status_code == 200
        assert response.json == []

    def test_get_subscriptions_by_member(self, client, created_member):
        """Test GET /api/subscriptions with member filter."""
        response = client.get(f'/api/subscriptions/?member={created_member.name}')
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_create_subscription_success(self, client, created_member, sample_subscription_data):
        """Test POST /api/subscriptions creates subscription."""
        response = client.post(
            '/api/subscriptions/',
            data=json.dumps(sample_subscription_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.json
        assert data['client_name'] == sample_subscription_data['client_name']
        assert 'id' in data

    def test_get_subscription_by_id_success(self, client, created_subscription):
        """Test GET /api/subscriptions/<id> retrieves subscription."""
        response = client.get(f'/api/subscriptions/{created_subscription.id}')
        assert response.status_code == 200
        assert response.json['id'] == created_subscription.id

    def test_get_subscription_by_id_not_found(self, client):
        """Test GET /api/subscriptions/<id> with non-existent ID."""
        response = client.get('/api/subscriptions/9999')
        assert response.status_code == 404

    def test_update_subscription_success(self, client, created_subscription):
        """Test PUT /api/subscriptions/<id> updates subscription."""
        update_data = {'plan_name': 'Premium'}
        response = client.put(
            f'/api/subscriptions/{created_subscription.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json['plan_name'] == 'Premium'

    def test_delete_subscription_success(self, client, created_subscription):
        """Test DELETE /api/subscriptions/<id> deletes subscription."""
        response = client.delete(f'/api/subscriptions/{created_subscription.id}')
        assert response.status_code == 200

        # Verify deletion
        get_response = client.get(f'/api/subscriptions/{created_subscription.id}')
        assert get_response.status_code == 404

    def test_get_active_subscriptions(self, client):
        """Test GET /api/subscriptions/active retrieves active subscriptions."""
        response = client.get('/api/subscriptions/active')
        assert response.status_code == 200
        assert isinstance(response.json, list)

    @pytest.mark.negative
    def test_create_subscription_invalid_data(self, client):
        """Test POST /api/subscriptions with invalid data."""
        invalid_data = {
            'client_name': '',
            'plan_name': 'Basic',
            'start_date': '2024-01-01',
            'end_date': '2023-12-31'  # End before start
        }
        response = client.post(
            '/api/subscriptions/',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        assert response.status_code == 400


class TestWorkoutRoutes:
    """Test workout endpoints."""

    def test_get_workouts_empty(self, client):
        """Test GET /api/workouts when no workouts exist."""
        response = client.get('/api/workouts/')
        assert response.status_code == 200
        assert response.json == []

    def test_get_workouts_by_member(self, client, created_member):
        """Test GET /api/workouts with member filter."""
        response = client.get(f'/api/workouts/?member={created_member.name}')
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_create_workout_success(self, client, created_member, sample_workout_data):
        """Test POST /api/workouts creates workout."""
        response = client.post(
            '/api/workouts/',
            data=json.dumps(sample_workout_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.json
        assert data['client_name'] == sample_workout_data['client_name']
        assert 'id' in data

    def test_get_workout_by_id_success(self, client, created_workout):
        """Test GET /api/workouts/<id> retrieves workout with exercises."""
        response = client.get(f'/api/workouts/{created_workout.id}')
        assert response.status_code == 200
        data = response.json
        assert data['id'] == created_workout.id
        assert 'exercises' in data

    def test_get_workout_by_id_not_found(self, client):
        """Test GET /api/workouts/<id> with non-existent ID."""
        response = client.get('/api/workouts/9999')
        assert response.status_code == 404

    def test_update_workout_success(self, client, created_workout):
        """Test PUT /api/workouts/<id> updates workout."""
        update_data = {'duration_min': 75}
        response = client.put(
            f'/api/workouts/{created_workout.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json['duration_min'] == 75

    def test_delete_workout_success(self, client, created_workout):
        """Test DELETE /api/workouts/<id> deletes workout."""
        response = client.delete(f'/api/workouts/{created_workout.id}')
        assert response.status_code == 200

        # Verify deletion
        get_response = client.get(f'/api/workouts/{created_workout.id}')
        assert get_response.status_code == 404

    @pytest.mark.negative
    def test_create_workout_invalid_data(self, client):
        """Test POST /api/workouts with invalid data."""
        invalid_data = {
            'client_name': 'John Doe',
            'date': '2024-01-01',
            'workout_type': 'Chest',
            'duration_min': -30  # Invalid negative duration
        }
        response = client.post(
            '/api/workouts/',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        assert response.status_code == 400


@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests for API workflows."""

    def test_complete_member_lifecycle(self, client, sample_member_data):
        """Test complete member lifecycle: create, read, update, delete."""
        # Create
        create_response = client.post(
            '/api/members/',
            data=json.dumps(sample_member_data),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        member_id = create_response.json['id']
        
        # Read
        read_response = client.get(f'/api/members/{member_id}')
        assert read_response.status_code == 200
        assert read_response.json['id'] == member_id
        
        # Update
        update_data = {'weight': 85.0}
        update_response = client.put(
            f'/api/members/{member_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert update_response.status_code == 200
        assert update_response.json['weight'] == 85.0
        
        # Delete
        delete_response = client.delete(f'/api/members/{member_id}')
        assert delete_response.status_code == 200

    def test_multiple_members_operations(self, client):
        """Test operations on multiple members."""
        members_data = [
            {
                'name': 'Member1',
                'age': 28,
                'height': 170.0,
                'weight': 70.0,
                'program': 'Fat Loss (FL) – 3 day',
                'target_weight': 65.0,
                'target_adherence': 80
            },
            {
                'name': 'Member2',
                'age': 35,
                'height': 185.0,
                'weight': 90.0,
                'program': 'Muscle Gain (MG) – PPL',
                'target_weight': 95.0,
                'target_adherence': 85
            }
        ]
        
        created_ids = []
        for data in members_data:
            response = client.post(
                '/api/members/',
                data=json.dumps(data),
                content_type='application/json'
            )
            assert response.status_code == 201
            created_ids.append(response.json['id'])
        
        # Get all
        get_all_response = client.get('/api/members/')
        assert get_all_response.status_code == 200
        assert len(get_all_response.json) == len(members_data)

    @pytest.mark.negative
    def test_error_handling_chain(self, client, created_member):
        """Test error handling in sequential operations."""
        # Try to create duplicate
        duplicate_data = {
            'name': created_member.name,
            'age': 25,
            'height': 170.0,
            'weight': 70.0,
            'program': 'Fat Loss (FL) – 3 day',
            'target_weight': 65.0,
            'target_adherence': 75
        }
        response = client.post(
            '/api/members/',
            data=json.dumps(duplicate_data),
            content_type='application/json'
        )
        assert response.status_code in [400, 409, 500]  # Error expected

    def test_response_content_type(self, client, created_member):
        """Test that all responses have correct content type."""
        response = client.get(f'/api/members/{created_member.id}')
        assert 'application/json' in response.content_type

    @pytest.mark.edge_case
    def test_api_with_boundary_values(self, client):
        """Test API with boundary value inputs."""
        boundary_data = {
            'name': 'X' * 100,  # Very long name
            'age': 1,
            'height': 100.0,
            'weight': 30.0,
            'program': 'Beginner (BG)',
            'target_weight': 40.0,
            'target_adherence': 0
        }
        response = client.post(
            '/api/members/',
            data=json.dumps(boundary_data),
            content_type='application/json'
        )
        assert response.status_code == 201

    @pytest.mark.integration
    def test_member_summary_with_data(self, client, created_member):
        """Test member summary endpoint with populated data."""
        response = client.get(f'/api/members/{created_member.name}/summary')
        assert response.status_code == 200
        data = response.json
        assert 'member' in data
        assert 'bmi' in data


class TestTrainerRoutes:
    """Test trainer API endpoints."""

    def test_get_trainers_empty(self, client):
        """Test GET /api/members/trainers when no trainers exist."""
        response = client.get('/api/members/trainers')
        assert response.status_code == 200
        assert response.json == []

    def test_create_trainer_success(self, client):
        """Test POST /api/members/trainers creates new trainer."""
        trainer_data = {
            'name': 'Coach John',
            'specialization': 'CrossFit',
            'experience_years': 5,
            'email': 'john@example.com'
        }
        response = client.post(
            '/api/members/trainers',
            data=json.dumps(trainer_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.json['name'] == trainer_data['name']

    def test_create_trainer_invalid_data(self, client):
        """Test POST /api/members/trainers with invalid data."""
        invalid_data = {
            'name': '',
            'specialization': 'CrossFit'
        }
        response = client.post(
            '/api/members/trainers',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_update_trainer_valid(self, client):
        """Test PUT /api/members/trainers/<id> updates trainer."""
        # First create
        trainer_data = {
            'name': 'Coach Jane',
            'specialization': 'Yoga',
            'experience_years': 3,
            'email': 'jane@example.com'
        }
        create_response = client.post(
            '/api/members/trainers',
            data=json.dumps(trainer_data),
            content_type='application/json'
        )
        trainer_id = create_response.json['id']

        # Then update
        update_data = {'specialization': 'Pilates'}
        response = client.put(
            f'/api/members/trainers/{trainer_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json['specialization'] == 'Pilates'

    def test_update_trainer_not_found(self, client):
        """Test PUT /api/members/trainers/<id> with non-existent trainer."""
        response = client.put(
            '/api/members/trainers/9999',
            data=json.dumps({'specialization': 'Updated'}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_delete_trainer_success(self, client):
        """Test DELETE /api/members/trainers/<id> deletes trainer."""
        # First create
        trainer_data = {
            'name': 'Coach Bob',
            'specialization': 'Powerlifting'
        }
        create_response = client.post(
            '/api/members/trainers',
            data=json.dumps(trainer_data),
            content_type='application/json'
        )
        trainer_id = create_response.json['id']

        # Then delete
        response = client.delete(f'/api/members/trainers/{trainer_id}')
        assert response.status_code == 200
        assert 'deleted' in response.json['message'].lower()

    def test_delete_trainer_not_found(self, client):
        """Test DELETE /api/members/trainers/<id> with non-existent trainer."""
        response = client.delete('/api/members/trainers/9999')
        assert response.status_code == 404


class TestMembersUpdateDelete:
    """Test member update and delete operations with error handling."""

    def test_update_member_not_found(self, client):
        """Test PUT /api/members/<id> with non-existent member."""
        response = client.put(
            '/api/members/9999',
            data=json.dumps({'program': 'Updated'}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_delete_member_not_found(self, client):
        """Test DELETE /api/members/<id> with non-existent member."""
        response = client.delete('/api/members/9999')
        assert response.status_code == 404


class TestSubscriptionFilters:
    """Test subscription endpoint filters and edge cases."""

    def test_get_subscriptions_by_member(self, client, created_subscription):
        """Test GET /api/subscriptions with member filter."""
        response = client.get(f'/api/subscriptions/?member={created_subscription.client_name}')
        assert response.status_code == 200
        data = response.json
        assert len(data) > 0
        assert data[0]['client_name'] == created_subscription.client_name

    def test_update_subscription_not_found(self, client):
        """Test PUT /api/subscriptions/<id> with non-existent subscription."""
        response = client.put(
            '/api/subscriptions/9999',
            data=json.dumps({'plan_name': 'Updated'}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_delete_subscription_not_found(self, client):
        """Test DELETE /api/subscriptions/<id> with non-existent subscription."""
        response = client.delete('/api/subscriptions/9999')
        assert response.status_code == 404

    def test_get_active_subscriptions(self, client, created_subscription):
        """Test GET /api/subscriptions/active."""
        response = client.get('/api/subscriptions/active')
        assert response.status_code == 200
        assert isinstance(response.json, list)


class TestWorkoutFilters:
    """Test workout endpoint filters and edge cases."""

    def test_get_workouts_empty_no_filter(self, client):
        """Test GET /api/workouts without member filter returns empty."""
        response = client.get('/api/workouts/')
        assert response.status_code == 200
        assert response.json == []

    def test_get_workouts_by_member_filter(self, client, created_workout):
        """Test GET /api/workouts with member filter."""
        response = client.get(f'/api/workouts/?member={created_workout.client_name}')
        assert response.status_code == 200
        data = response.json
        assert len(data) > 0
        assert data[0]['client_name'] == created_workout.client_name

    def test_update_workout_not_found(self, client):
        """Test PUT /api/workouts/<id> with non-existent workout."""
        response = client.put(
            '/api/workouts/9999',
            data=json.dumps({'duration_min': 100}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_delete_workout_not_found(self, client):
        """Test DELETE /api/workouts/<id> with non-existent workout."""
        response = client.delete('/api/workouts/9999')
        assert response.status_code == 404


class TestExceptionHandling:
    """Test exception handling in route handlers."""

    @patch('routes.members.MemberService.get_all_members')
    def test_get_members_generic_exception(self, mock_get_all, client):
        """Test GET /api/members with unexpected exception."""
        mock_get_all.side_effect = RuntimeError("Database connection error")
        response = client.get('/api/members/')
        assert response.status_code == 500
        assert 'error' in response.json

    @patch('routes.members.MemberService.get_member_by_id')
    def test_get_member_by_id_generic_exception(self, mock_get_by_id, client):
        """Test GET /api/members/<id> with unexpected exception."""
        mock_get_by_id.side_effect = RuntimeError("Database error")
        response = client.get('/api/members/1')
        assert response.status_code == 500
        assert 'error' in response.json

    @patch('routes.members.MemberService.create_member')
    def test_create_member_generic_exception(self, mock_create, client):
        """Test POST /api/members with unexpected exception."""
        mock_create.side_effect = RuntimeError("Database error")
        response = client.post(
            '/api/members/',
            data=json.dumps({'name': 'Test'}),
            content_type='application/json'
        )
        assert response.status_code == 500

    @patch('routes.members.MemberService.update_member')
    def test_update_member_generic_exception(self, mock_update, client):
        """Test PUT /api/members/<id> with unexpected exception."""
        mock_update.side_effect = RuntimeError("Database error")
        response = client.put(
            '/api/members/1',
            data=json.dumps({'program': 'Updated'}),
            content_type='application/json'
        )
        assert response.status_code == 500

    @patch('routes.subscriptions.SubscriptionService.get_all_subscriptions')
    def test_get_subscriptions_generic_exception(self, mock_get_all, client):
        """Test GET /api/subscriptions with unexpected exception."""
        mock_get_all.side_effect = RuntimeError("Database error")
        response = client.get('/api/subscriptions/')
        assert response.status_code == 500
        assert 'error' in response.json

    @patch('routes.subscriptions.SubscriptionService.get_subscription_by_id')
    def test_get_subscription_by_id_generic_exception(self, mock_get, client):
        """Test GET /api/subscriptions/<id> with unexpected exception."""
        mock_get.side_effect = RuntimeError("Database error")
        response = client.get('/api/subscriptions/1')
        assert response.status_code == 500

    @patch('routes.subscriptions.SubscriptionService.create_subscription')
    def test_create_subscription_generic_exception(self, mock_create, client):
        """Test POST /api/subscriptions with unexpected exception."""
        mock_create.side_effect = RuntimeError("Database error")
        response = client.post(
            '/api/subscriptions/',
            data=json.dumps({'client_name': 'Test'}),
            content_type='application/json'
        )
        assert response.status_code == 500

    @patch('routes.workouts.WorkoutService.get_workouts_by_member')
    def test_get_workouts_generic_exception(self, mock_get, client):
        """Test GET /api/workouts with unexpected exception."""
        mock_get.side_effect = RuntimeError("Database error")
        response = client.get('/api/workouts/?member=test')
        assert response.status_code == 500

    @patch('routes.workouts.WorkoutService.get_workout_with_exercises')
    def test_get_workout_generic_exception(self, mock_get, client):
        """Test GET /api/workouts/<id> with unexpected exception."""
        mock_get.side_effect = RuntimeError("Database error")
        response = client.get('/api/workouts/1')
        assert response.status_code == 500

    @patch('routes.workouts.WorkoutService.create_workout')
    def test_create_workout_generic_exception(self, mock_create, client):
        """Test POST /api/workouts with unexpected exception."""
        mock_create.side_effect = RuntimeError("Database error")
        response = client.post(
            '/api/workouts/',
            data=json.dumps({'client_name': 'Test'}),
            content_type='application/json'
        )
        assert response.status_code == 500


@pytest.mark.integration
class TestAPIErrorHandling:
    """Test API error handling and edge cases."""

    @pytest.mark.negative
    def test_malformed_json(self, client):
        """Test API with malformed JSON."""
        response = client.post(
            '/api/members/',
            data='{ invalid json }',
            content_type='application/json'
        )
        assert response.status_code in [400, 415, 500]

    @pytest.mark.negative
    def test_missing_content_type(self, client, sample_member_data):
        """Test API request without content-type header."""
        response = client.post(
            '/api/members/',
            data=json.dumps(sample_member_data)
            # No content_type specified
        )
        # Should still work or give clear error
        assert response.status_code in [200, 201, 400, 415, 500]

    @pytest.mark.edge_case
    def test_empty_payload(self, client):
        """Test API with empty payload."""
        response = client.post(
            '/api/members/',
            data='{}',
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'error' in response.json

    @pytest.mark.negative
    def test_special_characters_in_name(self, client):
        """Test member creation with special characters in name."""
        data = {
            'name': 'José García-López #1',
            'age': 30,
            'height': 180.0,
            'weight': 80.0,
            'program': 'Muscle Gain (MG) – PPL',
            'target_weight': 85.0,
            'target_adherence': 80
        }
        response = client.post(
            '/api/members/',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 201
