from tortoise import fields, Model

from app.core.utils.files import delete_file


class CoreModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class AbstractImageModel(CoreModel):
    image_path = fields.CharField(150, null=True)

    class Meta:
        abstract = True

    async def delete(self, *args, **kwargs):
        delete_file(self.image_path)
        await super().delete(*args, **kwargs)
