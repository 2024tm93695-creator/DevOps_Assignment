from models.database import db

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey('member.name'), nullable=False)
    week = db.Column(db.String(20), nullable=False)  # e.g., '2023-W01'
    adherence = db.Column(db.Integer, nullable=False)  # percentage

    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'week': self.week,
            'adherence': self.adherence
        }