import datetime

from fastapi_admin.models import AbstractAdmin
from tortoise import fields
from tortoise.validators import MinLengthValidator

from app.core.utils.mixins import CoreModel


class User(CoreModel):

    email = fields.CharField(100, unique=True, index=True)
    password = fields.CharField(128)
    name = fields.CharField(50)
    surname = fields.CharField(10)
    city = fields.CharField(30, null=True)
    company_name = fields.CharField(40, null=True)


    @staticmethod
    def get_contact_fields():
        return 'email',

    def __str__(self):
        return f'{self.name} {self.surname} | {self.email}'


class Admin(AbstractAdmin):
    """test"""
    last_login = fields.DatetimeField(description="Last Login", default=datetime.datetime.now)
    email = fields.CharField(max_length=200, default="")
    avatar = fields.CharField(max_length=200, default="")
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}#{self.username}"
