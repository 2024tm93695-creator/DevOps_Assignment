from models.database import db

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey('member.name'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    workout_type = db.Column(db.String(100), nullable=False)
    duration_min = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    # Relationship
    exercises = db.relationship('Exercise', backref='workout', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'date': self.date.isoformat(),
            'workout_type': self.workout_type,
            'duration_min': self.duration_min,
            'notes': self.notes
        }

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'workout_id': self.workout_id,
            'name': self.name,
            'sets': self.sets,
            'reps': self.reps,
            'weight': self.weight
        }