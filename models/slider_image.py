from utils.extensions import db

class SliderImage(db.Model):
    __tablename__ = 'slider_images'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(256), nullable=False)
    alt_text = db.Column(db.String(256))
    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<SliderImage {self.image_url}>'
