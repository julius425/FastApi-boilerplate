import os
import shutil

from fastapi import UploadFile
from tortoise import Model

from app.core.config import settings
from app.core.utils.core import make_unique_filename


def save_image(upload_dir: str, file: UploadFile) -> str:
    """
    :param upload_dir: absolute path to upload
    :return the relative image path: /<media_dir>/<model_dir>/filename.ext
    """
    os.makedirs(upload_dir, exist_ok=True)  # create dir if it doesn't exist
    img_path = os.path.join(upload_dir, make_unique_filename(file.filename))

    with open(img_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return img_path[len(settings.ROOT_DIR):]


def get_upload_dir(model: Model) -> str:
    if hasattr(model, 'upload_dir'):
        return model.upload_dir
    return model.__class__.__name__


def get_full_upload_dir(model: Model) -> str:
    """:return path to upload a file. Default: model name"""
    upload_to = get_upload_dir(model)
    return os.path.join(settings.ROOT_DIR, settings.MEDIA_PATH, upload_to)


def delete_file(path: str):
    """:param path: relative path starting with media/static catalogue.
    Example: media/boar/fdfdf.jpg
    """
    os.remove(f'{settings.ROOT_DIR}{os.path.join(settings.ROOT_DIR, path)}')
