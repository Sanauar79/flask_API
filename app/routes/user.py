from flask import Blueprint, jsonify, session
from app.models import Contact
from app.extensions import db

messages_bp = Blueprint('messages', __name__, url_prefix='/api/messages')

@messages_bp.route('/my', methods=['GET'])
def get_user_messages():
    user_id = session.get('user_id')
    if 'role' not in session or session['role'] != 'user':
        return jsonify({"error": "unauthorized"}), 403
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    messages = Contact.query.filter_by(user_id=user_id).all()

    data = [
        {
            "id": msg.id,
            "name": msg.name,
            "email": msg.email,
            "phone": msg.phone,
            "address": msg.address,
            "message": msg.message
        }
        for msg in messages
    ]

    return jsonify({"messages": data}), 200
