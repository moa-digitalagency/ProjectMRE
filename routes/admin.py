import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from models.section import Section
from models.slider_image import SliderImage
from utils.extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/')
def dashboard():
    sections = Section.query.all()
    slider_images = SliderImage.query.order_by(SliderImage.order).all()
    return render_template('admin.html', sections=sections, slider_images=slider_images)

@admin_bp.route('/section/update/<int:id>', methods=['POST'])
def update_section(id):
    section = Section.query.get_or_404(id)

    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Ensure unique filename to prevent overwriting or caching issues?
            # For simplicity, we keep original filename but might be good to prepend ID or timestamp

            # Remove old image if it exists and is a local file
            if section.image_url and section.image_url.startswith('uploads/'):
                 old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], section.image_url.replace('uploads/', ''))
                 if os.path.exists(old_image_path):
                     os.remove(old_image_path)

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            section.image_url = f'uploads/{filename}'
            db.session.commit()
            flash('Image updated successfully.', 'success')
        elif file.filename != '':
             flash('Invalid file type.', 'error')

    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/slider/add', methods=['POST'])
def add_slider_image():
    if 'image' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('admin.dashboard'))

    file = request.files['image']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('admin.dashboard'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        alt_text = request.form.get('alt_text', '')
        order = request.form.get('order', 0)

        new_image = SliderImage(
            image_url=f'uploads/{filename}',
            alt_text=alt_text,
            order=order
        )
        db.session.add(new_image)
        db.session.commit()
        flash('Slider image added successfully.', 'success')
    else:
        flash('Invalid file type.', 'error')

    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/slider/delete/<int:id>', methods=['POST'])
def delete_slider_image(id):
    image = SliderImage.query.get_or_404(id)

    # Remove file if it is local
    if image.image_url.startswith('uploads/'):
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.image_url.replace('uploads/', ''))
        if os.path.exists(file_path):
            os.remove(file_path)

    db.session.delete(image)
    db.session.commit()
    flash('Slider image deleted successfully.', 'success')

    return redirect(url_for('admin.dashboard'))
