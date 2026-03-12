import io
import os
import sys
import base64
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    send_file,
    session,
    url_for  # ✅ ADDED THIS
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
app.secret_key = 'your-secret-key-here-ganti-ini'  # Ganti dengan key yang aman
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
        return render_template('view/upload.html', success=False)
    
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file or file.filename == '':
            return render_template('view/upload.html', 
                                 success=False, 
                                 error='Tidak ada file yang dipilih.')
        
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if file.content_type not in allowed_types:
            return render_template('view/upload.html', 
                                 success=False,
                                 error=f'Tipe file tidak didukung ({file.content_type}). Gunakan JPG, PNG, atau WEBP.')
        
        try:
            # Generate unique ID untuk file
            unique_id = str(uuid.uuid4())
            original_filename = secure_filename(file.filename)
            filename_without_ext = os.path.splitext(original_filename)[0]
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            
            # Baca file
            img_bytes = file.read()
            input_image = Image.open(io.BytesIO(img_bytes))
            
            # Simpan file original
            original_filename_saved = f"original_{unique_id}.{file_extension}"
            original_path = UPLOAD_DIR / original_filename_saved
            input_image.save(original_path)
            
            # Process image (remove background)
            input_image_rgba = input_image.convert('RGBA')
            output_image = remove(input_image_rgba, session=BG_SESSION)
            
            # Simpan file hasil
            processed_filename_saved = f"processed_{unique_id}.png"
            processed_path = UPLOAD_DIR / processed_filename_saved
            output_image.save(processed_path, format="PNG")
            
            # Simpan info di session untuk download
            session['processed_file_path'] = str(processed_path)
            session['processed_filename_saved'] = processed_filename_saved
            session['download_filename'] = f"removebg_{filename_without_ext}.png"
            
            # Generate URL untuk preview gambar
            original_file_url = url_for('uploaded_file', filename=original_filename_saved)
            processed_file_url = url_for('uploaded_file', filename=processed_filename_saved)
            
            return render_template('view/upload.html', 
                                 success=True,
                                 original_file=original_file_url,
                                 processed_file=processed_file_url,
                                 original_filename=original_filename,
                                 download_filename=f"removebg_{filename_without_ext}.png")
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"ERROR: {str(e)}")
            return render_template('view/upload.html', 
                                 success=False,
                                 error=f'Gagal memproses gambar: {str(e)}')


@app.route("/uploads/<filename>")
def uploaded_file(filename: str):
    """Route untuk mengakses file yang sudah diupload"""
    return send_from_directory(UPLOAD_DIR, filename)


@app.route('/download-result')
def download_result():
    """Route untuk download hasil processing"""
    processed_filename = session.get('processed_filename_saved')
    download_filename = session.get('download_filename', 'result.png')
    
    if processed_filename:
        file_path = UPLOAD_DIR / processed_filename
        if file_path.exists():
            return send_file(
                file_path,
                mimetype='image/png',
                as_attachment=True,
                download_name=download_filename
            )
    
    return jsonify({'error': 'File tidak ditemukan'}), 404


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
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Internal server error'}), 500
    else:
        return render_template('view/error_handling/500.html'), 500


@app.errorhandler(413)
def too_large(error):
    """Handle error file terlalu besar"""
    return render_template('index.html', 
                          error='File terlalu besar! Maksimal ukuran file adalah 10MB.'), 413


@app.errorhandler(403)
def forbidden(error):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Access forbidden'}), 403
    else:
        return render_template('view/error_handling/403.html'), 403


# Server Execute
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)