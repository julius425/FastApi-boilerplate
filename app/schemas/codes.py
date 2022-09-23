from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.codes import EmailCode


EmailCode_Pydantic = pydantic_model_creator(EmailCode, name="EmailCode")
EmailCodeIn_Pydantic = pydantic_model_creator(EmailCode, name="EmailCodeIn",
                                              exclude_readonly=True)
