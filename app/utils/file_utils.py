import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'csv'}

def allowed_file(filename):
    """Check if a file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, subfolder=None):
    """Save a file to the upload folder"""
    if not file or file.filename == '':
        return None
        
    if not allowed_file(file.filename):
        return None
        
    filename = secure_filename(file.filename)
    
    # Create subfolder if specified
    folder_path = UPLOAD_FOLDER
    if subfolder:
        folder_path = os.path.join(UPLOAD_FOLDER, subfolder)
    
    # Ensure directory exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Save file
    filepath = os.path.join(folder_path, filename)
    file.save(filepath)
    
    # Return relative path
    if subfolder:
        return os.path.join(subfolder, filename)
    return filename

def delete_file(filepath):
    """Delete a file from the upload folder"""
    if not filepath:
        return False
        
    full_path = os.path.join(UPLOAD_FOLDER, filepath)
    if os.path.exists(full_path):
        os.remove(full_path)
        return True
    return False