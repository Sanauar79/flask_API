from flask import Blueprint, request, jsonify,session
from app.models import Contact, User
from app.extensions import db
from app.utils.email_utils import send_email_to_user, send_email_to_admin

contact_bp = Blueprint('contact', __name__, url_prefix='/api')

@contact_bp.route('/contact', methods=['POST'])
def contact():
    errors = {}
    if 'role' not in session or session['role'] != 'user':
        return jsonify({"error": "unauthorized"}), 403

    if 'user_id' not in session:
        return jsonify({"error": "Session expired or invalid"}), 401

    data = request.json
    name = data.get("name")
    email = data.get("email")
    address = data.get("address")
    phone = data.get("phone")
    message = data.get("message")
    user_id = session['user_id']

    if not name and not email and not address and not phone and not message:
        return jsonify({'error': 'All fields are required'}), 400

    if not name:
        errors['name'] = 'Name is required.'
    if not email:
        errors['email'] = 'Email is required.'
    elif User.query.filter_by(email=email).first():
        errors['email'] = 'Email already exists.'
    if not message:
        errors['message'] = 'Message is required.'
    elif len(message) < 6:
        errors['message'] = 'Message must be at least 6 characters.'

    if  errors:
        return jsonify({'errors': errors}), 400

    new_msg = Contact(
        name=name,
        email=email,
        address=address,
        phone=phone,
        message=message,
        user_id=user_id
    )

    db.session.add(new_msg)
    db.session.commit()

    send_email_to_user(name, email)
    send_email_to_admin(name, email, phone, message)

    return jsonify({"message": "Message Sent to Admin"}), 201

