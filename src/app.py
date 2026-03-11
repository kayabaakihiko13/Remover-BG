import io
import os
import sys
import base64
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory
)
from flask_cors import CORS
from PIL import Image
from rembg import remove, new_session

from config.directory_project import UPLOAD_DIR, MODEL_DIR

# Configuration Application
sys.path.append(str(Path(__file__).parent.parent))

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='styles',
    static_url_path='/static'
)
CORS(app)

UPLOAD_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

os.environ["U2NET_HOME"] = str(MODEL_DIR)
BG_SESSION = new_session("u2netp")

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = str(UPLOAD_DIR)


@app.route('/')
def home():
    """Halaman Beranda"""
    return render_template('index.html')

@app.route('/about')
def about():
    """Halaman Tentang"""
    return render_template('view/about.html')

@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    """Halaman Upload & Proses Gambar"""
    
    if request.method == 'GET':
        return render_template('view/upload.html')
    
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file or file.filename == '':
            return render_template('view/upload.html', error='Tidak ada file yang dipilih.')
        
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if file.content_type not in allowed_types:
            return render_template('view/upload.html', 
                                 error=f'Tipe file tidak didukung ({file.content_type}). Gunakan JPG, PNG, atau WEBP.')
        
        try:
            img_bytes = file.read()
            input_image = Image.open(io.BytesIO(img_bytes))
            original_filename = file.filename
            
            if original_filename.lower().endswith(('.jpg', '.jpeg')):
                if input_image.mode in ('RGBA', 'P', 'LA'):
                    input_image = input_image.convert('RGB')
                input_image.save(UPLOAD_DIR / original_filename, 'JPEG', quality=95)
            else:
                input_image.save(UPLOAD_DIR / original_filename)
            
            input_image_rgba = input_image.convert('RGBA')
            output_image = remove(input_image_rgba, session=BG_SESSION)
            
            buffered = io.BytesIO()
            output_image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            processed_data = f"image/png;base64,{img_base64}"
            
            original_buffered = io.BytesIO()
            input_image.save(original_buffered, format="PNG")
            original_base64 = base64.b64encode(original_buffered.getvalue()).decode('utf-8')
            original_data = f"image/png;base64,{original_base64}"
            
            return render_template('view/upload.html', 
                                 original_file=original_data,
                                 processed_file=processed_data,
                                 success=True)
        
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return render_template('view/upload.html', error=f'Gagal memproses gambar: {str(e)}')

@app.route("/uploads/<filename>")
def uploaded_file(filename: str):
    """Route untuk mengakses file yang sudah diupload"""
    return send_from_directory(UPLOAD_DIR, filename)

@app.route('/health')
def health_check():
    """Endpoint untuk cek kesehatan server"""
    return jsonify({'status': 'healthy', 'service': 'remover-bg'})

@app.route('/public/<path:filename>')
def serve_static(filename):
    """Serve file statis dari folder styles"""
    return send_from_directory(app.static_folder, filename)

# == Error Handler
@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found"""
    return render_template('view/error_handling/404.html'), 404
@app.errorhandler(500)
def internal_error(error):
    # Cek apakah request dari browser (HTML) atau API (JSON)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Internal server error'}), 500
    else:
        return render_template('view/error_handling/500.html'), 500

@app.errorhandler(413)
def too_large(error):
    """
    Handle error file terlalu besar
    Render index.html dengan error message di alert box
    """
    # Return index.html dengan parameter error
    return render_template('index.html', 
                          error='File terlalu besar! Maksimal ukuran file adalah 10MB.'), 413

# Optional: Error handler untuk 403 (Forbidden)
@app.errorhandler(403)
def forbidden(error):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Access forbidden'}), 403
    else:
        return render_template('view/error_handling/403.html'), 403  # Buat file 403.html jika perlu
#  Servere Execute
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)