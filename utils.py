import os

def ensure_folder(folder_path):
    """
    Create a directory if it doesn't exist.
    
    Args:
        folder_path (str): Path to the directory to be created
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created directory: {folder_path}")
    else:
        print(f"Directory already exists: {folder_path}")
