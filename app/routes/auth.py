from flask import Blueprint, request, jsonify, session
from itsdangerous import URLSafeTimedSerializer
from app.models import User
from app.extensions import db, mail
from flask_mail import Message

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

serializer = URLSafeTimedSerializer("your_secret_key")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    errors = {}

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not name and not email and not password:
        return jsonify({'error': 'All fields are required'}), 400

    if not name:
        errors['name'] = 'Name is required.'
    if not email:
        errors['email'] = 'Email is required.'
    elif User.query.filter_by(email=email).first():
        errors['email'] = 'Email already exists.'
    if not password:
        errors['password'] = 'Password is required.'
    elif len(password) < 6:
        errors['password'] = 'Password must be at least 6 characters.'

    if  errors:
        return jsonify({'errors': errors}), 400

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = serializer.dumps(email, salt='email-confirm')
    confirm_url = f"{request.url_root}api/confirm/{token}"

    msg = Message("Confirm Email", recipients=[email])
    msg.body = f"Click here to confirm your email: {confirm_url}"
    mail.send(msg)

    return jsonify({"message": "Registered. Check your email to confirm."}), 201

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
    except:
        return jsonify({"error": "Invalid or expired token"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_verified = True
    db.session.commit()
    return jsonify({"message": "Email confirmed"}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({"error": "Invalid credentials"}), 401
    if not user.is_verified:
        return jsonify({"error": "Please verify your email"}), 403
    
    session['user_id'] = user.id
    session['email'] = user.email
    session['role'] = user.role
    return jsonify({"message": "Login successful", "role": user.role}), 200

@auth_bp.route("/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})
