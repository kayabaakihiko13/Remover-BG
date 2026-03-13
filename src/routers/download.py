from flask import (
    Blueprint, 
    session, 
    send_file, 
    jsonify, 
    current_app
)
from pathlib import Path

download_bp = Blueprint('download', __name__, url_prefix='/')


@download_bp.route('/download-result')
def download_result():
    """Route untuk download hasil processing"""
    processed_filename = session.get('processed_file_name')
    download_filename = session.get('download_filename', 'result.png')
    
    if processed_filename:
        file_path = Path(current_app.config['UPLOAD_FOLDER']) / processed_filename
        
        if file_path.exists():
            return send_file(
                file_path,
                mimetype='image/png',
                as_attachment=True,
                download_name=download_filename
            )
    
    return jsonify({'error': 'File tidak ditemukan atau session expired'}), 404