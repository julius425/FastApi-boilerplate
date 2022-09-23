from tortoise import fields

from app.core.utils.mixins import CoreModel


class Code(CoreModel):
    code = fields.CharField(4)

    class Meta:
        abstract = True


class EmailCode(Code):
    email = fields.CharField(100, index=True)
