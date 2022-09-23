from fastapi_admin.file_upload import FileUpload
from fastapi_admin.resources import Field
from fastapi_admin.widgets import displays, inputs
from tortoise import Model

from app.core.utils.core import make_unique_filename
from app.core.utils.files import get_full_upload_dir, get_upload_dir


def get_admin_file_upload(model: Model) -> FileUpload:
    return FileUpload(
        uploads_dir=get_full_upload_dir(model),
        prefix=f'/media/{get_upload_dir(model)}',
        filename_generator=make_unique_filename
    )


def get_admin_image_field(upload: FileUpload) -> Field:
    """For models inherited from AbstractImageModel (with image_path prop)"""
    return Field(
        name='image_path',
        label='Image',
        display=displays.Image(),
        input_=inputs.Image(null=True, upload=upload),
    )
