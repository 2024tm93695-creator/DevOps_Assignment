from models.database import db

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)  # in cm
    weight = db.Column(db.Float, nullable=False)  # in kg
    program = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    target_weight = db.Column(db.Float, nullable=False)
    target_adherence = db.Column(db.Integer, nullable=False)
    membership_status = db.Column(db.String(50), default='active')
    membership_end = db.Column(db.Date, nullable=True)

    # Relationships
    progress = db.relationship('Progress', backref='member', lazy=True)
    workouts = db.relationship('Workout', backref='member', lazy=True)
    metrics = db.relationship('Metric', backref='member', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'program': self.program,
            'calories': self.calories,
            'target_weight': self.target_weight,
            'target_adherence': self.target_adherence,
            'membership_status': self.membership_status,
            'membership_end': self.membership_end.isoformat() if self.membership_end else None
        }