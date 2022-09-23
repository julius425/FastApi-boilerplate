from fastapi import HTTPException

from app.models.codes import EmailCode
from app.schemas.codes import EmailCode_Pydantic


class AbstractCodeService:
    model = None
    key: str = 'email'  # specific field for searching, for example, email
    schema_out = None

    async def create(self, code_schema):
        code = await self.model.create(**code_schema.dict())
        return await self.schema_out.from_tortoise_orm(code)

    async def get(self, **kwargs) -> EmailCode_Pydantic:
        code = await self.model.filter(**kwargs).order_by('-id').first()
        if not code:
            raise HTTPException(400, 'No activation code was found')
        return await self.schema_out.from_tortoise_orm(code)

    async def exists(self, **kwargs) -> bool:
        return await self.model.filter(**kwargs).exists()

    async def verify_code(self, code_schema) -> bool:
        kwargs = {self.key: getattr(code_schema, self.key)}
        activation = await self.get(**kwargs)
        return code_schema.code == activation.code


class EmailCodeService(AbstractCodeService):
    model = EmailCode
    schema_out = EmailCode_Pydantic
    key = 'email'
