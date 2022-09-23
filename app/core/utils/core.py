import os
import inspect
import random
from typing import Type, Union
from time import time

import requests
from fastapi import Form, HTTPException
from fastapi_mail import MessageSchema, FastMail
from pydantic import BaseModel
from starlette.background import BackgroundTasks
from starlette.datastructures import UploadFile

from app.core.config import settings, mail_conf


def get_models_files() -> list:
    """:return [app.models.users, ...]"""
    from app.core.config import settings

    try:
        models_dir = os.listdir(os.path.join(settings.ROOT_DIR, 'app/models'))
    except FileNotFoundError:
        models_dir = os.listdir(os.path.join(settings.ROOT_DIR, 'models'))

    return [
        f'app.models.{f.split(".")[0]}' for f in models_dir
        if not f.startswith('__')
    ]


def make_unique_filename(filename: Union[str, UploadFile]) -> str:
    if isinstance(filename, UploadFile):
        filename = filename.filename

    filename, extension = os.path.splitext(filename)
    salt = str(time()).split(".")[-1]
    return f'{filename}-{salt}{extension}'


def as_form(cls: Type[BaseModel]):
    """Decorator to add as_form method to pydantic model
    for accepting form data
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
            annotation=field.outer_type_,
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


def add_if_not_none(dictionary: dict, key: str, value) -> dict:
    new_dict = dictionary.copy()
    if value:
        new_dict[key] = value
    return new_dict


def generate_code():
    return str(random.randint(1000, 9999))


def send_email(background_tasks: BackgroundTasks, subject: str, email_to: str, body: str):
    message = MessageSchema(subject=subject, recipients=[email_to], body=body)
    fm = FastMail(mail_conf)
    background_tasks.add_task(fm.send_message, message)
