import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Налаштування Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def upload_image(file_path: str):
    """upload_image AI is creating summary for upload_image

    Args:
        file_path (str): [description]

    Returns:
        [type]: [description]
    """    
    return cloudinary.uploader.upload(file_path, folder="avatars")

def delete_image(public_id: str):
    """delete_image AI is creating summary for delete_image

    Args:
        public_id (str): [description]

    Returns:
        [type]: [description]
    """    
    return cloudinary.uploader.destroy(public_id)
