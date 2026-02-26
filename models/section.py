from utils.extensions import db

class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    image_url = db.Column(db.String(256))

    def __repr__(self):
        return f'<Section {self.slug}>'
