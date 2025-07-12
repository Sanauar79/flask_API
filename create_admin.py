# create_admin.py

from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    admin_email = "admin@gmail.com"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            name="Admin",
            email=admin_email,
            role="admin",
            is_verified=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created.")
    else:
        print("⚠️ Admin already exists.")
