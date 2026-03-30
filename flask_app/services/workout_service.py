from models.database import db
from models.workout import Workout, Exercise
from utils.validations import validate_workout_data, validate_exercise_data
from datetime import date, datetime

class WorkoutService:
    @staticmethod
    def get_workouts_by_member(member_name):
        return Workout.query.filter_by(client_name=member_name).order_by(Workout.date.desc()).all()

    @staticmethod
    def get_workout_by_id(workout_id):
        return Workout.query.get(workout_id)

    @staticmethod
    def create_workout(data):
        validate_workout_data(data)
        
        # Convert date string to date object if needed
        workout_date = data['date']
        if isinstance(workout_date, str):
            workout_date = datetime.fromisoformat(workout_date).date()
        
        workout = Workout(
            client_name=data['client_name'],
            date=workout_date,
            workout_type=data['workout_type'],
            duration_min=data['duration_min'],
            notes=data.get('notes', '')
        )
        
        db.session.add(workout)
        db.session.commit()
        
        # Add exercises if provided
        if 'exercises' in data:
            for exercise_data in data['exercises']:
                validate_exercise_data(exercise_data)
                exercise = Exercise(
                    workout_id=workout.id,
                    name=exercise_data['name'],
                    sets=exercise_data['sets'],
                    reps=exercise_data['reps'],
                    weight=exercise_data.get('weight')
                )
                db.session.add(exercise)
            db.session.commit()
        
        return workout

    @staticmethod
    def update_workout(workout_id, data):
        workout = Workout.query.get(workout_id)
        if not workout:
            raise ValueError("Workout not found")
        
        validate_workout_data(data, update=True)
        
        for key, value in data.items():
            if hasattr(workout, key) and key != 'exercises':
                setattr(workout, key, value)
        
        # Update exercises if provided
        if 'exercises' in data:
            # Remove existing exercises
            Exercise.query.filter_by(workout_id=workout_id).delete()
            
            # Add new exercises
            for exercise_data in data['exercises']:
                validate_exercise_data(exercise_data)
                exercise = Exercise(
                    workout_id=workout.id,
                    name=exercise_data['name'],
                    sets=exercise_data['sets'],
                    reps=exercise_data['reps'],
                    weight=exercise_data.get('weight')
                )
                db.session.add(exercise)
        
        db.session.commit()
        return workout

    @staticmethod
    def delete_workout(workout_id):
        workout = Workout.query.get(workout_id)
        if not workout:
            raise ValueError("Workout not found")
        
        # Delete associated exercises
        Exercise.query.filter_by(workout_id=workout_id).delete()
        
        db.session.delete(workout)
        db.session.commit()
        return True

    @staticmethod
    def get_workout_with_exercises(workout_id):
        workout = Workout.query.get(workout_id)
        if not workout:
            raise ValueError("Workout not found")
        
        exercises = Exercise.query.filter_by(workout_id=workout_id).all()
        
        workout_dict = workout.to_dict()
        workout_dict['exercises'] = [e.to_dict() for e in exercises]
        
        return workout_dict