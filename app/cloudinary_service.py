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
    return cloudinary.uploader.upload(file_path, folder="avatars")

def delete_image(public_id: str):
    return cloudinary.uploader.destroy(public_id)
