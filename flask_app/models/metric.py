from models.database import db

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey('member.name'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=True)
    waist = db.Column(db.Float, nullable=True)
    bodyfat = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'date': self.date.isoformat(),
            'weight': self.weight,
            'waist': self.waist,
            'bodyfat': self.bodyfat
        }