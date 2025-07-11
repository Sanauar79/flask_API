from flask import Blueprint, jsonify, request,session
from app.models import Contact , User
from collections import OrderedDict
from app.extensions import db
import csv, io
from flask import send_file

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route("/users", methods=["GET"])
def api_users():
        if 'role' not in session or session['role'] != 'admin':
         return jsonify({"error": "unauthorized"}), 403
    
        users = User.query.all()
        return jsonify([
        {"id": u.id, "name": u.name, "email": u.email, "role": u.role}
        for u in users
    ])

@admin_bp.route('/messages')
def list_messages():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({"error": "unauthorized"}), 403

    messages = Contact.query.order_by(Contact.id.desc()).all()
    formatted = []

    for msg in messages:
        formatted.append(OrderedDict([
            ("id", msg.id),
            ("name", msg.name),
            ("email", msg.email),
            ("message", msg.message)
        ]))
        
    return jsonify({"messages": formatted}) 

@admin_bp.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = Contact.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200

@admin_bp.route('/messages/<int:id>', methods=['PUT'])
def update_message(id):
    msg = Contact.query.get_or_404(id)
    data = request.json
    for field in ['name', 'email', 'address', 'phone', 'message']:
        setattr(msg, field, data.get(field, getattr(msg, field)))
    db.session.commit()
    return jsonify({"message": "Updated"}), 200

@admin_bp.route('/export')
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Message'])

    for m in Contact.query.all():
        writer.writerow([m.id, m.name, m.email, m.phone, m.message])

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', download_name='messages.csv', as_attachment=True)
