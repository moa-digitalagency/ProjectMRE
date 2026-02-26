from flask import Blueprint, render_template
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # List of available section images
    all_images = [f'section_{i}.jpg' for i in range(1, 9)]

    # Select 4 unique random images for the slider
    slider_images = random.sample(all_images, 4)

    return render_template('index.html', slider_images=slider_images)
