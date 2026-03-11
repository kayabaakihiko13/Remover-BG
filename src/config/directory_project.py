from pathlib import Path

# Get project root (2 level up from this file)
BASE_DIR = Path(__file__).resolve().parents[2]
print(BASE_DIR)
# Define directories
TEMPLATE_DIR = BASE_DIR / "src" / "templates"
UPLOAD_DIR = BASE_DIR / "uploads"
STATIC_DIR = BASE_DIR / "static"
MODEL_DIR = BASE_DIR / "model"
