from typing import Any

from fastapi_admin.app import app
from fastapi_admin.resources import Link, Model, Dropdown, Field
from fastapi_admin.widgets import filters, inputs
from starlette.requests import Request

from app.core.utils.admin import get_admin_file_upload, get_admin_image_field
from app.models.users import User


class CustomModel(Model):
    """Base class for resource with page titles"""

    @property
    def page_pre_title(self):
        return f'{self.label} list'

    @property
    def page_title(self):
        return self.label


class CustomForeignKey(inputs.ForeignKey):
    async def parse_value(self, request: Request, value: Any):
        is_nullable = self.context.get("null", False) is True
        if not value and is_nullable:
            return None
        model = self.model
        field_pk_attr = model._meta.pk_attr
        obj = await model.get(**{field_pk_attr: value})
        return obj


@app.register
class Dashboard(Link):
    label = "Dashboard"
    icon = "fas fa-home"
    url = "/admin"


@app.register
class UserResource(CustomModel):
    label = 'User'
    model = User
    icon = 'fas fa-user'
    fields = [
        'id', 'email', 'name', 'surname', 'city', 'status',
        'INN', 'company_name', 'call_from_time', 'call_to_time'
    ]

