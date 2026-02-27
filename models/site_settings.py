from utils.extensions import db

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)

    # General
    site_name = db.Column(db.String(128), default="Mon Site Vitrine")
    favicon_url = db.Column(db.String(256))

    # SEO
    meta_title = db.Column(db.String(128))
    meta_description = db.Column(db.Text)
    meta_keywords = db.Column(db.String(256))

    # Advanced SEO (Open Graph)
    og_title = db.Column(db.String(128))
    og_description = db.Column(db.Text)
    og_image_url = db.Column(db.String(256))

    # Contact
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))

    def __repr__(self):
        return f'<SiteSettings {self.site_name}>'
