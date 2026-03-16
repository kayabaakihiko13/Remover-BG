from flask import (
    Blueprint, 
    render_template, 
    request, 
    session, 
    url_for, 
    current_app
)
from ..services.image_processor import ImageProcessor

upload_bp = Blueprint('upload', __name__, url_prefix='/')


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload_page():
    if request.method == 'GET':
        return render_template('view/upload.html', success=False)
    
    if request.method == 'POST':
        try:
            processor = ImageProcessor(
                upload_dir=current_app.config['UPLOAD_FOLDER'],
                model_dir=current_app.config['MODEL_DIR']
            )
            
            file = request.files.get('file')
            result = processor.process_image(file)  # ✅ Result dict dari service
            
            # ✅ Gunakan key yang ADA di result:
            session['processed_file_name'] = result['processed_name']
            session['download_filename'] = result['download_name']
            session['original_file_name'] = result['original_name']
            
            # ✅ Generate URL dengan key yang benar
            original_file_url = url_for('uploaded_file', filename=result['original_name'])
            processed_file_url = url_for('uploaded_file', filename=result['processed_name'])
            
            return render_template('view/upload.html', 
                                 success=True,
                                 original_file=original_file_url,
                                 processed_file=processed_file_url,
                                 original_filename=result['original_filename'],
                                 download_filename=result['download_name'])
        
        except ValueError as e:
            return render_template('view/upload.html', success=False, error=str(e))
        except Exception as e:
            import traceback
            traceback.print_exc()
            return render_template('view/upload.html', success=False, error=f'Error: {str(e)}')