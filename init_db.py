from app import create_app
from utils.extensions import db
from models.user import User
from models.project import Project
from models.section import Section
from models.slider_image import SliderImage
from models.site_settings import SiteSettings

import os

# Initialize the Flask application
app = create_app()

def init_db():
    """Initializes the database with tables and necessary columns."""

    # Create required directories for the application to function
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Create cache directory
    cache_dir = os.path.join(base_dir, 'cache')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        print(f"Created cache directory at {cache_dir}")
        try:
            os.chmod(cache_dir, 0o775)
        except PermissionError:
            print("Warning: Could not set 775 permissions on cache directory")

    # Create uploads directory
    uploads_dir = os.path.join(base_dir, 'statics', 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir, exist_ok=True)
        print(f"Created uploads directory at {uploads_dir}")
        try:
            os.chmod(uploads_dir, 0o775)
        except PermissionError:
            print("Warning: Could not set 775 permissions on uploads directory")

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

        # Seed Slider Images
        if SliderImage.query.count() == 0:
            print("Seeding Slider Images...")
            slider_data = [
                ("https://images.unsplash.com/photo-1539020140153-e479b8c22e70?auto=format&fit=crop&q=80&w=2000", "Vue d'ensemble des villas", 1),
                ("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&q=80&w=2000", "Clubhouse et vue Atlas", 2),
                ("https://images.unsplash.com/photo-1552084117-56a98a414520?auto=format&fit=crop&q=80&w=2000", "Villas avec vue sur l'Atlas", 3),
                ("https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?auto=format&fit=crop&q=80&w=2000", "Entrée sécurisée", 4)
            ]
            for url, alt, order in slider_data:
                db.session.add(SliderImage(image_url=url, alt_text=alt, order=order))
            db.session.commit()
            print("Slider Images seeded.")
        else:
             print("Slider Images already exist.")

        # Seed Sections
        if Section.query.count() == 0:
            print("Seeding Sections...")
            sections_data = [
                ("contexte", "Contexte & Ambition", "https://images.unsplash.com/photo-1539020140153-e479b8c22e70?auto=format&fit=crop&q=80&w=1000"),
                ("domaine", "Aménagement & Concept", "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?auto=format&fit=crop&q=80&w=1000"),
                ("mobilite", "Mobilité & Accessibilité", "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&q=80&w=1000"),
                ("premium", "Positionnement Premium", "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&q=80&w=1000"),
                ("budget", "Budget & Investissement", "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=1000"),
                ("commercialisation", "Commercialisation", "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&q=80&w=1000"),
                ("gouvernance", "Gouvernance & Exploitation", "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&q=80&w=1000"),
                ("partenariats", "Partenariats", "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?auto=format&fit=crop&q=80&w=1000")
            ]
            for slug, title, url in sections_data:
                db.session.add(Section(slug=slug, title=title, image_url=url))
            db.session.commit()
            print("Sections seeded.")
        else:
            print("Sections already exist.")

        # Seed Site Settings
        if SiteSettings.query.count() == 0:
            print("Seeding Site Settings...")
            default_settings = SiteSettings(
                site_name="Mon Site Vitrine",
                meta_title="Accueil - Mon Site Vitrine",
                meta_description="Bienvenue sur notre site vitrine.",
                favicon_url="img/favicon.svg"
            )
            db.session.add(default_settings)
            db.session.commit()
            print("Site Settings seeded.")
        else:
            print("Site Settings already exist.")


if __name__ == '__main__':
    init_db()
