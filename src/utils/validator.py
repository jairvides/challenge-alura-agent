import os

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.csv', '.json', '.html', '.md', '.xlsx'}
MAX_FILE_SIZE_MB = 10

def validate_file(file_path: str) -> (bool, str):
    """
    Validates if the file format is supported and within size limits.
    """
    # Check extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Formato {ext} no permitido. Permitidos: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return False, f"Archivo demasiado grande ({file_size_mb:.2f} MB). Máximo: {MAX_FILE_SIZE_MB} MB"
        
    return True, "Archivo válido"
