from flask import Blueprint, request, jsonify
from services.subscription_service import SubscriptionService

subscriptions_bp = Blueprint('subscriptions', __name__)

@subscriptions_bp.route('/', methods=['GET'])
def get_subscriptions():
    try:
        member_name = request.args.get('member')
        if member_name:
            subscriptions = SubscriptionService.get_subscriptions_by_member(member_name)
        else:
            subscriptions = SubscriptionService.get_all_subscriptions()
        return jsonify([sub.to_dict() for sub in subscriptions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscriptions_bp.route('/<int:subscription_id>', methods=['GET'])
def get_subscription(subscription_id):
    try:
        subscription = SubscriptionService.get_subscription_by_id(subscription_id)
        if not subscription:
            return jsonify({'error': 'Subscription not found'}), 404
        return jsonify(subscription.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscriptions_bp.route('/', methods=['POST'])
def create_subscription():
    try:
        data = request.get_json()
        subscription = SubscriptionService.create_subscription(data)
        return jsonify(subscription.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscriptions_bp.route('/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    try:
        data = request.get_json()
        subscription = SubscriptionService.update_subscription(subscription_id, data)
        return jsonify(subscription.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscriptions_bp.route('/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    try:
        SubscriptionService.delete_subscription(subscription_id)
        return jsonify({'message': 'Subscription deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscriptions_bp.route('/active', methods=['GET'])
def get_active_subscriptions():
    try:
        subscriptions = SubscriptionService.get_active_subscriptions()
        return jsonify([sub.to_dict() for sub in subscriptions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500