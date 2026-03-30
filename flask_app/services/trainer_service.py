from models.database import db
from models.trainer import Trainer
from utils.validations import validate_trainer_data

class TrainerService:
    @staticmethod
    def get_all_trainers():
        return Trainer.query.all()

    @staticmethod
    def get_trainer_by_id(trainer_id):
        return Trainer.query.get(trainer_id)

    @staticmethod
    def get_trainer_by_name(name):
        return Trainer.query.filter_by(name=name).first()

    @staticmethod
    def create_trainer(data):
        validate_trainer_data(data)
        
        trainer = Trainer(
            name=data['name'],
            specialization=data.get('specialization'),
            experience_years=data.get('experience_years'),
            email=data.get('email')
        )
        
        db.session.add(trainer)
        db.session.commit()
        return trainer

    @staticmethod
    def update_trainer(trainer_id, data):
        trainer = Trainer.query.get(trainer_id)
        if not trainer:
            raise ValueError("Trainer not found")
        
        validate_trainer_data(data, update=True)
        
        for key, value in data.items():
            if hasattr(trainer, key):
                setattr(trainer, key, value)
        
        db.session.commit()
        return trainer

    @staticmethod
    def delete_trainer(trainer_id):
        trainer = Trainer.query.get(trainer_id)
        if not trainer:
            raise ValueError("Trainer not found")
        
        db.session.delete(trainer)
        db.session.commit()
        return True