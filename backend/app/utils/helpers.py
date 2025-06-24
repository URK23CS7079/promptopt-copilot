from pathlib import Path
import hashlib
from fastapi import UploadFile
import shutil

def save_uploaded_file(upload_file: UploadFile, target_dir: Path = Path("data")) -> Path:
    target_dir.mkdir(exist_ok=True)
    file_path = target_dir / upload_file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_path

def calculate_file_hash(file_path: Path) -> str:
    hash_md5 = hashlib.md5()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()