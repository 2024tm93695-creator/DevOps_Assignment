from flask import Blueprint, request, jsonify
from services.member_service import MemberService
from services.trainer_service import TrainerService

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['GET'])
def get_members():
    try:
        members = MemberService.get_all_members()
        return jsonify([member.to_dict() for member in members]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = MemberService.get_member_by_id(member_id)
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        return jsonify(member.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/', methods=['POST'])
def create_member():
    try:
        data = request.get_json()
        member = MemberService.create_member(data)
        return jsonify(member.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    try:
        data = request.get_json()
        member = MemberService.update_member(member_id, data)
        return jsonify(member.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        MemberService.delete_member(member_id)
        return jsonify({'message': 'Member deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/<name>/summary', methods=['GET'])
def get_member_summary(name):
    try:
        summary = MemberService.get_member_summary(name)
        return jsonify(summary), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Trainer routes
@members_bp.route('/trainers', methods=['GET'])
def get_trainers():
    try:
        trainers = TrainerService.get_all_trainers()
        return jsonify([trainer.to_dict() for trainer in trainers]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/trainers', methods=['POST'])
def create_trainer():
    try:
        data = request.get_json()
        trainer = TrainerService.create_trainer(data)
        return jsonify(trainer.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/trainers/<int:trainer_id>', methods=['PUT'])
def update_trainer(trainer_id):
    try:
        data = request.get_json()
        trainer = TrainerService.update_trainer(trainer_id, data)
        return jsonify(trainer.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/trainers/<int:trainer_id>', methods=['DELETE'])
def delete_trainer(trainer_id):
    try:
        TrainerService.delete_trainer(trainer_id)
        return jsonify({'message': 'Trainer deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500