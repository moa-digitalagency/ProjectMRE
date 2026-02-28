import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from PIL import Image
from models.section import Section
from models.slider_image import SliderImage
from models.site_settings import SiteSettings
from utils.extensions import db
from app import cache

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'ico'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_and_save_image(file_storage, filename):
    """
    Saves an uploaded image. If it's an image that can be optimized (jpg, png, etc.),
    it resizes it to a max of 1920x1080 and converts it to WebP.
    SVG and ICO files are saved as is.
    Returns the final filename saved.
    """
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)

    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if ext in ['svg', 'ico', 'gif']:
        # Save as is for vector/animated/icon formats
        final_filename = filename
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], final_filename)
        file_storage.save(save_path)
        return final_filename

    # Process image with Pillow
    try:
        img = Image.open(file_storage)

        # Convert P to RGBA to preserve transparency, but do not convert RGBA to RGB
        # as WebP natively supports alpha channels.
        if img.mode == "P":
            img = img.convert("RGBA")
        elif img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")

        # Resize if larger than 1920x1080 while maintaining aspect ratio
        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)

        # Change filename to .webp
        name_without_ext = filename.rsplit('.', 1)[0]
        final_filename = f"{name_without_ext}.webp"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], final_filename)

        # Save compressed WebP
        img.save(save_path, 'WEBP', quality=85, optimize=True)
        return final_filename
    except Exception as e:
        # Fallback to saving original if processing fails
        print(f"Error processing image {filename}: {e}")
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file_storage.seek(0) # Reset file pointer just in case
        file_storage.save(save_path)
        return filename

@admin_bp.route('/')
def dashboard():
    sections = Section.query.all()
    slider_images = SliderImage.query.order_by(SliderImage.order).all()
    site_settings = SiteSettings.query.first()
    return render_template('admin.html', sections=sections, slider_images=slider_images, site_settings=site_settings)

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

            saved_filename = process_and_save_image(file, filename)
            section.image_url = f'uploads/{saved_filename}'
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
        saved_filename = process_and_save_image(file, filename)

        alt_text = request.form.get('alt_text', '')
        try:
            order = int(request.form.get('order', 0))
        except (ValueError, TypeError):
            order = 0

        new_image = SliderImage(
            image_url=f'uploads/{saved_filename}',
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

@admin_bp.route('/settings/update', methods=['POST'])
def update_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)

    settings.site_name = request.form.get('site_name')
    settings.meta_title = request.form.get('meta_title')
    settings.meta_description = request.form.get('meta_description')
    settings.meta_keywords = request.form.get('meta_keywords')
    settings.og_title = request.form.get('og_title')
    settings.og_description = request.form.get('og_description')
    settings.contact_email = request.form.get('contact_email')
    settings.contact_phone = request.form.get('contact_phone')

    # Handle Favicon
    if 'favicon' in request.files:
        file = request.files['favicon']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"favicon_{file.filename}")
            saved_filename = process_and_save_image(file, filename)
            settings.favicon_url = f'uploads/{saved_filename}'

    # Handle Open Graph Image
    if 'og_image' in request.files:
        file = request.files['og_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"og_{file.filename}")
            saved_filename = process_and_save_image(file, filename)
            settings.og_image_url = f'uploads/{saved_filename}'

    db.session.commit()
    # Invalidate cached settings
    cache.delete('site_settings')
    flash('Paramètres mis à jour avec succès.', 'success')
    return redirect(url_for('admin.dashboard'))
