from flask import Flask, send_from_directory
from flask_cors import CORS
from .config import Config  # ✅ Relative import
from .extensions import init_extensions
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='styles',
        static_url_path='/static'
    )
    
    app.config.from_object(Config)
    os.environ["U2NET_HOME"] = str(Config.MODEL_DIR)
    
    CORS(app)
    init_extensions(app)
    register_routes(app)
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)
    
    return app


def register_routes(app):
    """Register semua blueprint"""
    # ✅ Pakai relative import (pakai titik)
    from .routers.main import main_bp
    from .routers.upload import upload_bp
    from .routers.download import download_bp
    
    app.register_blueprint(main_bp,name_parameter='')
    app.register_blueprint(upload_bp,name_parameter='')
    app.register_blueprint(download_bp,name_parameter='')