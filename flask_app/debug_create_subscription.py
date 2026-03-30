from app import app
from models.database import db
from models.member import Member
from services.subscription_service import SubscriptionService
from datetime import date, timedelta
import traceback

with app.app_context():
    db.drop_all()
    db.create_all()
    m = Member(name='John Doe', age=30, height=180.0, weight=80.0, program='BG', calories=2500, target_weight=75.0, target_adherence=80)
    db.session.add(m)
    db.session.commit()
    data = {'client_name': 'John Doe', 'plan_name': 'Premium', 'start_date': date.today().isoformat(), 'end_date': (date.today() + timedelta(days=365)).isoformat()}
    try:
        s = SubscriptionService.create_subscription(data)
        print('created', s.id, s.start_date, s.end_date, s.fee)
    except Exception:
        traceback.print_exc()