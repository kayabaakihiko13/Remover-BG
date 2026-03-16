from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# Upload & Model directories
UPLOAD_DIR = BASE_DIR / 'uploads'
MODEL_DIR = BASE_DIR / 'model'

# Auto create directories
UPLOAD_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)