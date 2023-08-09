from PIL import Image

from app.tasks.celery_ import celery_app
from app.tasks.utils import count_files_in_folder, remove_file_from_disk


@celery_app.task
def process_image(folder: str, file_path: str):
    folder_path = f"./app/static/images/{folder}/"
    file_name = f"{count_files_in_folder(folder_path) + 1}.webp"
    img = Image.open(file_path)
    img = img.convert("RGB")
    img.thumbnail((600, 500))
    img.save(f"{folder_path}{file_name}", "webp")
    remove_file_from_disk(file_path)
    return file_name
