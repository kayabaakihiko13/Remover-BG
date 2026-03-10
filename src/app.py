from flask import (Flask, render_template, request, send_file, jsonify, send_from_directory)
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
from pathlib import Path
import sys
from config.directory_project import BASE_DIR,UPLOAD_DIR


# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Initialize Flask app
app = Flask(__name__,
            template_folder='templates',
            static_folder='styles',
            static_url_path='/static') 
CORS(app)


# Create directories if not exist
UPLOAD_DIR.mkdir(exist_ok=True)

# Config
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max
app.config['UPLOAD_FOLDER'] = str(UPLOAD_DIR)

# ============== Routes ==============

@app.route('/')
def home():
    """Home page with upload interface"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('view/about.html')


@app.route('/remove-bg', methods=['POST'])
def remove_background():
    """
    Remove background from uploaded image
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    if file.content_type not in allowed_types:
        return jsonify({'error': 'Invalid file type. Allowed: JPG, PNG, WEBP'}), 400
    
    try:
        # Read and process image
        image_data = file.read()
        input_image = Image.open(io.BytesIO(image_data))
        output_image = remove(input_image)
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'no-bg-{file.filename}'
        )
    
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'remover-bg'})

@app.route('/public/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory(app.static_folder, filename)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def too_large(error):
    return jsonify({'error': 'File too large. Maximum size: 10MB'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)