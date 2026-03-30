from models.database import db
from datetime import datetime

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey('member.name'), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    end_date = db.Column(db.Date, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='active')  # active, expired, cancelled

    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'plan_name': self.plan_name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'fee': self.fee,
            'status': self.status
        }