from flask import Blueprint, request, jsonify
from models import members

members_bp = Blueprint('members', __name__)

# Create a new member
@members_bp.route('/members', methods=['POST'])
def create_member():
    data = request.json
    member_id = len(members) + 1
    members[member_id] = {
        "id": member_id,
        "name": data["name"],
        "email": data["email"],
        "membership_date": data["membership_date"]
    }
    return jsonify({"message": "Member added successfully", "member": members[member_id]}), 201

# Get all members
@members_bp.route('/members', methods=['GET'])
def get_members():
    return jsonify(list(members.values())), 200

# Update a member
@members_bp.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    if member_id not in members:
        return jsonify({"error": "Member not found"}), 404
    data = request.json
    members[member_id].update(data)
    return jsonify({"message": "Member updated", "member": members[member_id]}), 200

# Delete a member
@members_bp.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if member_id not in members:
        return jsonify({"error": "Member not found"}), 404
    del members[member_id]
    return jsonify({"message": "Member deleted"}), 200
