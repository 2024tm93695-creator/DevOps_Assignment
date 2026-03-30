from models.database import db
from models.subscription import Subscription
from utils.validations import validate_subscription_data
from utils.calculations import calculate_subscription_fee
from datetime import date

class SubscriptionService:
    @staticmethod
    def get_all_subscriptions():
        return Subscription.query.all()

    @staticmethod
    def get_subscriptions_by_member(member_name):
        return Subscription.query.filter_by(client_name=member_name).order_by(Subscription.start_date.desc()).all()

    @staticmethod
    def get_subscription_by_id(subscription_id):
        return Subscription.query.get(subscription_id)

    @staticmethod
    def create_subscription(data):
        validate_subscription_data(data)
        
        # Calculate fee based on plan
        fee = calculate_subscription_fee(data['plan_name'])
        
        # Convert date strings to date objects if needed
        start_date = data['start_date']
        end_date = data['end_date']
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)
        
        subscription = Subscription(
            client_name=data['client_name'],
            plan_name=data['plan_name'],
            start_date=start_date,
            end_date=end_date,
            fee=fee
        )
        
        db.session.add(subscription)
        db.session.commit()
        return subscription

    @staticmethod
    def update_subscription(subscription_id, data):
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")
        
        validate_subscription_data(data, update=True)
        
        for key, value in data.items():
            if hasattr(subscription, key):
                setattr(subscription, key, value)
        
        # Recalculate fee if plan changed
        if 'plan_name' in data:
            subscription.fee = calculate_subscription_fee(subscription.plan_name)
        
        db.session.commit()
        return subscription

    @staticmethod
    def delete_subscription(subscription_id):
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")
        
        db.session.delete(subscription)
        db.session.commit()
        return True

    @staticmethod
    def get_active_subscriptions():
        from datetime import date
        return Subscription.query.filter(
            Subscription.status == 'active',
            Subscription.end_date >= date.today()
        ).all()