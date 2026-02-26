from flask import Blueprint, render_template
from models.section import Section
from models.slider_image import SliderImage

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    sections_list = Section.query.all()
    # Convert list to dictionary keyed by slug for easy access in template
    sections = {section.slug: section for section in sections_list}

    slider_images = SliderImage.query.order_by(SliderImage.order).all()

    return render_template('index.html', sections=sections, slider_images=slider_images)
