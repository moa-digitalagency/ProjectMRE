from app import create_app
from utils.extensions import db
from models.user import User
from models.project import Project

# Initialize the Flask application
app = create_app()

def init_db():
    """Initializes the database with tables and necessary columns."""
    with app.app_context():
        # Create all tables defined in models
        db.create_all()
        print("Database tables created.")

        # Check if admin user exists, if not create one
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created (username: admin, password: admin).")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()
