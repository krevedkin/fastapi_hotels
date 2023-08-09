from fastapi import APIRouter, UploadFile

from app.images.exceptions import FileNameIsNoneHTTPException
from app.images.schemas import FolderToSave
from app.tasks.tasks import process_image
from app.tasks.utils import save_file_to_disk

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("/resize")
async def resize_image_to_webp(folder_to_save: FolderToSave, file: UploadFile):
    if file.filename:
        tmp_path = save_file_to_disk(file_name=file.filename, file=file.file)
    else:
        raise FileNameIsNoneHTTPException

    process_image.delay(folder_to_save, tmp_path)
    return {"task_recieved": True}
