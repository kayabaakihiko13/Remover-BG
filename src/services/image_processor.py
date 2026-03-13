import io
import uuid
from pathlib import Path
from PIL import Image
from rembg import remove, new_session
from werkzeug.utils import secure_filename
from typing import Dict, Optional

from ..config import UPLOAD_DIR, MODEL_DIR

class ImageProcessor:
    """Service untuk memproses gambar (remove background)"""
    
    ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    
    def __init__(self, upload_dir: Path, model_dir: Path):
        self.upload_dir = Path(upload_dir)
        self.model_dir = Path(model_dir)
        self.session = new_session("u2netp")
    
    def validate_file(self, file_storage) -> None:
        """Validasi file yang diupload"""
        if not file_storage:
            raise ValueError("Tidak ada file yang dipilih")
        
        if file_storage.filename == '':
            raise ValueError("Nama file kosong")
        
        if file_storage.content_type not in self.ALLOWED_TYPES:
            raise ValueError(
                f"Tipe file tidak didukung ({file_storage.content_type}). "
                f"Gunakan JPG, PNG, atau WEBP."
            )
    
    def process_image(self, file_storage) -> Dict[str, str]:
        """
        Proses gambar untuk remove background
        
        Returns:
            Dict dengan informasi file original dan processed
        """
        # Validasi
        self.validate_file(file_storage)
        
        # Generate unique ID
        unique_id = str(uuid.uuid4())
        original_filename = secure_filename(file_storage.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        filename_without_ext = Path(original_filename).stem
        
        # Baca file
        img_bytes = file_storage.read()
        input_image = Image.open(io.BytesIO(img_bytes))
        
        # Simpan file original
        original_name = f"original_{unique_id}.{file_extension}"
        original_path = self.upload_dir / original_name
        input_image.save(original_path)
        
        # Process image (remove background)
        input_image_rgba = input_image.convert('RGBA')
        output_image = remove(input_image_rgba, session=self.session)
        
        # Simpan file hasil
        processed_name = f"processed_{unique_id}.png"
        processed_path = self.upload_dir / processed_name
        output_image.save(processed_path, format="PNG")
        
        return {
                'original_path': str(original_path),
                'processed_path': str(processed_path),
                'original_filename': original_filename,
                'original_name': original_name,
                'processed_name': processed_name,
                'download_name': f"removebg_{filename_without_ext}.png",
                'original_url_name': original_name,        # Sama dengan original_name
                'processed_url_name': processed_name,      # Sama dengan processed_name
            }
    def get_file_path(self, filename: str) -> Optional[Path]:
        """Get full path untuk file yang sudah diupload"""
        file_path = self.upload_dir / filename
        return file_path if file_path.exists() else None