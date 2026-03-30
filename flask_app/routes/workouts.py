from flask import Blueprint, request, jsonify
from services.workout_service import WorkoutService

workouts_bp = Blueprint('workouts', __name__)

@workouts_bp.route('/', methods=['GET'])
def get_workouts():
    try:
        member_name = request.args.get('member')
        if member_name:
            workouts = WorkoutService.get_workouts_by_member(member_name)
        else:
            # This would need a method to get all workouts, but for now return empty
            workouts = []
        return jsonify([workout.to_dict() for workout in workouts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@workouts_bp.route('/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    try:
        workout = WorkoutService.get_workout_with_exercises(workout_id)
        return jsonify(workout), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@workouts_bp.route('/', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()
        workout = WorkoutService.create_workout(data)
        return jsonify(workout.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@workouts_bp.route('/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    try:
        data = request.get_json()
        workout = WorkoutService.update_workout(workout_id, data)
        return jsonify(workout.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@workouts_bp.route('/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    try:
        WorkoutService.delete_workout(workout_id)
        return jsonify({'message': 'Workout deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500