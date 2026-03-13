from .directory import UPLOAD_DIR, MODEL_DIR
import os

class Config:
    """Configuration class"""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    
    UPLOAD_FOLDER = UPLOAD_DIR
    MODEL_DIR = MODEL_DIR
    
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    
    # Session config
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set True untuk production HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'

# Export semua yang diperlukan
__all__ = ['Config', 'UPLOAD_DIR', 'MODEL_DIR']