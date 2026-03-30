from models.database import db
from models.member import Member
from models.progress import Progress
from models.workout import Workout, Exercise
from models.metric import Metric
from models.subscription import Subscription
from utils.validations import validate_member_data
from utils.calculations import calculate_calories, calculate_bmi
from datetime import datetime

class MemberService:
    @staticmethod
    def get_all_members():
        return Member.query.all()

    @staticmethod
    def get_member_by_id(member_id):
        return Member.query.get(member_id)

    @staticmethod
    def get_member_by_name(name):
        return Member.query.filter_by(name=name).first()

    @staticmethod
    def create_member(data):
        validate_member_data(data)
        
        # Calculate calories based on program
        calories = calculate_calories(data['weight'], data['height'], data['age'], data.get('program', ''))
        
        member = Member(
            name=data['name'],
            age=data['age'],
            height=data['height'],
            weight=data['weight'],
            program=data['program'],
            calories=calories,
            target_weight=data['target_weight'],
            target_adherence=data['target_adherence']
        )
        
        db.session.add(member)
        db.session.commit()
        return member

    @staticmethod
    def update_member(member_id, data):
        member = Member.query.get(member_id)
        if not member:
            raise ValueError("Member not found")
        
        validate_member_data(data, update=True)
        
        for key, value in data.items():
            if hasattr(member, key):
                setattr(member, key, value)
        
        # Recalculate calories if relevant fields changed
        if any(k in data for k in ['weight', 'height', 'age', 'program']):
            member.calories = calculate_calories(member.weight, member.height, member.age, member.program)
        
        db.session.commit()
        return member

    @staticmethod
    def delete_member(member_id):
        member = Member.query.get(member_id)
        if not member:
            raise ValueError("Member not found")
        
        db.session.delete(member)
        db.session.commit()
        return True

    @staticmethod
    def get_member_summary(name):
        member = Member.query.filter_by(name=name).first()
        if not member:
            raise ValueError("Member not found")
        
        # Get recent progress
        recent_progress = Progress.query.filter_by(client_name=name).order_by(Progress.week.desc()).limit(4).all()
        
        # Get recent workouts
        recent_workouts = Workout.query.filter_by(client_name=name).order_by(Workout.date.desc()).limit(5).all()
        
        # Get latest metrics
        latest_metric = Metric.query.filter_by(client_name=name).order_by(Metric.date.desc()).first()
        
        # Calculate BMI
        bmi = calculate_bmi(member.weight, member.height)
        
        return {
            'member': member.to_dict(),
            'bmi': bmi,
            'recent_progress': [p.to_dict() for p in recent_progress],
            'recent_workouts': [w.to_dict() for w in recent_workouts],
            'latest_metrics': latest_metric.to_dict() if latest_metric else None
        }